from bank.settings import telegapiKey
import requests,json

def SendMessage(chat_id,text,reply_markup={}):
    url = "https://api.telegram.org/bot" + telegapiKey + "/"
    return requests.post(url + "sendMessage",data={'chat_id':chat_id,"text":text,'reply_markup': json.dumps(reply_markup)})