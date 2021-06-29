#!/usr/bin/python3
import ssl
import datetime
import socket
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--urls', nargs='+', dest='urls', type=str)
args = parser.parse_args()
tt = datetime.datetime.now()


def ssl_expiry_datetime(host, tt, port=443):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=host,
    )
    # 3 second timeout because Lambda has runtime limitations
    conn.settimeout(3.0)
    try:
        conn.connect((host, port))
        ssl_info = conn.getpeercert()
        # parse the string from the certificate into a Python datetime object
        res = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        expiry = (res - tt).days
    except Exception as e:
        res = e
        expiry = '100'
    return res, expiry


zabbixurls = '{\n"data":[\n'
for url in args.urls:
    try:
        check = ssl_expiry_datetime(url, tt)
    except Exception as e:
        check = e
    zabbixurls += '{\n"URL": "' + url + '", ' + '\n"EXDATE": "' + str(check[0]).split(' ')[
        0] + '",' + '\n"EXPIRY": ' + str(check[1]) + '\n},'
zabbixurls = zabbixurls[:-1]
zabbixurls += '\n]\n}'
print(zabbixurls)
