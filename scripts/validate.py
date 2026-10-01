"""Validate content packaging, not the quality of future writing."""
import re
from build_bundle import ROOT,build

def validate():
    expected={f'C{i:02}' for i in range(1,27)}|{f'E{i:02}' for i in range(1,9)}
    text=build();ids=re.findall(r'^### ([A-Z]+\d{2}) \[',text,re.M)
    assert len(ids)==len(set(ids)) and set(ids)==expected, 'Rule coverage or duplicates'
    assert (ROOT/'CONTENT-RULES.md').read_text()==text, 'Stale bundle'
    for p in [ROOT/'LICENSE',ROOT/'NOTICE.md',*sorted((ROOT/'licenses').glob('*.txt'))]:
        assert p.read_text().strip() in text, 'Missing license/notice'
    for p in ROOT.rglob('*.md'):
        if '.git' in p.parts:continue
        for link in re.findall(r'\[[^\]\n]+\]\(([^)]+)\)',p.read_text()):
            if '://' not in link and not link.startswith('#'):
                assert (p.parent/link.split('#')[0]).exists(), f'Broken link: {p}: {link}'
    print('Validated 34 editorial/copy rules, bundle, licenses and local links.')
if __name__=='__main__':validate()
