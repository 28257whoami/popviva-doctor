#!/usr/bin/env python3
"""Exercise download/cache/corruption handling without any network or release execution."""
import hashlib
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


class BootstrapIntegrityTest(unittest.TestCase):
    def test_integrity_on_supported_platforms(self):
        source = Path(__file__).with_name('agent-doctor-bootstrap')
        for os_name, platform in [('Darwin', 'darwin-arm64'), ('Linux', 'linux-arm64')]:
            with self.subTest(platform=platform), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                (root / 'tools').mkdir()
                shutil.copy2(source, root / 'tools/agent-doctor-bootstrap')
                stub = root / 'stub-bin'
                stub.mkdir()
                payload = root / 'download-payload'
                good = b'fixture binary content, never executed\n'
                payload.write_bytes(good)
                digest = hashlib.sha256(good).hexdigest()
                (root / '.agent-doctor-version').write_text(
                    f'version: v-test\nbinaries:\n  {platform}: sha256:{digest}\n')
                (stub / 'uname').write_text(
                    '#!/bin/sh\nif [ "$1" = -s ]; then echo "$BOOTSTRAP_TEST_OS"; else echo arm64; fi\n')
                (stub / 'curl').write_text(
                    '#!/bin/sh\necho fetch >> "$BOOTSTRAP_TEST_COUNT"\n'
                    'while [ "$#" -gt 1 ]; do shift; done\ncp "$BOOTSTRAP_TEST_PAYLOAD" "$1"\n')
                for executable in stub.iterdir():
                    executable.chmod(0o755)
                count = root / 'downloads'
                env = dict(os.environ, PATH=f'{stub}:{os.environ["PATH"]}',
                           BOOTSTRAP_TEST_OS=os_name, BOOTSTRAP_TEST_PAYLOAD=str(payload),
                           BOOTSTRAP_TEST_COUNT=str(count))
                def run():
                    return subprocess.run(['bash', 'tools/agent-doctor-bootstrap'], cwd=root,
                                          env=env, capture_output=True, text=True)
                target = root / 'tools/.bin/agent-doctor-v-test'
                result = run()
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(target.read_bytes(), good)
                self.assertTrue(os.access(target, os.X_OK))
                self.assertEqual(run().returncode, 0)
                self.assertEqual(len(count.read_text().splitlines()), 1, 'valid cache must avoid download')
                target.write_bytes(b'corrupt cache')
                self.assertEqual(run().returncode, 0)
                self.assertEqual(target.read_bytes(), good)
                target.unlink()
                payload.write_bytes(b'corrupt download')
                self.assertNotEqual(run().returncode, 0)
                self.assertFalse(target.exists())
                self.assertFalse(target.with_suffix('.tmp').exists())


if __name__ == '__main__':
    unittest.main()
