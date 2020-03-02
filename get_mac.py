import nmap
import sys
import os


def get_mac_from_ips():
    ip_cam = []
    try:
        r = os.popen('arp -e')
        text = r.read()
        r.close()
        for line in text.splitlines():
            line = line.split()[:3]
            # print(line)
            if ('192.168.' in line[0]) and (line[2].find(':') > 0):
                    if line[2].split(':')[0] == 'e0':
                        ip_cam.append(line[0])

    except Exception as e:
        print(e)

    return ip_cam


def nmap_ping_scan(network_prefix):
    try:
        # 创建一个扫描实例
        nm = nmap.PortScanner()
        # 配置nmap参数
        ping_scan_result = nm.scan(hosts=network_prefix, arguments='-v -n -sn')
        host_list = []
        for result in ping_scan_result['scan'].values():
            if result['status']['state'] == 'up':
                host_list.append(result['addresses']['ipv4'])
        return get_mac_from_ips()

    except Exception as e:
        print(e)

    return None


def get_mac(test_model=False):
    if test_model:
        # test on another network
        return nmap_ping_scan('192.168.0.0/24')
    else:
        return nmap_ping_scan('192.168.10.0/24')

 
if __name__ == '__main__':
    print(get_mac())
    pass