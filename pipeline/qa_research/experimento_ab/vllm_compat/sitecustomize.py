"""Compatibilidade do vLLM 0.28 com Python 3.10 (venv_vllm da DL-28), carregada em todos os processos via PYTHONPATH.

O flashinfer 0.6.16 usa `array.array[int]` numa anotação (só válido no Python 3.12+), e o vLLM importa
`flashinfer.comm` ao iniciar o tensor parallel; o erro é TypeError, que o vLLM não captura. Aqui `flashinfer.comm`
passa a falhar com ImportError, que o vLLM trata: o all-reduce fica com o NCCL/custom all-reduce de sempre.
"""
import importlib.abc
import sys

if sys.version_info < (3, 12):
    class _SemFlashinferComm(importlib.abc.MetaPathFinder):
        def find_spec(self, nome, caminho=None, alvo=None):
            if nome == "flashinfer.comm" or nome.startswith("flashinfer.comm."):
                raise ImportError("flashinfer.comm desativado (exige Python 3.12+)")
            return None

    sys.meta_path.insert(0, _SemFlashinferComm())
