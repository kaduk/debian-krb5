#!/usr/bin/python
from k5test import *

realm = K5Realm(start_kadmind=False, create_host=False)
output = realm.run_as_client([kvno, 'krbtgt/'], expected_code=1)
if 'not found in Kerberos database' not in output:
    fail('TGT lookup for empty realm failed in unexpected way')
success('Empty tgt lookup.')
