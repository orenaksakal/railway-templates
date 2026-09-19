"""Merge the three reviewed groups into the fifteen-template release catalog."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main():
    for prefix, suffix in [('marketplace', ''), ('images', '.lock'),
                           ('sources', '.lock'), ('eligibility', '')]:
        merged = {}
        for group in 'abc':
            path = ROOT / f'{prefix}.round10-{group}{suffix}.json'
            values = json.loads(path.read_text())
            for key, value in values.items():
                if key in merged and merged[key] != value:
                    raise RuntimeError(f'Conflicting {prefix} entry: {key}')
                merged[key] = value
        if prefix != 'images' and len(merged) != 15:
            raise RuntimeError(f'Expected 15 {prefix} entries, found {len(merged)}')
        (ROOT / f'{prefix}.round10{suffix}.json').write_text(
            json.dumps(merged, indent=2, sort_keys=True) + '\n')
    print('Assembled fifteen templates and their image/source/eligibility records.')


if __name__ == '__main__':
    main()
