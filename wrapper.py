from flask import Flask, request
import os
import requests

app = Flask(__name__)

api_url = os.environ.get("NTFY_API", "http://example.com/")

def keyExtractor(keys: list, data: dict):
    """get a list of keys of one neted key pair and return its value
        like: ["foo", "bar", "baz"], the dict of this is like:
        {
            "foo": {
                "bar":
                    "baz"
            }
        }
        """

    if not keys:
        return data

    key = keys[0]

    if isinstance(data, dict) and key in data:
        return keyExtractor(keys[1:], data[key])

    elif isinstance(data, list):
        tmp = []
        for item in data:
            result = keyExtractor(keys, item)
            if result is not None:
                tmp.append(result)
        return tmp if tmp else None

    else:
        return None

@app.route('/<path:path>', methods=["POST", "PUT"])
def catch_all(path):
    if request.headers.get("Content-Type") == "application/json":
        res = requests.post(url=os.path.join(api_url, path), data=request.get_json()) #TODO: use keyExtractor
        print(keyExtractor(["alerts", "status"], request.get_json()))
        print(res.status_code, path) if os.environ.get("DEBUG") == 'true' else ... 
        return [res.status_code, os.path.join(api_url, path)]
    else:
        return "content type should be json and you should send json data\n"

if __name__ == '__main__':
    app.run()
