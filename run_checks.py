from activitypy.jsonld import CachedRequestsJsonLoader
from activitypy.jsonld import ApplicationActivityJson
from pyld import jsonld
import os
import logging
logging.basicConfig(level=logging.CRITICAL)
jsonld.get_document_loader().secure = False
all_files = list(os.walk('sample_data'))
files = all_files[0][2]
test_files = [f for f in files if os.path.isfile(os.path.join('sample_data', f)) and '.json' in f and f != 'package.json']
failures = []
for file in test_files:
    with open(os.path.join('sample_data', file), 'r') as reader:
        try:
            obj = ApplicationActivityJson.from_json(reader.read())
        except Exception as e:
            failures.append((file, e))
print('\n'.join(f'{f} : {e}' for f, e in failures))