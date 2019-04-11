from bank.settings import telegapiKey
import requests,json

def SendMessage(chat_id,text,reply_markup={}):
    url = "https://api.telegram.org/bot" + telegapiKey + "/"
    try:
        return requests.post(url + "sendMessage",data={'chat_id':chat_id,"text":text,'reply_markup': json.dumps(reply_markup)},
                    proxies=dict(http='socks5://sandogh:85mamad85@185.53.141.123:441',
                                 https='socks5://sandogh:85mamad85@185.53.141.123:441'))
    except:
        return None