import json
from api_sender import APISender
from base_auth_info import BaseAuthInfo


def main(args):

    # 전체 Block Storage 정보
    bs_list = block_storage_list()

    data = json.loads(bs_list.decode('utf-8'))

    block_storage_instance_list = data["getBlockStorageInstanceListResponse"]["blockStorageInstanceList"]

    for item in block_storage_instance_list:
        instance_id = item['serverInstanceNo']

        # 서버상태 확인
        instance_info = server_instance_list(instance_id)
        json_instance_info = json.loads(instance_info.decode('utf-8'))
        instance_item = json_instance_info["getServerInstanceListResponse"]["serverInstanceList"]

        instance_status = instance_item[0]['serverInstanceStatusName']
        server_name = instance_item[0]['serverName']

        print("## " + server_name, instance_id, instance_status)

        # 서버상태가 복제중 상태이면 운영중 상태가 될때 까지 대기
        if instance_status == "copying":
            while True:
                instance_info = server_instance_list(instance_id)
                json_instance_info = json.loads(instance_info.decode('utf-8'))
                instance_item = json_instance_info["getServerInstanceListResponse"]["serverInstanceList"]

                instance_status = instance_item[0]['serverInstanceStatusName']

                if instance_status == "running" or instance_status == "stopped":
                   break

        # 운영중인 서버는 스냅샷 생성
        create_block_storage_snapshot(item["blockStorageInstanceNo"])

    return {"result": ""}


def server_instance_list(instance_no):
    base_auth_info = BaseAuthInfo()

    req_path = '/server/v2/getServerInstanceList?serverInstanceNoList.1='+instance_no+'&responseFormatType=json'
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()

    if response.getcode() == 200:
        res_list = response.read()

        return res_list
    else:
        print("" + response)


def block_storage_list():
    base_auth_info = BaseAuthInfo()

    req_path = '/server/v2/getBlockStorageInstanceList?responseFormatType=json'
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()

    if response.getcode() == 200:
        res_list = response.read()

        return res_list
    else:
        print("" + response)


def create_block_storage_snapshot(storage_instance_id):

    base_auth_info = BaseAuthInfo()

    req_path = '/server/v2/createBlockStorageSnapshotInstance?blockStorageInstanceNo={0}&responseFormatType=json'.\
        format(storage_instance_id)
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()

    if response.getcode() == 200:
        print(">> snapshot success : " + storage_instance_id)
    else:
        print(""+response)


def create_server_image(server_instance_id):

    base_auth_info = BaseAuthInfo()

    req_path = '/server/v2/createMemberServerImage?serverInstanceNo={0}&responseFormatType=json'. \
        format(server_instance_id)
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()
    res_list = response.read()
    print(json.loads(res_list.decode('utf-8')))


if __name__ == '__main__':
    main(None)
