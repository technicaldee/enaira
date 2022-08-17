# Your code goes here
from email import message
from flask import Flask, request
import json
import random
import requests
import africastalking
import http.client
import ssl
# import asyncio
# import aioflask

# from aioflask import Flask, request, Response

username = 'sandbox'
api_key = 'd4157382a1cc716cfd17bbbf115dc6213ff7a22286aa3f60e3254d6548cab6b7'
africastalking.initialize(username, api_key)

app = Flask(__name__)

response = ""

@app.route('/favicon.ico')
def favicon():
    return 'OK'

def sendMail(message, phone):
    africastalking.SMS.send(
       message,
       [phone]
   )

def option2(phone_number):

    conn = http.client.HTTPSConnection("rgw.k8s.apis.ng", context = ssl._create_unverified_context())

    payload = {
                "phone_number": phone_number.replace('+234', '0'),
                "user_type": "USER",
                "channel_code": "APISNG"
                }

    headers = {
        'ClientId': "40b011dd72596c3baf51f886f952d51f",
        'content-type': "application/json",
        'accept': "application/json"
        }

    conn.request(method="POST", url="/centric-platforms/uat/enaira-user/GetUserDetailsByPhone", body=json.dumps(payload), headers=headers)

    res = conn.getresponse()
    data = res.read()

    ndata = json.loads(data.decode("utf-8"))
    data = ndata['response_data']
    try:
        if('Data' in data):
            tosend = 'You are not yet registered with eNaira'
            sendMail(tosend, phone_number)
        else:
            tosend = "Dear "+data['first_name']+" "+data['last_name']+", \n The Account Number connected to enaira is: \n "+data['account_number']+"; "+data['relationship_bank']+". \n and your wallet address is "+data['wallet_info']['wallet_address']
            sendMail(tosend, phone_number)
    except:
        tosend = 'Something went wrong!'
        # sendMail(tosend, phone_number)
    print(data)

def register(text, phone_number):
    try:
        transf = text.split(',')
        print(transf[3])
        print(phone_number)
        name = transf[0].split()
        url = 'https://rgw.k8s.apis.ng/centric-platforms/uat/enaira-user/CreateConsumerV2'
        headers = {
        'Content-Type': 'application/json',
        'ClientId': '40b011dd72596c3baf51f886f952d51f'
        }
        request_data = {
            "channelCode": "APISNG",
            "uid": transf[2],
            "uidType": "BVN",
            "reference": "NXG3547585HGTKJHGO",
            "title": "Mr",
            "firstName": name[0],
            "middleName": name[1],
            "lastName": name[2],
            "userName": str(name[0])+str(name[2])+str(random.randint(90, 900)),
            "phone": phone_number,
            "emailId": str(name[0])+str(name[2])+str(random.randint(90, 900))+"@gmail.com",
            "postalCode": "900110",
            "city": "gwarinpa",
            "address": "Lagos Estate, Abuja",
            "countryOfResidence": "NG",
            "tier": "2",
            "accountNumber": transf[3],
            "dateOfBirth": "31/12/1987",
            "countryOfBirth": "NG",
            "password": transf[2],
            "remarks": "Passed",
            "referralCode": "@imbah.01"
            }
        res = requests.post(url, headers=headers, json=request_data, verify=False)
        data = res.json()['response_data']
        print(data)
        res = data['message']
        return res
    except Exception as e:
        print(e)
        res = 'An Error Occured'
        return res

@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    phone_number = str(request.values.get("phoneNumber", '+2347082500307'))
    phone_number = phone_number.replace(' ', '')
    data = request.get_json(force=True)
    text = request.get_json(force=True)
    
    print(f'Delivery report response...\n ${data}')

    # sendMail(register(text, phone_number), phone_number)
    sendMail(data, phone_number)

    return Flask.Response(status=200) 

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = str(request.values.get("phoneNumber", '+2348035336810'))
    phone_number = phone_number.replace(' ', '')
    text = request.values.get("text", "default")
    print(text)

    if text == '':
        response  = "CON What would you want to do \n"
        response += "1. Use this language \n"
        response += "2. Yi amfani da wannan harshe \n"
        response += "3. Lo ede yii \n"
        response += "4. Jiri asụsụ a \n"
        response += "5. More languages"

    if text == '1':
        response  = "CON What would you want to do \n"
        response += "1. Create eNaira Wallet \n"
        response += "2. Check my eNaira Info \n"
        response += "3. Load my eNaira wallet \n"
        response += "4. Transfer money \n"
        response += "5. Pay"

    elif text == '1*1':
        response = "CON Do you have a bank account? \n"
        response += "1. Yes \n"
        response += "2. No \n"

    elif text == '1*1*1':
        message = "Send REGISTER with your \n Full Name, BVN, Password(12 chars or more) \n and Account Number to 88081 seperated by comma \n eg 'REGISTER Mr John Bassey Okon,2847592048,\nPa$$word1234,2262933119' to 88081. \n\nNo spaces after comma"
        sendMail(message, phone_number)
        response = "END Dear customer, you will receive a message on how to register for enaira shortly"

    elif text == '1*1*2':
        message = "Dear customer, visit the nearest \n POS center to open an account!"
        sendMail(message, phone_number)
        response = "END Dear customer, you will receive a message on how to register for enaira shortly"

    elif text == '1*2':
        option2(phone_number)
        response = 'END Dear user, you will receive an SMS with your enaira details shortly'
        return response
        
    elif text == '1*3':
        response  = "CON Credit through? \n"
        response += "1. Bank \n"
        response += "2. POS \n"
        
    elif text == '1*3*1':
        response  = "CON Select the bank or financial provider to credit from \n"
        response += "1. First Bank \n"
        response += "2. GTCO \n"
        response += "3. Zenith Bank \n"
        response += "5. Access Bank \n"
        response += "6. Titan Trust Bank \n"
        response += "7. Load More Banks"
        
    elif text == '1*3*2':
        response  = "END Feature coming soon! \n"

    elif text == '1*4':
        response  = "CON Transfer money to \n"
        response += "1. To cash \n"
        response += "2. Another Wallet \n"

    elif text == '1*4*2':
        response = "END Send PAY with wallet_address, amount and pin to 88081"

    elif text == '1*5':
        response = "END Send PAY with wallet_address, amount and pin to 88081"

    elif text == '1*4*1':
        response  = "CON To Cash \n"
        response += "1. Bank \n"
        response += "2. POS \n"

    elif text == '1*4*1*1':
        response  = "CON Select the bank or financial provider to transfer money to \n"
        response += "1. First Bank \n"
        response += "2. GTCO \n"
        response += "3. Zenith Bank \n"
        response += "4. Access Bank \n"
        response += "5. Titan Trust Bank \n"
        response += "6. Load More Banks \n"

    elif text == '1*4*1*2':
        response  = "END Feature coming soon! \n"

    elif '1*3*1*' in text:
        response = "END Send RECEIVE with account number to 88081"

    elif '1*4*1*1*' in text:
        response = "END Send PAY with account number to 88081"
    else:
        response  = "CON Select language \n"
        response += "1. Use this language \n"
        response += "2. Yi amfani da wannan harshe \n"
        response += "3. Lo ede yii \n"
        response += "4. Jiri asụsụ a \n"
        response += "5. More languages"
    return response

# if __name__ == '__main__':
# #     # pass
#     app.run(host="0.0.0.0",port=8000)