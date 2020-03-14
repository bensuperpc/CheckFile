from multiprocessing.dummy import Pool as ThreadPool
import numpy as np
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
#from itertools import groupby

# or

update = False

if len(sys.argv) >= 2:
    if sys.argv[1] == '-update' or sys.argv[1] == '-u':
        update = True
    elif sys.argv[1] == '-help' or sys.argv[1] == '-h':
        print('you can add "-u" or "-update" to update json')
    else:
        print('Commande inconnue, please use "-h" or "-update" to display help')


def checkfile(fname, mode='sha3_512'):
    #md5 = hashlib.md5()
    #sha1 = hashlib.sha1()
    #h = hashlib.new(mode)
    h = hashlib.sha3_512()
    with open(fname, 'rb') as file:
        block = file.read(1024)
        while block:
            h.update(block)
            block = file.read(1024)
    return h.hexdigest()


def my_function(_file):
    if os.path.exists(_file):
        return (_file, checkfile(_file))
    else:
        return (_file, 'null')


path = pathlib.Path(__file__).parent.absolute()
files = []


start = time.process_time()
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    #thread_wraper(r, d, f)
    for file in f:
        files.append(os.path.relpath(os.path.join(r, file), path))

pool = ThreadPool(24)
pool = mp.Pool(processes=24)
res = pool.map(my_function, files)

print('Time:', time.process_time() - start)

#res.sort(key=lambda tup: tup[0])

res = filter(lambda x: x[0] != 'data.json', res)
res = filter(lambda x: x[1] != 'null', res)
res = filter(lambda x: x[0] != os.path.basename(__file__), res)
res = list(res)

print(len(res), 'files founds')

params = {}
params = {'Checker': {"params": {"check": "sha3_512", "multiprocessing": "True"},
                      'files': [{'file': x, 'check': y} for x, y in res]}}

if not os.path.isfile('data.json') or update == True:
    print('Create or update')
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(params, f, ensure_ascii=False, sort_keys=True, indent=4)


json_data = []

with open('data.json', 'r') as json_file:
    data = json.load(json_file)
    data = data['Checker']

    for p in data['files']:
        json_data.append((p['file'], p['check']))

#res = [i for i in res if not i[0] == os.path.basename(__file__)]

json_data = filter(lambda x: x[0] != 'data.json', json_data)
json_data = filter(lambda x: x[0] != os.path.basename(__file__), json_data)
json_data = list(json_data)

start = time.process_time()

'''
res_clean = res.copy()
for i in range(0, len(json_data)):
    if json_data[i] in res_clean:
        res_clean.remove(json_data[i])
'''

res_clean = set(res) - set(json_data)
json_data_clean = set(json_data) - set(res)

print('Current dir:', len(res_clean), 'Files changed or removed')
print('In JSON:', len(json_data_clean), 'Files changed or removed')

print('Time:', time.process_time() - start)
