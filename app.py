from flask import Flask, request
import util
import whatsappservice
import chatgptservice

app = Flask(__name__)
@app.route('/welcome', methods=['GET'])
def index():
    return "welcome developer"

@app.route('/whatsapp', methods=['GET'])
def VerifyToken():
    
    try:
        accessToken = "78SAJSNJANS76S8DSHDBSBDS"
        token = request.args.get("hub.verify_token")
        challenge = request.args.get("hub.challenge")

        if token != None and challenge != None and token == accessToken:
            return challenge
        else:
            return "", 400
    except:
        return "", 400    

@app.route('/whatsapp', methods=['POST'])
def ReceivedMessage():

    try:
        body = request.get_json()
        entry = (body["entry"])[0]
        changes = (entry["changes"])[0]
        value = changes["value"]
        message = (value["messages"])[0]
        number = message["from"]

        text = util.GetTextUser(message)
        responseGPT = chatgptservice.GetResponse(text)
        if responseGPT != "error":
            data = util.TextMessage(responseGPT, number)
        else:
            data = util.TextMessage("Lo siento, ocurrió un problema.", number)

        whatsappservice.SendMessageWhatsapp(data)
        # ProcessMessages(text, number)
        # print (text)

        return "EVENT_RECEIVED"
    except:
        return "EVENT_RECEIVED"

def ProcessMessages(text,number):
    text = text.lower()
    listData = []

    if "hi" in text or "option" in text:
        data = util.TextMessage("Hello, how can I help you?", number)
        dataMenu = util.ListMessage(number)

        listData.append(data)
        listData.append(dataMenu)

    elif "thank" in text:
        data = util.TextMessage("Thank you for contacting me", number)
    elif "agency" in text:
        data  = util.TextMessage("This is our agency", number)
        dataLocation = util.LocationMessage(number)
        listData.append(data)
        listData.append(dataLocation)
    elif "contact" in text:
        data = util.TextMessage("*Contact center:*\n00783456", number)
        listData.append(data)

    elif "buy" in text:
        data = util.ButtonsMessage(number)
        listData.append(data)
    elif "sell" in text:
        data = util.ButtonsMessage(number)
        listData.append(data)

    elif "sign up" in text:
        data = util.TextMessage("Enter this link to register: https://form.jotform.com/222507994363665", number)
        listData.append(data)

    elif "log in" in text or "login" in text:
        data = util.TextMessage("Enter this link to log in: https://form.jotform.com/222507994363665", number)
        listData.append(data)

    else:
        data = util.TextMessage("I'm sorry, I cant't understand you", number)
        listData.append(data)

    for item in listData:
        whatsappservice.SendMessageWhatsapp(item)

def GenerateMessage(text, number):
    
    text = text.lower()
    if "text" in text:
        data = util.TextMessage("Text", number)
    if "format" in text:
        data = util.TextFormatMessage(number)
    
    if "image" in text:
        data = util.ImageMessage(number)

    if "video" in text:
        data = util.VideoMessage(number)
    if "audio" in text:
        data = util.AudioMessage(number)

    if "document" in text:
        data = util.DocumentMessage(number)
    if "location" in text:
        data = util.LocationMessage(number)
    if "button" in text:
        data = util.ButtonsMessage(number)
    if "list" in text:
        data = util.ListMessage(number)

    whatsappservice.SendMessageWhatsapp(data)

if(__name__ == "__main__"):
    app.run()