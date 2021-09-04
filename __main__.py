import json
from api_sender import APISender
from base_auth_info import BaseAuthInfo

def main(args):

    #start_server("6645579")
    #stop_server("6645579")
    #storage_snapshot("7956620")
    server_snap_shot()

    return {"result": ""}

def start_server(server_instance_id):

    base_auth_info = BaseAuthInfo()

    req_path = '/vserver/v2/startServerInstances?serverInstanceNoList.1={0}&responseFormatType=json'. \
        format(server_instance_id)
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()

    rescode = response.status_code

    if rescode == 200:
        print(response.text)
    else:
        print("Error : " + response.text)


def delete_server(server_instance_id):

    base_auth_info = BaseAuthInfo()

    req_path = '/vserver/v2/terminateServerInstances?serverInstanceNoList.1={0}&responseFormatType=json'. \
        format(server_instance_id)
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()

    rescode = response.status_code

    if rescode == 200:
        print(response.text)
    else:
        print("Error : " + response.text)


def stop_server(server_instance_id):

    base_auth_info = BaseAuthInfo()

    req_path = '/vserver/v2/stopServerInstances?serverInstanceNoList.1={0}&responseFormatType=json'. \
        format(server_instance_id)
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()

    rescode = response.status_code

    if rescode == 200:
        print(response.text)
    else:
        print("Error : " + response.text)



def storage_snapshot(instance_id):

    base_auth_info = BaseAuthInfo()

    req_path = '/vserver/v2/createBlockStorageSnapshotInstance?originalBlockStorageInstanceNo={0}&responseFormatType=json'. \
        format(instance_id)
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()

    rescode = response.status_code

    if rescode == 200:
        print(response.text)
    else:
        print("Error : " + response.text)


def server_snap_shot():
    # 전체 Block Storage 정보
    bs_list = block_storage_list()

    data = json.loads(bs_list, encoding="utf-8")

    block_storage_instance_list = data["getBlockStorageInstanceListResponse"]["blockStorageInstanceList"]

    for item in block_storage_instance_list:
        instance_id = item['serverInstanceNo']

        print("########## "+instance_id)

        # 서버상태 확인
        instance_info = server_instance_list(instance_id)
        json_instance_info = json.loads(instance_info, encoding="utf-8")
        instance_item = json_instance_info["getServerInstanceListResponse"]["serverInstanceList"]

        print(instance_item)

        instance_status = instance_item[0]['serverInstanceStatusName']
        server_name = instance_item[0]['serverName']

        print("## " + server_name, instance_id, instance_status)
        #
        # # 서버상태가 복제중 상태이면 운영중 상태가 될때 까지 대기
        if instance_status == "copying":
            while True:
                instance_info = server_instance_list(instance_id)
                json_instance_info = json.loads(instance_info, encoding="utf-8")
                instance_item = json_instance_info["getServerInstanceListResponse"]["serverInstanceList"]

                instance_status = instance_item[0]['serverInstanceStatusName']

                if instance_status == "running" or instance_status == "stopped":
                    break

        # 운영중인 서버는 스냅샷 생성
        create_block_storage_snapshot(item["blockStorageInstanceNo"])


def server_instance_list(instance_no):
    base_auth_info = BaseAuthInfo()

    print(">>>>>>>>> "+instance_no)

    req_path = '/vserver/v2/getServerInstanceList?serverInstanceNoList.1='+instance_no+'&responseFormatType=json'
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()
    rescode = response.status_code

    if rescode == 200:
        print(response.text)
        instance_info = response.text
        return instance_info
    else:
        print("Error Code:" + rescode)


def block_storage_list():
    base_auth_info = BaseAuthInfo()

    req_path = '/vserver/v2/getBlockStorageInstanceList?responseFormatType=json'
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()

    rescode = response.status_code

    if rescode == 200:
        print(response.text)
        res_list = response.text

        return res_list

    else:
        print("Error Code:" + rescode)


def create_block_storage_snapshot(storage_instance_id):

    base_auth_info = BaseAuthInfo()

    req_path = '/vserver/v2/createBlockStorageSnapshotInstance?originalBlockStorageInstanceNo={0}&responseFormatType=json'.\
        format(storage_instance_id)
    base_auth_info.set_req_path(req_path)

    sender = APISender(base_auth_info)

    response = sender.request()
    rescode = response.status_code

    if rescode == 200:
        print("snapshot success")
    else:
        print("Error Code:" + response.text)



if __name__ == '__main__':
    main(None)
