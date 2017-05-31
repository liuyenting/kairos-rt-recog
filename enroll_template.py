import os
import requests
import base64
import json

dataDir = 'template'

url = 'https://api.kairos.com/enroll';
appId = '420de94a';
appKey = 'bb9d4e85c8acbb16de74654e4a9c009a';

headers = {
    'Content-Type': 'application/json',
    'app_id': appId,
    'app_key': appKey
}

# list files in current directory
for f in os.listdir(dataDir):
    if f.endswith('.png'):
        path = os.path.join(dataDir, f)
        print(path)

        # name
        fname, fext = os.path.splitext(path)
        name = os.path.basename(fname)
        # remove illegal character
        name = name.replace('_', '-')

        # dump file as base64 string
        with open(path, 'rb') as f:
            imstr = base64.b64encode(f.read())

        # generate the post fields
        values = {
            'image': 'data:image/png;base64,' + imstr,
            'subject_id': name,
            'gallery_name': 'AKB48'
        }

        # send the request
        response = requests.post(url, headers=headers, json=values)

        # convert to json string
        result = json.dumps(json.loads(response.text), indent=3)
        # print result
        print result + '\n'
