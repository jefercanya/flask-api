import requests
import json

def SendMessageWhatsapp(data):
    try:
        token = "YOUR_TOKEN"
        api_url = "https://graph.facebook.com/v13.0/YOUR_ID/messages"
        headers = {"Content-Type": "application/json", "Authorization": "Bearer " + token}
        response = requests.post(api_url, data = json.dumps(data), headers = headers)
        if response.status_code == 200:
            return True
        
        return False
    except Exception as exception:
        print(exception)
        return False