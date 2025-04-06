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

def sendNtfy(template: str, url: str) -> int:
    res = requests.post(url, data=template)
    return res.status_code

@app.route('/<path:path>', methods=["POST", "PUT"])
def catch_all(path):
    if request.headers.get("Content-Type") == "application/json":
        jdata = request.get_json()

        st = keyExtractor("alerts.status".split("."), jdata) or ['EMPTY']
        al = keyExtractor("alerts.labels.alertname".split("."), jdata) or ['EMPTY']
        qu = keyExtractor("alerts.labels.queue".split("."), jdata) or ['EMPTY']
        sa = keyExtractor("alerts.startsAt".split("."), jdata) or ['EMPTY']
        de = keyExtractor("alerts.annotations.description".split("."), jdata) or ['EMPTY']
        su = keyExtractor("alerts.annotations.summary".split("."), jdata) or ['EMPTY']

        for _st, _al, _qu, _sa, _de, _su in zip(st, al, qu, sa, de, su):
            template = f"""
                {_st}

                {_al}

                {_qu}

                {_sa}

                {_de}

                {_su}
            """
            res = sendNtfy(template, os.path.join(api_url, path))
            print(res, path) if os.environ.get("DEBUG") == 'true' else ... 
            return [res, os.path.join(api_url, path)]
        else:
            return "content type should be json and you should send json data\n"

if __name__ == '__main__':
    app.run()
