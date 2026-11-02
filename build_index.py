# 扫描 CSP-J/、CSP-S/ 下的题解与 knowledge/ 下的知识点，生成导航页使用的 problems.js 与 knowledge.js
import json, os, re

root = os.path.dirname(os.path.abspath(__file__))


def split_list(s):
    return [t.strip() for t in re.split(r'[、,，]', s) if t.strip()]


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
                'tags': split_list(tags.group(1)) if tags else [],
                'diff': int(diff.group(1)) if diff else None,
            })

cat_names = {
    'language-basics': '语言基础', 'basic-algorithms': '基础算法', 'data-structures': '数据结构',
    'dynamic-programming': '动态规划', 'graph-theory': '图论', 'math': '数学', 'strings': '字符串',
}
kb = []
kb_root = os.path.join(root, 'knowledge')
for cat in sorted(os.listdir(kb_root)):
    mc = re.match(r'(\d+)-(.+)$', cat)
    if not mc:
        continue
    for f in sorted(os.listdir(os.path.join(kb_root, cat))):
        m = re.match(r'(\d+)-.+\.md$', f)
        if not m:
            continue
        text = open(os.path.join(kb_root, cat, f), encoding='utf-8').read()
        level = re.search(r'\*\*组别\*\*：([JS])', text)
        keys = re.search(r'\*\*关键词\*\*：(.*)', text)
        kb.append({
            'id': f'{mc.group(1)}-{m.group(1)}', 'cat': cat_names[mc.group(2)],
            'name': re.match(r'# (.+)', text).group(1).strip(),
            'path': f'knowledge/{cat}/{f}',
            'level': level.group(1) if level else None,
            'keys': split_list(keys.group(1)) if keys else [],
        })


def dump(name, var, rows):
    with open(os.path.join(root, name), 'w', encoding='utf-8') as out:
        out.write(f'const {var} = [\n' + ',\n'.join(json.dumps(x, ensure_ascii=False) for x in rows) + '\n];\n')


dump('problems.js', 'PROBLEMS', items)
dump('knowledge.js', 'KNOWLEDGE', kb)
print(len(items), 'problems,', len(kb), 'knowledge points')
