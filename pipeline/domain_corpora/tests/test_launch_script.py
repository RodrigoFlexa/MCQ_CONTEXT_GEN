"""Launcher Bash com Python simulado: não baixa dados e não chama Azure."""
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

from pipeline.fase_4.config import ROOT
from test_corpora import setUpModule,tearDownModule

GIT_BASH=Path('C:/Program Files/Git/bin/bash.exe')
BASH=str(GIT_BASH) if GIT_BASH.is_file() else shutil.which('bash')


@unittest.skipUnless(BASH,'Bash indisponível')
class Launcher(unittest.TestCase):
    script=ROOT/'pipeline/fase_4/run_qa_v6.sh'

    def run_bash(self,args,env=None):
        return subprocess.run([BASH,'--noprofile','--norc',*args],env=env,capture_output=True,text=True,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name=='nt' else 0)

    def test_shell_syntax(self):
        result=self.run_bash(['-n',self.script.as_posix()])
        self.assertEqual(result.returncode,0,result.stderr)

    def test_launcher_forwards_exact_generation_flags_and_resume(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);manifest=root/'manifest.json';manifest.write_text('{}')
            fake=root/'fake-python.sh'
            fake.write_text('#!/usr/bin/env bash\nprintf "ARG:%s\\n" "$@"\n',encoding='utf-8')
            fake.chmod(0o755)
            env={**os.environ,'PYTHON_BIN':fake.as_posix(),'QA_CORPUS_MANIFEST':manifest.as_posix(),
                 'QA_OUTPUT':(root/'output with spaces').as_posix()}
            result=self.run_bash([self.script.as_posix(),'--resume','--max-calls','40000'],env)
            self.assertEqual(result.returncode,0,result.stderr)
            args=result.stdout.splitlines()
            for pair in (('--context-mode','composed'),('--chunk-words','1000'),('--chunks-per-facet','10'),
                         ('--deployment','gpt-5-4-petrobras'),('--effort','medium')):
                pos=args.index('ARG:'+pair[0]);self.assertEqual(args[pos+1],'ARG:'+pair[1])
            self.assertIn('ARG:--observe-only',args);self.assertIn('ARG:--resume',args)
            self.assertIn('ARG:'+(root/'output with spaces').as_posix(),args)
            self.assertNotIn('ARG:pipeline/domain_corpora/install_corpora.py',args)

    def test_missing_manifest_fails_before_any_python_call(self):
        with tempfile.TemporaryDirectory() as directory:
            env={**os.environ,'QA_CORPUS_MANIFEST':(Path(directory)/'missing.json').as_posix(),
                 'PYTHON_BIN':'does-not-exist'}
            result=self.run_bash([self.script.as_posix()],env)
            self.assertEqual(result.returncode,2);self.assertIn('Manifesto',result.stdout)


if __name__=='__main__':unittest.main()
