from multiprocessing.dummy import Pool as ThreadPool
import time
import multiprocessing as mp

from pathlib import Path
import pathlib
import sys
import time
import os
import sys
import hashlib

import json

update = False

if len(sys.argv) >= 2:
    if sys.argv[1] == '-update' or sys.argv[1] == '-u':
        update = True
    elif sys.argv[1] == '-help' or sys.argv[1] == '-h':
        print('you can add "-u" or "-update" to update json')
    else:
        print('Commande inconnue, please use "-h" or "-update" to display help')

def clean(_file):
    _file = filter(lambda x: x[0] != 'data.json', _file)
    _file = filter(lambda x: x[1] != 'null', _file)
    _file = filter(lambda x: x[0] != os.path.basename(__file__), _file)
    return _file

def checkfile(fname, mode='sha3_512'):
    h = hashlib.new(mode)
    #h = hashlib.sha3_512()
    with open(fname, 'rb') as file:
        block = file.read(1024)
        while block:
            h.update(block)
            block = file.read(1024)
    return h.hexdigest()


def file_exist(_file):
    if os.path.exists(_file):
        return (_file, checkfile(_file))
    else:
        return (_file, 'null')


path = pathlib.Path(__file__).parent.absolute()
files = []


start = time.process_time()

for path in Path('.').rglob('*'):
    if path.is_file():
        files.append(str(path))

pool = ThreadPool(24)
pool = mp.Pool(processes=24)
res = pool.map(file_exist, files)

print('Time:', time.process_time() - start)

res = clean(res)
res = list(res)

print(len(res), 'files founds')

params = {'Checker': {"params": {"hash": "sha3_512", "multiprocessing": "True"},
                      'files': [{'file': x, 'hash': y} for x, y in res]}}

if not os.path.isfile('data.json') or update == True:
    print('Create or update: data.json')
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(params, f, ensure_ascii=False, sort_keys=True, indent=4)


json_data = []

with open('data.json', 'r') as json_file:
    data = json.load(json_file)
    data = data['Checker']

    for p in data['files']:
        json_data.append((p['file'], p['hash']))

json_data = clean(json_data)
json_data = list(json_data)

start = time.process_time()

res_clean = set(res) - set(json_data)
json_data_clean = set(json_data) - set(res)

print('Current dir:', len(res_clean), 'Files changed or removed')
print('In JSON:', len(json_data_clean), 'Files changed or removed')

if (len(res_clean) > 0):
    print('Update or add file in directory:')
    for w,e in res_clean:
        print(f"{w}\t{e}")

if (len(json_data_clean) > 0):
    print('Update or add file in JSON:')
    for w,e in json_data_clean:
        print(f"{w}\t{e}")
    #print(list(json_data_clean))

print('Time:', time.process_time() - start)
