# 扫描 CSP-J/ 与 CSP-S/ 下的题解，生成导航页使用的 problems.js
import json, os, re

root = os.path.dirname(os.path.abspath(__file__))
items = []
for contest in ['CSP-J', 'CSP-S']:
    for year in sorted(os.listdir(os.path.join(root, contest))):
        folder = os.path.join(root, contest, year)
        for f in sorted(os.listdir(folder)):
            m = re.match(r'(P\d+) (\S+) (.+)\.md$', f)
            if not m:
                continue
            pid, slot, name = m.groups()
            text = open(os.path.join(folder, f), encoding='utf-8').read()
            tags = re.search(r'\*\*标签\*\*：(.*?)\s*\*\*难度', text)
            diff = re.search(r'\*\*难度\*\*：(\d+)/10', text)
            items.append({
                'pid': pid, 'contest': contest, 'year': int(year), 'slot': slot, 'name': name,
                'path': f'{contest}/{year}/{f}',
                'tags': [t.strip() for t in re.split(r'[、,，]', tags.group(1))] if tags else [],
                'diff': int(diff.group(1)) if diff else None,
            })

with open(os.path.join(root, 'problems.js'), 'w', encoding='utf-8') as out:
    out.write('const PROBLEMS = [\n' + ',\n'.join(json.dumps(x, ensure_ascii=False) for x in items) + '\n];\n')
print(len(items), 'problems')
