import os
import requests
import base64
import json

dataDir = 'test_set'

url = 'https://api.kairos.com/recognize';
appId = '420de94a';
appKey = 'bb9d4e85c8acbb16de74654e4a9c009a';

headers = {
    'Content-Type': 'application/json',
    'app_id': appId,
    'app_key': appKey
}

# list files in current directory
for f in os.listdir(dataDir):
    if f.endswith('.jpeg'):
        path = os.path.join(dataDir, f)
        print(path)

        # dump file as base64 string
        with open(path, 'rb') as f:
            imstr = base64.b64encode(f.read())

        # generate the post fields
        values = {
            'image': 'data:image/png;base64,' + imstr,
            'gallery_name': 'AKB48'
        }

        # send the request
        response = requests.post(url, headers=headers, json=values)

        # convert to json string
        result = json.dumps(json.loads(response.text), indent=3)
        # print result
        print result + '\n'
