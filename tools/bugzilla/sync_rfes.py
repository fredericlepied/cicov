#!/usr/bin/env python3
#
# Copyright (C) 2019 Red Hat, Inc. 
#
# Author: Frederic Lepied <frederic.lepied@redhat.com>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

'''
'''

import json
import requests
import sys
import time

import bugzilla

CICOV_URL = 'http://localhost:8000/api'

if len(sys.argv) != 3:
    print('Usage: %s <product name> <bz saved search>' % sys.argv[0],
          file=sys.stderr)
    sys.exit(1)

product_name = sys.argv[1]
bz_savedsearch = sys.argv[2]

r = requests.get(CICOV_URL + '/products')
data = json.loads(r.text)

for dat in data:
    if dat['name'] == product_name:
        product = dat
        break
else:
    print('Unable to find %s on CICOV (%s)' % (product_name, CICOV_URL),
          file=sys.stderr)
    sys.exit(2)

r = requests.get(CICOV_URL + '/view/get_rfes/%s' % product_name)
cicov_rfes = {}

data = json.loads(r.text)
print("%d RFEs in cicov" % len(data))

for rfe in data:
    cicov_rfes[rfe['url']] = rfe

URL = "bugzilla.redhat.com"

bzapi = bugzilla.Bugzilla(URL)

query = bzapi.build_query(savedsearch=bz_savedsearch)

t1 = time.time()
rfes = bzapi.query(query)
t2 = time.time()
print("Found %d RFEs in bugzilla" % len(rfes))
print("Query processing time: %.2fs" % (t2 - t1))

bz_rfes = {}
for rfe in rfes:
    url = "https://bugzilla.redhat.com/show_bug.cgi?id=%d" % rfe.id
    bz_rfes[url] = rfe
    if url not in cicov_rfes:
        print("%s need to be created: %s" % (url, rfe.summary))
        r = requests.post(CICOV_URL + '/rfes',
                          {'url': url,
                           'name': rfe.summary,
                           'product': product['id'],
                           'tests': []
                           })
    elif rfe.summary != cicov_rfes[url]['name']:
        print('Updating %s: %s' % (rfe.id, rfe.summary))
        r = requests.patch(CICOV_URL + '/rfes/%d' % cicov_rfes[url]['id'],
                           {'name': rfe.summary})

for url in cicov_rfes:
    if url not in bz_rfes:
        print("%s do not exist anymore: %s" % (url, cicov_rfes[url]["name"]))
        r = requests.delete(CICOV_URL + '/rfes/%d' % cicov_rfes[url]["id"])

# sync_rfes.py ends here
