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
        import validate as checker
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);(root/'CONTENT-RULES.md').write_text('stale')
            with patch.object(checker,'ROOT',root):
                with self.assertRaises(AssertionError):checker.validate()
if __name__=='__main__':unittest.main()
