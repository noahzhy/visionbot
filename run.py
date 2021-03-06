import os
import requests
import json
import time
from configparser import ConfigParser


config_file = 'config.ini'
config = ConfigParser()
config.read(config_file, encoding='UTF-8')
local_version = config['update_config']['version']
domain = config['update_config']['domain']
update_file = config['update_config']['update_file']


def check_network():
    try:
        sess = requests.Session()
        url = 'http://{}/{}'.format(domain, update_file)
        r = sess.post(url=url, timeout=10)
        if r.status_code == 200:
            return True
        else:
            return False
    except Exception as e:
        return False


class Update():
    def __init__(self):
        version = local_version
        updateFile = []
        try:
            while True:
                if check_network():
                    print('network connected!')
                    break
                time.sleep(15)

            url = 'http://{}/{}'.format(domain, update_file)
            sess = requests.Session()
            r = sess.post(url=url, timeout=10)
            if r.status_code == 200:
                j = r.json()
                version = j['version']
                if len(j['updateFile']) > 0:
                    updateFile = j['updateFile']

        except Exception as e:
            print(e)

        self.version = version
        self.updateFile = updateFile

    def get_newest_version(self):
        return self.version

    def get_file_list(self):
        return self.updateFile


def download_files(file_list):
    def download_big_file(file_name):
        try:
            url = 'http://{}/{}'.format(domain, file_name)
            r = requests.get(url, stream=True)
            with open(file_name, "wb") as pdf:
                for chunk in r.iter_content(chunk_size=1024):
                    if chunk:
                        pdf.write(chunk)
            return True
        except Exception as e:
            print(e)
            return False

    file_counter = 0

    for i in file_list:
        if download_big_file(i):
            file_counter += 1
            print(i, 'downloaded')

    return True if file_counter == len(file_list) else False


def run():
    file_list = update_json.get_file_list()

    if download_files(file_list):
        config = ConfigParser()
        config.read(config_file)
        config.set('update_config', 'version', update_json.get_newest_version())
        with open(config_file, 'w') as cf:
            config.write(cf)


if __name__ == "__main__":
    update_json = Update()
    newest_version = update_json.get_newest_version()

    if local_version < newest_version:
        run()

    os.system('python3 main.py')

    # print(check_network())