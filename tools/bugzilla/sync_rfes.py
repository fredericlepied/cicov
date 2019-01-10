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
import time

import bugzilla


r = requests.get('http://localhost:8000/api/view/get_rfes/OSP15')
cicov_rfes = {}

data = json.loads(r.text)
print("%d RFEs in cicov" % len(data))

for rfe in data:
    cicov_rfes[rfe['url']] = rfe

URL = "bugzilla.redhat.com"

bzapi = bugzilla.Bugzilla(URL)

query = bzapi.build_query(product="RedHat OpenStack", savedsearch="osp15rfe")

# query() is what actually performs the query. it's a wrapper around Bug.search
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
        r = requests.post('http://localhost:8000/api/rfes',
                          {'url': url,
                           'name': rfe.summary,
                           'product': 8,
                           'tests': []
                           })

for url in cicov_rfes:
    if url not in bz_rfes:
        print("%s do not exist anymore: %s" % (url, cicov_rfes[url]["name"]))
        r = requests.delete('http://localhost:8000/api/rfes/%d' %
                            cicov_rfes[url]["id"])

# sync_rfes.py ends here
