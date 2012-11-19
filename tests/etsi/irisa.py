#!/usr/bin/env python3
# coding: utf-8

import requests
import logging

send_url = "http://senslab2.irisa.fr/coap/submit"
values = {
    "agree" : 1,
    "file": "irisa.py"
}

r = requests.post(send_url, data=values, files={'irisa.py': open('irisa.py', 'rb')})
print(r.content)
