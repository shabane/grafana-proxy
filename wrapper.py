from flask import Flask, request
import os
import requests

app = Flask(__name__)

api_url = os.environ.get("NTFY_API", "http://example.com/")

@app.route('/<path:path>', methods=["POST", "PUT"])
def catch_all(path):
    if request.headers.get("Content-Type") == "application/json":
        res = requests.post(url=os.path.join(api_url, path), data=request.get_json())
        print(res.status_code, path) if os.environ.get("DEBUG") == 'true' else ... 
        return [res.status_code, os.path.join(api_url, path)]
    else:
        return "content type should be json and you should send json data\n"

if __name__ == '__main__':
    app.run()
