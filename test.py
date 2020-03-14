from multiprocessing.dummy import Pool as ThreadPool
#import numpy as np
import time
import multiprocessing as mp

from pathlib import Path
import pathlib
import sys
import time
import os
import hashlib

import json
from itertools import groupby

BUF_SIZE = 65536


def checkfile(fname, checker=hashlib.sha3_512()):
    md5 = hashlib.md5()
    sha1 = hashlib.sha1()
    with open(fname, 'rb') as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            checker.update(data)
    return checker.hexdigest()


def my_function(_file):
    parse = [_file, checkfile(_file)]
    return parse


path = pathlib.Path(__file__).parent.absolute()
files = []


start = time.process_time()
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    #thread_wraper(r, d, f)
    for file in f:
        files.append(os.path.relpath(os.path.join(r, file), path))

pool = ThreadPool(32)
pool = mp.Pool(processes=32)
res = pool.map(my_function, files)
print('Time:', time.process_time() - start)

#res.sort(key=lambda tup: tup[0])

print(len(res), 'files founds')


params = {}
#params['Checker'] = {"params": {"check": "sha3_512", "multiprocessing": "True"}, 'files' : [{'file':x,'check':y} for x,y in res]}
params = {'Checker': {"params": {"check": "sha3_512", "multiprocessing": "True"},
                      'files': [{'file': x, 'check': y} for x, y in res]}}

if not os.path.isfile('data.json'):
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(params, f, ensure_ascii=False, sort_keys=True, indent=4)


save_files = []

with open('data.json', 'r') as json_file:
    data = json.load(json_file)
    data = data['Checker']

    for p in data['files']:
        save_files.append([p['file'], p['check']])

#for x in 

#save_files.sort(key=lambda tup: tup[0])

