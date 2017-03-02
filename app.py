#!/usr/bin/env python

from __future__ import print_function
from future.standard_library import install_aliases
install_aliases()

from urllib.parse import urlparse, urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import requests
import json
import os


from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))

    #res = processRequest(req)
    res = run_post()
    res = json.dumps(res, indent=4)
    # print(res)
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def run_post():
    #url = 'https://sandbox.api.kasikornbank.com:8243/gh/deposit/sight/transactions/1.0.0'
    url = 'https://sandbox.api.kasikornbank.com:8243/gh/creditcard/point/1.0.0'
    data = {"CARD_NO_ENCPT":"492141******6698"}
    headers = {'Content-Type' : 'application/json'}

    r = requests.post(url, data=json.dumps(data), headers=headers, verify=False)
    
    speech = ""
    d = json.loads(r.text)
    for item in range(d):
        speech = item["CRN_BAL_PTN_CTD"]
    
   # speech = d[0]["CRN_BAL_PTN_CTD"]
    
     
    print("Response:")
    print(speech)

    return {
        "speech": "Your credit card balance is" + speech,
        "displayText": "Your credit card balance is" +speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }

def processRequest(req):
    if req.get("result").get("action") == "getBalance":
        return run_post()
    return {
        "speech": "It's seem service is not available right now",
        "displayText": "It's seem service is not available right now",
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }
  
def makeYqlQuery(req):
    result = req.get("result")
    parameters = result.get("parameters")
    city = parameters.get("geo-city")
    if city is None:
        return None

    return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    trn = data.get('TXN_DSC_EN')

    speech = "transfer in " + trn

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')
