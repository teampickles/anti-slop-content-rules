import sys,unittest,tempfile
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import build_bundle as builder
from validate import validate
class BundleTests(unittest.TestCase):
    def test_integrity(self):validate()
    def test_copy_changes_propagate(self):
        import shutil
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)
            for name in ['rules','licenses']:shutil.copytree(builder.ROOT/name,root/name)
            for name in ['LICENSE','NOTICE.md','VERSION']:shutil.copyfile(builder.ROOT/name,root/name)
            p=root/'rules/copy.md';p.write_text(p.read_text().replace('Name what happens:', 'Changed functional wording:'))
            with patch.object(builder,'ROOT',root):self.assertIn('Changed functional wording:',builder.build())
    def test_stale_bundle_is_rejected(self):
        self.check_rejected('stale')

    def check_rejected(self, scenario, optimized=False):
        import shutil, subprocess
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder)/'repo'
            shutil.copytree(builder.ROOT,root,ignore=shutil.ignore_patterns('.git','__pycache__'))
            if scenario=='stale':
                (root/'CONTENT-RULES.md').write_text('stale')
            elif scenario=='license':
                (root/'licenses/no-ai-slop-MIT.txt').unlink()
                subprocess.run([sys.executable,'scripts/build_bundle.py'],cwd=root,check=True,capture_output=True)
            elif scenario=='anchor':
                (root/'README.md').write_text('[Section](rules/copy.md#missing-section)')
            elif scenario=='level':
                p=root/'rules/copy.md';p.write_text(p.read_text().replace('[MUST]','[UNKNOWN]',1))
                subprocess.run([sys.executable,'scripts/build_bundle.py'],cwd=root,check=True,capture_output=True)
            command=[sys.executable]+(['-O'] if optimized else [])+['scripts/validate.py']
            result=subprocess.run(command,cwd=root,text=True,capture_output=True)
            self.assertNotEqual(result.returncode,0,result.stdout)
            self.assertIn('FAIL:',result.stderr)

    def test_optimized_python_still_rejects_stale_bundle(self):
        self.check_rejected('stale',optimized=True)

    def test_missing_notice_cannot_disappear_from_rebuilt_bundle(self):
        self.check_rejected('license')

    def test_broken_local_heading_is_rejected(self):
        self.check_rejected('anchor')

    def test_unknown_rule_level_is_rejected(self):
        self.check_rejected('level')

    def test_valid_anchor_and_fenced_examples(self):
        import validate as checker
        self.assertEqual(checker.heading_ids('# Repeat\n## Repeat\n```markdown\n# Hidden\n```\n'),{'repeat','repeat-1'})

if __name__=='__main__':unittest.main()
