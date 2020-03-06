import util
import requests
import json
import time
#BASE_URL = "http://127.0.0.1:8000/"
BASE_URL = "https://devodsy.dynamyn.com/"
true = True
false = False
null = None

def test_api():
    full_payload =  {
	"checksum":"0",
	"imei1":"911655450002265","imei2":"362523432430703","device_type":"smartphone","model_name":"itel L5503","brand_name":"Itel","latitude":"null","longitude":"null","gaid":"null","mnc":"null","mcc":"23xyz","device_id":"731907db986ad9af","app_package_name":"com.datacultr.odyssey","app_version_name":"6.1.9.3","app_version_code":74,"suspicious_activity":"null","last_performed_activity":"{\"modified\":1579503003018,\"actions\":[{\"type\":\"knox\",\"action_tags\":[{\"action\":\"AB\",\"status\":\"unlock\",\"packages\":[\"com.datacultr.odyssey\",\"com.google.android.apps.photos\",\"com.samsung.android.messaging\",\"com.snapchat.android\",\"com.android.vending\",\"com.instagram.android\",\"com.Obhai.driver\",\"com.android.dialer\"]},{\"action\":\"DF\",\"status\":false},{\"action\":\"DAL\",\"status\":true}]}]}","actor_theme_change_status":false,"pwd_data_modified_status":false
    }

    syncing_payload =  {
	"checksum":"43E04950AA4959A0",
	"imei1":"911655450002265"
    }
    payload = full_payload
    while True:
        dict_response = sendToServer(payload)
        if dict_response['_hash_'] != full_payload['checksum']:
            full_payload['checksum'] = dict_response['_hash_']
            syncing_payload['checksum'] = dict_response['_hash_']
            payload = full_payload
            print("\n\n----device got new data----\n\n")
            if dict_response['data']['actor_theme_change_status']:
                print("actor_theme_change_status is True here\n sending true in response")
                full_payload['actor_theme_change_status'] = true
        else:
            if 'data' in dict_response.keys():
                if dict_response['data']['actor_theme_change_status']:
                    full_payload['actor_theme_change_status'] = true
                    payload = full_payload
                else:
                    payload = syncing_payload
            else:
                payload = syncing_payload
            print("\n\n----device is in sync with server----\n\n")
        time.sleep(10)


def sendToServer(dic_payload):
    url = BASE_URL + "api/dem/device_sync_view/"
    payload = encrypt(json.dumps(dic_payload)).decode("utf-8")
    print("length of payload",len(payload))
    print("request from device is:",dic_payload)
    payload = "{\"key\":\"%s\"}" % payload
    #print("after encryption data is:",payload)

    headers = {
        'Content-Type': "application/json",
	'sdk-token':"bb0261c4ec75463f8713bf570fe9c348"
    }
    res = requests.post(url, data=payload, headers=headers)
    print(res.status_code)
    print(res.text)
    #decode here
    res_dic = dict(eval(res.text))['response']
    dict_resp = decrypt(res_dic).decode("utf-8")
    dict_resp = dict(eval(dict_resp))
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#")
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*",dic_payload['checksum']," *~*~*~*~*~*~*~*~*~*~*~#")
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*",dict_resp['_hash_']," *~*~*~*~*~*~*~*~*~*~*~#")
    print("#*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~#")
    print("response from server is:",dict_resp)
    return dict_resp

def encrypt(str):
    return util.encrypt(str,util.dem_client_secret)

def decrypt(str):
    return util.decrypt(str,util.dem_client_secret)

test_api()
