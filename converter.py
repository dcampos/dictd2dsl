#!/usr/bin/env python3

from dictdlib import DictReader
import orjson as json
import re

reader = DictReader('deu-eng')
deflist = reader.getdeflist()

out = open('/opt/GoldenDict/freedict/deu-eng/deu-eng.dsl', 'w+')

out.write('\ufeff')

out.write("""#NAME "German - English Ding/FreeDict dictionary"
#INDEX_LANGUAGE "German"
#CONTENTS_LANGUAGE "English"

""")

def split_pos(val):
    # r'[p][i]\1[/i][/p]'
    parts = val.group(1).split(',')
    result = ''
    for part in parts:
        result += f'[p][i]{part}[/i][/p] '
    return result

# with open('deu-eng-fixed.json', 'r+') as file:
count = 0
for key in deflist:
    count += 1
    print(f"Adding entry {count}...", end='\r')
    # data = json.loads(line)
    # key = list(data.keys())[0]
    for value in reader.getdef(key):
        key = re.sub(r'^ +', '', key)
        out.write(key + '\n')
        defs = value.splitlines()
        result = []
        r = defs[0].decode('utf-8')
        r = re.sub(r'([\[\@\]])', r'\\\1', r)
        r = re.sub(r'^(.*?) (/.*?/)', r'\t[m1][b]\1[/b] \2', r)
        r = re.sub(r'<(.*?)>', split_pos, r)
        result.append(r)
        for d in defs[1:]:
            d = d.decode('utf-8')
            if d == '':
                continue
            d = re.sub(r'\[(.*?)\]', r'[c darkred]\\[\1\\][/c]', d)
            d = re.sub(r'([\@])', r'\\\1', d)
            d = re.sub(r'^(\s+)(Note):', r'\1[i][p]\2[/p][/i]:', d)
            d = re.sub(r'^(\s+)(Synonym):', r'\1[i][p]Syn[/p][/i]:', d)
            d = re.sub(r'^(\s+)(see:)', r'\1⇨', d)
            d = re.sub(r'^(\s+)"(.*?)" \s*-\s* (.*)', r'\1[ex][i]\2[/i] - \3[/ex]', d)
            if not d.startswith(' '):
                d = '\t[m2]' + d
            else:
                d = re.sub(r'^\s+', '\t[m3]', d)
            d = re.sub(r'<(.*?)>', r'[p][i]\1[/i][/p]', d)
            d = re.sub(r'{(.*?)}', r'<<\1>>', d)
            result.append(d)
        out.write('\n'.join(result))
        out.write('\n\n')
