import os
import requests
import time
import json
import get_mark as gm


server = "rest.sotongbox.com"
headers = {'Content-Type': 'application/json'}
bearer_global = ''

def login(id="falluser", pw="skrtkd1234!"):
    sess = requests.Session()
    try:
        url = "http://{}/api/login".format(server)
        d = {
            "domain": "Company1",
            "userId": str(id),
            "password": str(pw)
        }
        r = sess.post(url, headers=headers, data=json.dumps(d))
        return r.text
    except Exception as e:
        print(e)
        return 000

def upload(path_to_file):
    global bearer_global
    if os.path.exists(path_to_file):
        print('file checked')
        try:
            sess = requests.Session()
            if (bearer_global == ''):
                bearer_global = login()
            # pass
            url = "http://{}/api/fall-events/upload".format(server)
            h = {"Authorization": str(bearer_global)}
            d = {
                'file': ('video.mp4', open(path_to_file, 'rb'), 'video/mp4'),
                'deviceSN': (None, "fall_"+str(gm.get_name())),
                'isActive': (None, 'true')                    
            }
            r = sess.post(url, headers=h, files=d)
            # print(r.request.body)
            print('>>>>>', r.status_code)
            return r.status_code
        except Exception as e:
            print('Error:', e)
            return 000

    # bearer_global = login()
    # upload_video(bearer_global)
    # return 000


def error_report(error_code=0):
    global bearer_global
    try:
        if (bearer_global == ''):
            bearer_global = login()
        
        sess = requests.Session()
        url = "http://{}/api/fall-cameras".format(server)
        h = {
            # 'Content-Type': 'multipart/form-data',
            # 'Value': 'multipart/form-data',
            'Content-Type': 'application/json',
            "Authorization": str(bearer_global)
        }
        d = {
            # 'deviceSN': 'speaker_2057_1',
            "deviceSN" : "fall_"+str(gm.get_name()),
            "isActive" : 'false'
        }

        r = sess.post(url, headers=h, data=json.dumps(d))
        # print(d)
        print(r.text)
        return r.status_code
    except Exception as e:
        print(e)
        return 000


def online_report():
    global bearer_global
    try:
        if (bearer_global == ''):
            bearer_global = login()
        
        sess = requests.Session()
        url = "http://{}/api/fall-cameras".format(server)
        h = {
            # 'Content-Type': 'multipart/form-data',
            # 'Value': 'multipart/form-data',
            'Content-Type': 'application/json',
            "Authorization": str(bearer_global)
        }
        d = {
            # 'deviceSN': 'speaker_2057_1',
            "deviceSN" : "fall_"+str(gm.get_name()),
            "isActive" : 'true'
        }

        r = sess.post(url, headers=h, data=json.dumps(d))
        # print(d)
        print(r.text)
        return r.status_code
    except Exception as e:
        print(e)
        return 000


if __name__ == "__main__":
    # main('video_004.mp4')
    # path_to_file = r'E:\FD-Nano\video_004.mp4'
    # print(str(gm.get_name()))
    # print(login("falluser", "skrtkd1234!"))
    # upload(path_to_file)
    # print(error_report())
    # print(online_report())
    pass