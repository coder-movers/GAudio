import base64
import json
import sys
import requests


def audio_request(model, path, appkey, token):
    payload = json.dumps({"model": model})
    with open(path, "rb") as f:
        data = f.read()
        data = base64.b64encode(data).decode('utf-8')
    return {
        "appkey": appkey,
        "token": token,
        "namespace": "MusicSourceSeparate",
        "payload": payload,
        "data": data
    }


def send_post(params):
    try:
        resp = requests.post("https://sami.bytedance.com/api/v1/invoke", json=params)
        resp.raise_for_status()
        sami_resp = resp.json()
    except requests.exceptions.RequestException as e:
        print(e)
        sys.exit(1)

    print(sami_resp)

    if "data" in sami_resp and len(sami_resp["data"]) > 0:
        data = base64.b64decode(sami_resp["data"])
        with open("output/output.wav", "wb") as f:
            f.write(data)
