import hashlib
import hmac
import base64
import time


def main(args):

    access_key = 'OR8bqh3Uq9ry8kAl1Mki'
    access_secret = 'ioDoclpl6g2aTyGfbPCnCf63sfSbDwtOomWFOPqH'

    timestamp = int(time.time() * 1000)
    timestamp = str(timestamp)

    access_secret_bytes = bytes(access_secret, 'UTF-8')

    method = "GET"
    ep_path = "/server/v2/getBlockStorageInstanceList?responseFormatType=json"

    message = method + " " + ep_path + "\n" + timestamp + "\n" + access_key

    print(message)

    message = bytes(message, 'UTF-8')
    signing_key = base64.b64encode(
        hmac.new(access_secret_bytes, message, digestmod=hashlib.sha256).digest())

    print(signing_key)

    return signing_key


if __name__ == '__main__':
    main(None)
