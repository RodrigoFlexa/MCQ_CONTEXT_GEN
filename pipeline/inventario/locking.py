"""Impede duas execuções de escreverem na mesma saída; o SO libera após interrupção."""
import os
from contextlib import contextmanager
from pathlib import Path


@contextmanager
def output_lock(output):
    path = Path(output)
    path.mkdir(parents=True, exist_ok=True)
    with (path / '.run.lock').open('a+b') as stream:
        stream.seek(0, 2)
        if stream.tell() == 0:
            stream.write(b'0')
            stream.flush()
        stream.seek(0)
        if os.name == 'nt':
            import msvcrt
            try:
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise RuntimeError('Outra execução usa esta saída; escolha outra pasta ou aguarde') from exc
        else:
            import fcntl
            try:
                fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError as exc:
                raise RuntimeError('Outra execução usa esta saída; escolha outra pasta ou aguarde') from exc
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == 'nt':
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)
