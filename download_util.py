import requests as req
from Settings import *
def aria2_download(aria2_body):
    aria2_api = ARIA2_RPC_URL
    resp = req.post(aria2_api, json=aria2_body)
    print(resp.text)
    print(resp.status_code)


def build_post_body(res_url, base_dir):
    illust_id = ""
    if res_url.find("ugoira") == -1:
        illust_id = res_url.split("/")[-1].split("_p")[0]
    else:
        illust_id = res_url.split("/")[-1].split("_ugoira")[0]
    return {
        "id": None,
        "jsonrpc": 2.0,
        "method": "aria2.addUri",
        "params": [
            [
                res_url
            ],
            {
                "header": [
                    "referer: https://www.pixiv.net/"
                ],
                "dir":"{}/{}".format(base_dir,illust_id)
            }
        ]
    }
def download_directly(url, base_dir):
    aria2_body = build_post_body(url, base_dir)
    aria2_download(aria2_body)