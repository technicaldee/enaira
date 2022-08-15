# Your code goes here
from email import message
from flask import Flask, request
import json
import random
import requests
import africastalking

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

@app.route('/delivery-reports', methods=['POST'])
def delivery_reports():
    phone_number = str(request.values.get("phoneNumber", '08035336810'))
    phone_number = phone_number.replace(' ', '')
    data = request.get_json(force=True)
    
    print(f'Delivery report response...\n ${data}')

    return Flask.Response(status=200) 

@app.route('/', methods=['POST', 'GET'])
def ussd_callback():
    global response
    session_id = request.values.get("sessionId", None)
    service_code = request.values.get("serviceCode", None)
    phone_number = str(request.values.get("phoneNumber", '08035336810'))
    phone_number = phone_number.replace(' ', '')
    text = request.values.get("text", "default")
    print(text)

    if text == '':
        response  = "CON What would you want to do \n"
        response += "1. Create eNaira Wallet \n"
        response += "2. Check my eNaira Info \n"
        response += "3. Load my eNaira wallet \n"
        response += "4. Transfer money"

    elif text == '1':
        message = "Send your REGISTER and your Full Name, BVN, Password(12 chars or more) and Account Number seperated by comma eg 'REGISTER Mr John Bassey Okon,2847592048,Pa$$word1234,2262933119'; No spaces after comma"
        sendMail(message, phone_number)
        response = "END Dear user, you will receive instructions on how to register for enaira shortly"
        # response += "1. Account number \n"
        # response += "2. Account balance"

    elif text == '1*1':
        accountNumber  = "ACC1001"
        response = "END Your account number is " + accountNumber

    elif text == '1*2':
        balance  = "KES 10,000"
        response = "END Your balance is " + balance

    elif text == '2':
        response = 'END Dear user, you will receive an SMS with your enaira details shortly'
        try:
            url = 'https://rgw.k8s.apis.ng/centric-platforms/uat/enaira-user/GetUserDetailsByPhone'
            headers = {
                'Content-Type': 'application/json',
                'ClientId': '40b011dd72596c3baf51f886f952d51f'
                }
            request_data = {
                "phone_number": phone_number,
                "user_type": "USER",
                "channel_code": "APISNG"
                }
            res = requests.post(url, headers=headers, json=request_data, verify=False)
            data = res.json()['response_data']
            try:
                if(data['Data']['status'] == 'error'):
                    tosend = 'You are not yet registered with eNaira'
                else:
                    tosend = "Dear "+data['first_name']+" "+data['last_name']+", The Account Number connected to enaira is: "+data['account_number']+"; "+data['relationship_bank']+". and your wallet address is "+data['wallet_info']['wallet_address']
            except:
                tosend = 'Something went wrong!'
            sendMail(tosend, phone_number)
            print(data)
            
            
        except Exception as e:
            print(e)
            response = 'You are not yet registered with eNaira or an error occured'
    elif text == '3':
        response  = "CON Select the bank or financial provider to credit from \n"
        response += "1. First Bank \n"
        response += "2. GTCO \n"
        response += "3. Zenith Bank \n"
        response += "4. Access Bank"
        response += "4. Titan Trust Bank"
        response += "4. Load More Banks"
    elif text == '4':
        response  = "CON Select the bank or financial provider to transfer monry to \n"
        response += "1. First Bank \n"
        response += "2. GTCO \n"
        response += "3. Zenith Bank \n"
        response += "4. Access Bank"
        response += "4. Titan Trust Bank"
        response += "4. Load More Banks"
    else:
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
            response = data['message']
        except Exception as e:
            print(e)
            response = 'An Error Occured'


    return response

# if __name__ == '__main__':
#     # pass
#     app.run(host="0.0.0.0",port=8000)