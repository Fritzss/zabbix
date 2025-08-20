#!/usr/bin/python3
import ssl
import datetime
import socket
import argparse
import json

def ssl_expiry_datetime(host, port=443):
    ssl_date_fmt = r'%b %d %H:%M:%S %Y %Z'
    context = ssl.create_default_context()
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    conn = context.wrap_socket(
        socket.socket(socket.AF_INET),
        server_hostname=host,
    )
    conn.settimeout(3.0)
    try:
        conn.connect((host, port))
        ssl_info = conn.getpeercert()
        expiry_date = datetime.datetime.strptime(ssl_info['notAfter'], ssl_date_fmt)
        expiry_days = (expiry_date - datetime.datetime.now()).days
        return expiry_date, expiry_days
    except Exception as e:
        return None, str(e)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--urls', nargs='+', required=True, help="Список URLs для проверки")
    args = parser.parse_args()
    
    results = []
    for url in args.urls:
        expiry_date, expiry_days = ssl_expiry_datetime(url)
        result = {
            "URL": url,
            "EXDATE": expiry_date.strftime("%Y-%m-%d") if expiry_date else "ERROR",
            "EXPIRY": expiry_days if isinstance(expiry_days, int) else -1  # -1 для ошибок
        }
        results.append(result)
    
    print(json.dumps({"data": results}, indent=2))

if __name__ == "__main__":
    main()
