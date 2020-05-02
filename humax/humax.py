#!/usr/bin/python3

from enum import Enum
import hashlib

import requests
from requests import post


class Basic(Enum):
    getStatus = "Basic.getStatus"
    getSetup = "Basic.getSetup"
    getDDNS = "Basic.getDDNS"
    getInitScan = "Basic.getInitScan"
    getSwitchMode = "Basic.getSwitchMode"


class Wireless(Enum):
    getWlanInterface = "Wireless.getWlanInterface"
    getRadio = "Wireless.getRadio"
    getPrimaryNetwork = "Wireless.getPrimaryNetwork"
    getPrimarySecurityType = "Wireless.getPrimarySecurityType"
    getGuestNetwork = "Wireless.getGuestNetwork"
    getWMM = "Wireless.getWMM"
    getWDS = "Wireless.getWDS"
    getDBInfo = "Wireless.getDBInfo"


class Advanced(Enum):
    getSetup = "Advanced.getSetup"
    getFiltering = "Advanced.getFiltering"
    getForwarding = "Advanced.getForwarding"
    getPortTriggers = "Advanced.getPortTriggers"
    getDMSHost = "Advanced.getDMSHost"
    getUPnP = "Advanced.getUPnP"


class Security(Enum):
    getFirewall = "Security.getFirewall"
    getVPNList = "Security.getVPNList"


class Device(Enum):
    getDBInfo = "Device.getDBInfo"


class System(Enum):
    getTimeSetting = "System.getTimeSetting"
    getAdministration = "System.getAdministration"


class Other(Enum):
    WebCmd = "WebCmd"


ALL_METHODS = []
for method_group in [Basic, Advanced, Security, Device, System, Other]:
    ALL_METHODS.extend(method.value for method in method_group)


class Humax:
    def __init__(self, url):
        self.url = url
        self.api = self.url + '/api'
        self.token = None
        self.session_timeout = None

    def _get_web_key(self):
        return self.post(Device.getDBInfo, WEB_KEY='')['WEB_KEY']

    def _encrypt_password(self, plaintext, web_key):
        # for some reason the key length has to be 4-times larger
        dk = hashlib.pbkdf2_hmac(
            'sha1',
            plaintext.encode(),
            web_key.encode(),
            2048,
            dklen=128/32*4)

        return dk.hex()

    def post(self, method, token=None, return_raw=False, **params):
        if isinstance(method, Enum):
            method = method.value

        data = {
            "method": method,
            "id": 90,
            "jsonrpc": "2.0",
            "params": params
        }
        if token:
            data['token'] = token
        r = requests.post(self.api, json=data).json()
        return r if return_raw else r['result']

    def posttoken(self, method, **params):
        return self.post(method, token=self.token, **params)

    def login(self, user, password):
        web_key = self._get_web_key()
        encrypted = self._encrypt_password(password, web_key)

        json = self.post('login', return_raw=True, id=user, password=encrypted)
        self.token = json['token']
        self.session_timeout = json['session_time_out']

    def get_forwarding(self):
        return self.posttoken(Advanced.getForwarding)
