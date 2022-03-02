#!/usr/bin/env python3

from dictdlib import DictReader
import re
import sys

if not len(sys.argv) == 3:
    print(f"Usage: {sys.argv[0]} <path to dict without extension> <path to dsl>")
    sys.exit(-1)

dict = sys.argv[1]
outfile = sys.argv[2]

reader = DictReader(dict)
deflist = reader.getdeflist()

out = open(outfile, 'w+')

out.write('\ufeff')

# CHANGE THESE
out.write("""#NAME "German - English Ding/FreeDict dictionary"
#INDEX_LANGUAGE "German"
#CONTENTS_LANGUAGE "English"

""")

def split_pos(val):
    parts = val.group(1).split(',')
    result = ''
    for part in parts:
        result += f'[p][i]{part}[/i][/p] '
    return result

count = 0
for key in deflist:
    count += 1
    print(f"Adding entry {count}...", end='\r')
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
