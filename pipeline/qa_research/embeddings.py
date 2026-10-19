"""Embeddings Azure: protocolo explícito, cache por conteúdo e entrada sem truncamento."""
import json
import random
import sqlite3
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np

from pipeline.inventario.llm import CallFailed, is_fatal, is_transient, load_dotenv, retry_after
from pipeline.inventario.textutil import sha


class AzureEmbedder:
    def __init__(self, config, budget, client=None, settings=None, tokenizer=None, sleep=time.sleep):
        self.config, self.budget, self.sleep = config, budget, sleep
        self.lock = threading.RLock()
        load_dotenv(Path(__file__).resolve().parents[2])
        if client is None:
            from azure_openai_backend import AzureSettings, AzureOpenAIBackend
            from openai import AzureOpenAI
            settings = settings or AzureSettings.load()
            settings.require()
            kwargs = dict(api_key=settings.azure_api_key, api_version=settings.azure_api_version,
                          timeout=config.timeout, max_retries=0)
            kwargs["base_url" if settings.use_base_url else "azure_endpoint"] = settings.azure_endpoint
            http = AzureOpenAIBackend._build_http_client(settings.ca_bundle, config.timeout)
            if http is not None:
                kwargs["http_client"] = http
            client = AzureOpenAI(**kwargs)
        self.client, self.tokenizer = client, tokenizer
        endpoint = getattr(settings, "azure_endpoint", None) or "injected-test-client"
        self.protocol = {"provider": "azure", "model": config.embedding_model,
            "deployment": config.embedding_deployment, "dimensions": config.embedding_dimensions,
            "declared_model_version": config.embedding_model_version,
            "api_version": getattr(settings, "azure_api_version", None),
            "endpoint_signature": sha(endpoint, 64), "tokenizer": "cl100k_base",
            "window": config.embedding_window_tokens, "overlap": config.embedding_overlap_tokens,
            "aggregation": "weighted_new_tokens_l2_v1", "text": "original_body_only_v1"}
        self.signature = sha(json.dumps(self.protocol, sort_keys=True), 64)
        directory = Path(config.index_dir) / "embeddings" / self.signature
        directory.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(directory / "vectors.sqlite3", check_same_thread=False, timeout=60)
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("CREATE TABLE IF NOT EXISTS vectors (digest TEXT PRIMARY KEY, value BLOB NOT NULL)")
        self.db.commit()
        self.log = Path(config.output) / "chamadas_embeddings.jsonl"

    def _get(self, digest):
        row = self.db.execute("SELECT value FROM vectors WHERE digest=?", (digest,)).fetchone()
        if row is None:
            return None
        vector = np.frombuffer(row[0], dtype=np.float32).copy()
        if vector.shape != (self.config.embedding_dimensions,) or not np.isfinite(vector).all():
            raise ValueError("Cache de embeddings inválido")
        if abs(float(np.linalg.norm(vector)) - 1) > .001:
            raise ValueError("Vetor em cache não normalizado")
        return vector

    def _tokens(self, text):
        if self.tokenizer is None:
            from pipeline.fase_4.prepare_tokenizer import ensure_tokenizer
            self.tokenizer = ensure_tokenizer()
        return self.tokenizer.encode(text, disallowed_special=())

    def _request(self, inputs):
        last = None
        for attempt in range(self.config.max_attempts):
            self.budget.reserve()  # Cada tentativa HTTP conta, inclusive retentativas.
            row = {"at": datetime.now(timezone.utc).isoformat(), "protocol": self.signature,
                   "deployment": self.config.embedding_deployment, "items": len(inputs),
                   "input_tokens_counted": sum(map(len, inputs)), "attempt": attempt + 1}
            started = time.monotonic()
            try:
                response = self.client.embeddings.create(model=self.config.embedding_deployment,
                    input=inputs, dimensions=self.config.embedding_dimensions, encoding_format="float")
                values = {}
                for item in response.data:
                    vector = np.asarray(item.embedding, dtype=np.float32)
                    if (type(item.index) is not int or item.index in values or not 0 <= item.index < len(inputs)
                            or vector.shape != (self.config.embedding_dimensions,) or not np.isfinite(vector).all()
                            or np.linalg.norm(vector) < 1e-12):
                        raise ValueError("Resposta de embeddings inválida: dimensão, índice ou vetor")
                    values[item.index] = vector / np.linalg.norm(vector)
                if len(values) != len(inputs):
                    raise ValueError("Resposta de embeddings incompleta")
                row.update(model=getattr(response, "model", None),
                           total_tokens=getattr(getattr(response, "usage", None), "total_tokens", None))
                return [values[i] for i in range(len(inputs))]
            except Exception as exc:
                row["error_type"] = type(exc).__name__
                last = exc
                if is_fatal(exc) or not is_transient(exc) or attempt + 1 == self.config.max_attempts:
                    raise
            finally:
                row["seconds"] = round(time.monotonic() - started, 3)
                self.log.parent.mkdir(parents=True, exist_ok=True)
                with self.log.open("a", encoding="utf-8") as stream:
                    stream.write(json.dumps(row, ensure_ascii=False) + "\n")
            self.sleep(min(60, max(retry_after(last), 2 ** attempt + random.random())))
        raise CallFailed("Embeddings indisponíveis") from last

    def encode(self, texts):
        with self.lock:
            texts = list(texts)
            if not texts:
                return np.empty((0, self.config.embedding_dimensions), dtype=np.float32)
            if any(not isinstance(text, str) or not text.strip() for text in texts):
                raise ValueError("Embedding de texto vazio ou inválido não é permitido")
            keys = [sha(text, 64) for text in texts]
            pending, seen, batch, positions, batch_tokens = {}, set(), [], [], 0

            def flush():
                nonlocal batch_tokens
                if not batch:
                    return
                for (key, weight), vector in zip(positions, self._request(batch)):
                    state = pending[key]
                    state["sum"] += weight * vector
                    state["received"] += 1
                    if state["received"] == state["expected"]:
                        total = state["sum"]
                        norm = float(np.linalg.norm(total))
                        if norm < 1e-12:
                            raise ValueError("Agregação de embeddings resultou em vetor nulo")
                        self.db.execute("INSERT OR REPLACE INTO vectors VALUES (?,?)",
                                        (key, (total / norm).astype(np.float32).tobytes()))
                self.db.commit()
                batch.clear()
                positions.clear()
                batch_tokens = 0

            for text, key in zip(texts, keys):
                if not isinstance(text, str) or not text.strip():
                    raise ValueError("Embedding de texto vazio não é permitido")
                if key in seen or self._get(key) is not None:
                    continue
                seen.add(key)
                tokens = self._tokens(text)
                if not tokens:
                    raise ValueError("Tokenizer retornou entrada vazia")
                window, overlap = self.config.embedding_window_tokens, self.config.embedding_overlap_tokens
                pieces, weights = [], []
                for start in range(0, len(tokens), window - overlap):
                    part = tokens[start:start + window]
                    pieces.append(part)
                    weights.append(len(part) if start == 0 else len(part) - overlap)
                    if start + window >= len(tokens):
                        break
                pending[key] = {"sum": np.zeros(self.config.embedding_dimensions, dtype=np.float32),
                                "received": 0, "expected": len(pieces)}
                for part, weight in zip(pieces, weights):
                    if batch and (len(batch) >= self.config.embedding_batch_size
                                  or batch_tokens + len(part) > self.config.embedding_batch_tokens):
                        flush()
                    batch.append(part)
                    positions.append((key, weight))
                    batch_tokens += len(part)
            flush()
            return np.stack([self._get(key) for key in keys])

    def close(self):
        self.db.close()
        if hasattr(self.client, "close"):
            self.client.close()
