import requests
import urllib.parse
import datetime

from fake_useragent import UserAgent

from db import Database



class YouGov():
    def __init__(self, account_id):

        # SETTINGS
        self.DOMAIN = "https://sink.safe.yougov.com"
        self.VERIFY_SSL = True
        # MORE SETTINGS
        self.LIST_PATH = "/sources/list"
        self.UPLOAD_PATH = "/sources/upload/"

        self.db = Database()
        self.AUTH_TOKEN = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyIjp7ImNvdW50cnlDb2RlIjoiR0IiLCJwYW5lbGlzdElkIjpudWxsLCJ5b3Vnb3ZQZXJzb25JZGVudGlmaWVyIjoiZW1lYToxNDYwNTgwMjYiLCJwbXhfaWQiOiIxNDc4MTU0MDIiLCJwYW5lbF9pZCI6IjEzIiwiY3VycmVuY3lDb2RlIjpudWxsLCJleHRlbnNpb25VVUlEIjoiaGtiY3BmZ2dvbmlja2NwcG1ubm5uaGNpZWpiaGxwb2QiLCJsYW5nIjoiZW4iLCJ0eXBlIjoicHJvZmlsZXMiLCJhdWQiOiJlbWVhOjE0NjA1ODAyNiJ9LCJhdWQiOiJlbWVhOjE0NjA1ODAyNiIsImlzcyI6InlnLXNhZmUtc2VydmljZXM6YXV0aDpzc28vMS42LjMiLCJpYXQiOjE2MTkwMjE2NDcsImV4cCI6MTYyNDIwNTY0N30.TTXmKiqosTIzxosJ4BffIlTDEK-f1IMNGXV0mF-XzN8'

        ua = UserAgent()
        self.USER_AGENT = str(ua.chrome)

        self.HEADERS = {
            'User-Agent': self.USER_AGENT,
            'origin': 'chrome-extension://hkbcpfggonickcppmnnnnhciejbhlpod',
            'authorization': 'Bearer ' + self.AUTH_TOKEN,
            'accept': 'application/json'
        }
        self.points = 0 # get from database
        self.IP_ADDRESS = self._get_ip_address()
        if self.ip_address_already_used(account_id):
            print("Error! This IP address has already been used by another profile! Quitting...")
            quit()
        else:
            self.log_ip_address()   
        self.session = requests.Session()

    def get_available_sources(self):
        url = self.DOMAIN + self.LIST_PATH
        r = self.session.get(url, headers=self.HEADERS, verify=self.VERIFY_SSL)
        # todo: check status
        json_r = r.json()
        sources = []
        for source in json_r["sources"]:
            source_name = source["name"]

            # If last uploaded time + interval time is less than current time, append to sources
            last_upload_string = source["lastUploaded"]
            if source["lastUploaded"] is None:
                last_upload_date = datetime.datetime.min
            else:
                last_upload_date = datetime.datetime.strptime(source["lastUploaded"] , '%Y-%m-%dT%H:%M:%S.%fZ')
            interval = int(source["interval"])
            next_upload_date = last_upload_date + datetime.timedelta(minutes=interval)
            if next_upload_date < datetime.datetime.now():
                sources.append(source_name)

        # Sync newly retrieved points
        self.update_points(int(json_r["summary"]["points"]))

        return sources

    def upload_data(self, source_name, payload):
        # POST empty data
        url = self.DOMAIN + self.UPLOAD_PATH + source_name
        r = session.post(url, json=payload, headers=self.HEADERS, verify=VERIFY_SSL)
        if r.status_code != 200:
            print("Error. Could not upload data for", source_name)
            return False

        # Update points
        points_earned = int(r.json()["points"])
        update_points(self.points + points_earned)

        return True

    def update_points(self, new_points):
        if self.points != new_points:
            with self.db as conn:
                pass
                # todo: update points in database
                # conn.execute("")#

    def log_ip_address(self):
        pass
        # todo: log self.IP_ADDRESS to database

    def ip_address_already_used(self, account_id):
        return False
        # todo: Check if already IP used by another profile

    def _get_ip_address(self):
        r = requests.get('https://checkip.amazonaws.com')
        ip = r.text.strip()
        if r.status_code != 200 or not self._validate_ipv4(ip):
            # fallback
            r = requests.get('https://api.ipify.org')
            ip = r.text.strip()
            if r.status_code != 200 or not self._validate_ipv4(ip):
                raise IPRetrievalError("Could not retrieve own IP address.")
        return ip

    @staticmethod
    def _validate_ipv4(ip):
        if ip is None:
            return None
        parts = ip.split(".")
        if len(parts) != 4:
            return False
        for item in parts:
            if not 0 <= int(item) <= 255:
                return False
        return True




if __name__ == "__main__":
    yg = YouGov(0)
    sources = yg.get_available_sources()
    if not sources:
        print("No sources available to upload. Quitting...")
        quit()

    for source_name in sources:
        if source_name == "amazon-shopping-history":
            payload = {"data": {}}
        else:
            payload = {"data": []}
        yg.upload_data(source_name, payload)

print("Done!!!")
