# Your code goes here
from flask import Flask, request
import json
import requests
app = Flask(__name__)

response = ""

@app.route('/favicon.ico')
def favicon():
    return 'OK'

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = request.values.get("phoneNumber", None)
    text = request.values.get("text", "default")

    if text == '':
        response  = "CON What would you want to do \n"
        response += "1. Create eNaira Wallet \n"
        response += "2. Check my eNaira Info \n"
        response += "3. Load my eNaira wallet \n"
        response += "4. Transfer money"

    elif text == '1':
        response = "CON Chill till later this evening, Ill work on it"
        # response += "1. Account number \n"
        # response += "2. Account balance"

    elif text == '1*1':
        accountNumber  = "ACC1001"
        response = "END Your account number is " + accountNumber

    elif text == '1*2':
        balance  = "KES 10,000"
        response = "END Your balance is " + balance

    elif text == '2':
        url = 'https://rgw.k8s.apis.ng/centric-platforms/uat/enaira-user/GetUserDetailsByPhone'
        headers = {
            'Content-Type': 'application/json',
            'ClientId': '40b011dd72596c3baf51f886f952d51f'
            }
        request_data = {
              "phone_number": "08056064768",
              "user_type": "USER",
              "channel_code": "APISNG"
            }
        res = ''
        try:
            res = requests.post(url, headers=headers, json=request_data, verify=False)
        except Exception as e:
            # data = res.json()['response_data']
            res = e
        response = res
    else:
        response = "Error"

    return response

# if __name__ == '__main__':
#     pass
#     # app.run(host="0.0.0.0")