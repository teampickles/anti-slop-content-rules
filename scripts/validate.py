"""Validate content packaging, not the quality of future writing."""
import re
import sys
from urllib.parse import unquote, urlsplit

from build_bundle import ROOT, build

REQUIRED_LICENSES = ('no-ai-slop-MIT.txt', 'no-slop-ui-MIT.txt', 'taste-skill-MIT.txt')


def without_fences(text):
    return re.sub(r'^```[^\n]*\n.*?^```\s*$', '', text, flags=re.M | re.S)


def heading_ids(text):
    """IDs for the plain ATX headings used by this package, including duplicates."""
    used = set()
    for title in re.findall(r'^#+ (.+)$', without_fences(text), re.M):
        base = re.sub(r'[^\w\- ]', '', title.lower()).replace(' ', '-')
        candidate, index = base, 0
        while candidate in used:
            index += 1
            candidate = f'{base}-{index}'
        used.add(candidate)
    return used


def validate():
    expected = {f'C{i:02}' for i in range(1, 27)} | {f'E{i:02}' for i in range(1, 9)}
    required = [ROOT/'LICENSE', ROOT/'NOTICE.md', ROOT/'VERSION',
                *(ROOT/'licenses'/name for name in REQUIRED_LICENSES)]
    for path in required:
        if not path.is_file() or not path.read_text(encoding='utf-8').strip():
            raise ValueError(f'Missing or empty required file: {path.relative_to(ROOT)}')
    text = build()
    ids = re.findall(r'^### ([A-Z]+\d{2}) \[(?:MUST|DEFAULT|REVIEW)\]', text, re.M)
    all_ids = re.findall(r'^### ([A-Z]+\d{2})\b', text, re.M)
    if len(ids) != len(set(ids)) or set(ids) != expected or ids != all_ids:
        raise ValueError('Rule coverage, levels or duplicate IDs are invalid')
    bundle = ROOT/'CONTENT-RULES.md'
    if not bundle.is_file() or bundle.read_text(encoding='utf-8') != text:
        raise ValueError('CONTENT-RULES.md is missing or stale')
    for path in [ROOT/'LICENSE', ROOT/'NOTICE.md', *(ROOT/'licenses').glob('*.txt')]:
        if path.read_text(encoding='utf-8').strip() not in text:
            raise ValueError(f'Missing license/notice in bundle: {path.name}')
    for path in ROOT.rglob('*.md'):
        if '.git' in path.relative_to(ROOT).parts:
            continue
        for link in re.findall(r'\[[^\]\n]+\]\(([^)]+)\)', without_fences(path.read_text(encoding='utf-8'))):
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            destination = path.parent/unquote(parsed.path) if parsed.path else path
            if not destination.is_file():
                raise ValueError(f'Broken local link in {path.relative_to(ROOT)}: {link}')
            if parsed.fragment and destination.suffix == '.md':
                if unquote(parsed.fragment) not in heading_ids(destination.read_text(encoding='utf-8')):
                    raise ValueError(f'Broken heading link in {path.relative_to(ROOT)}: {link}')
    print('Validated 34 editorial/copy rules, bundle, required licenses and local links/headings.')


if __name__ == '__main__':
    try:
        validate()
    except (ValueError, OSError) as exc:
        print(f'FAIL: {exc}', file=sys.stderr)
        sys.exit(1)
