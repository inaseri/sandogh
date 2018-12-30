from client.models import User,catch,Loan,bankaccount
from bank.settings import telegapiKey
import json,sys,locale
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import requests
from django.db.models import Q
import jdatetime

def percentage(obj):
    bnk = bankaccount.objects.all()
    j=0
    for i in bnk:
        j += i.points
    value = round(obj.points / j * 100,2)
    return str(value)+"%"

@csrf_exempt
def data(request):
    context={}
    url="https://api.telegram.org/bot"+telegapiKey+"/"
    print(telegapiKey)
    tempdata=request.POST.get('data',"")
    webhook={}
    #handle1=open('/home/mrprogramer/bank/static/webhook.txt','r+')
    #handle1.write(tempdata)
    #handle1.close()
    webhook=json.loads(tempdata)['message']
    try:
        Qr = Q()
        context['chat_id']=webhook['from']['id']
        handle1=open('/home/mrprogramer/bank/static/test.txt','r+')
        Qr = Qr & (Q(**{"telegramid": webhook['from']['id']}))
        u=User.objects.filter(Qr)
        if u.exists():
            try:
                webhook['contact']
                if webhook['from']['id'] != 13814588:#13814588 #57113444
                    handle1.write(str(webhook['from']['id']))
                    r = requests.post(url+"sendMessage", data = {'chat_id':webhook['from']['id'],"text":"شما نمیتوانید حساب کسی را فعال کنید برای فعال کردن حساب کاربری با @Abbas2044 ارتباط بر قرار کنید."})
                else:
                    context['cellphone']=webhook['contact']['phone_number'][-10:]
                    Qr = Q()
                    Qr = Qr & (Q(**{"cellphone__contains": context['cellphone']}))
                    u=User.objects.filter(Qr)
                    if u.exists():
                        u=u[0]
                        context['contact_user_id']=webhook['contact']['user_id']
                        reply_markup='{"keyboard":[["وضعیت حساب"],["وضعیت وام"]],"one_time_keyboard":true}'
                        requests.post(url+"sendMessage", data = {'chat_id':webhook['from']['id'],"text":"تلگرام حساب کاربری آقای "+u.first_name+" "+u.last_name+" با شماره تلفن"+u.cellphone + " فعال شد."})
                        requests.post(url+"sendMessage", data = {'chat_id':webhook['contact']['user_id'],"text":"حساب کاربری شما فعال شد.",'reply_markup':reply_markup})
                        u.telegramid=str(webhook['contact']['user_id'])
                        u.save()
                return HttpResponse(json.dumps(context), content_type="application/json")
            except KeyError:
                pass
            if webhook['text'] == "وضعیت حساب":
                Qr = Q()
                Qr = Qr & (Q(**{"telegramid": webhook['from']['id']}))
                u=User.objects.get(Qr)
                Qr = Q()
                Qr = Qr & (Q(**{"user": u}))
                bankaccounts = bankaccount.objects.filter(Qr)
                for acc in bankaccounts:
                    count= acc.count
                    Qr = Q()
                    Qr = Qr & (Q(**{"added_with_bank": False}))
                    Qr = Qr & (Q(**{"bankaccount": acc}))
                    catchs=catch.objects.filter(Qr)
                    count=count+len(catchs)
                    price=0
                    for item in catchs:
                        price= price + item.price
                    Qr = Q()
                    Qr = Qr & (Q(**{"bankaccount": acc}))
                    Qr = Qr & (Q(**{"added_with_bank": True}))
                    catchs=catch.objects.filter(Qr)
                    price=price*10000
                    locale.setlocale( locale.LC_ALL, 'fa_IR' )
                    reply_markup='{"keyboard":[["وضعیت حساب"],["وضعیت وام"]],"one_time_keyboard":true}'
                    Message = "تاریخ:" + str(jdatetime.datetime.now().year)+"/"+str(jdatetime.datetime.now().month)+"/"+str(jdatetime.datetime.now().day)+"\n"
                    Message+="شماره حساب: "+acc.name+"\n"
                    Message=Message+"تعداد قسط پرداختی توسط شما:"+str(count)+"\nموجودی حساب شما:"+locale.currency( price, grouping=True )
                    Message=Message+"\n"
                    for item in catchs:
                        Message=Message+"\nسود سال "+str(item.year)+" مبلغ "+locale.currency( item.price*10000, grouping=True )+" می باشد."
                        price=price+item.price*10000
                    Message=Message+"\nکل موجودی شما مبلغ "+locale.currency( price, grouping=True )+" می باشد."
                    Message += "\nسود شما :" + percentage(acc)
                    Message += "\nبالاترین سود :" + percentage(bankaccount.objects.filter().order_by("-points")[0])
                    Message += "\nتعداد افرادی که بیشتر از شما واریزی داشته اند :" + str(bankaccount.objects.filter(points__gt=acc.points).count())
                    requests.post(url+"sendMessage", data = {'chat_id':webhook['from']['id'],"text":Message,'reply_markup':reply_markup})
                return HttpResponse(json.dumps(context), content_type="application/json")
            elif webhook['text'] == "وضعیت وام":
                Qr = Q()
                Qr = Qr & (Q(**{"telegramid": webhook['from']['id']}))
                u=User.objects.get(Qr)
                lo=Loan.objects.get(user=u)  
                reply_markup='{"keyboard":[["وضعیت حساب"],["وضعیت وام"]],"one_time_keyboard":true}'
               
                
                 
                locale.setlocale( locale.LC_ALL, 'fa_IR' )
                #locale.setlocale( locale.LC_ALL, 'fa' )
                
                loan_amount= ( lo.loan_amount*10000)
                part_amount=( lo.part_amount*10000)
                
                mess="آقای  "+ lo.user.first_name+" "+lo.user.last_name + "  عزیز \n اطلاعات وام دریافتی شما  : \n"
                mess=mess+"مبلغ وام شما : "+locale.currency(loan_amount, grouping=True)+"\n"
                mess=mess+"تعداد اقساط پرداختی : "+str(lo.part_payed) + " از "+str(lo.parts)+"\n"
                mess=mess+"مبلغ هر قسط :"+ locale.currency(part_amount, grouping=True)+"\n "
                
                p1=lo.part_payed * part_amount
                p2=loan_amount - p1
                mess=mess+" مبلغ پرداخت شده : "+locale.currency(p1, grouping=True)+" \n مبلغ باقی مانده : "+locale.currency(p2, grouping=True)
                
                requests.post("https://api.telegram.org/bot"+telegapiKey+"/sendMessage", data = {'chat_id':lo.user.telegramid,"text":mess})
                return HttpResponse(json.dumps(context), content_type="application/json")
            
            reply_markup='{"keyboard":[["وضعیت حساب"],["وضعیت وام"]],"one_time_keyboard":true}'
            requests.post(url+"sendMessage", data = {'chat_id':webhook['from']['id'],"text":"این دستور وجود ندارد.",'reply_markup':reply_markup})            
            
        else:
            #reply_markup='{"keyboard":[["Yes","No"],["Maybe"],["1","2","3"]],"one_time_keyboard":true}'
            if webhook['text'] == "/start":
                reply_markup='{"keyboard":[["درخواست فعال سازی"]],"one_time_keyboard":true}'
                requests.post(url+"sendMessage", data = {'chat_id':webhook['from']['id'],"text":"بر روی دکمه فعالسازی کلیک کنید.",'reply_markup':reply_markup})
            else:
                reply_markup='{"keyboard":[["درخواست فعال سازی"]],"one_time_keyboard":true}'
                requests.post(url+"sendMessage", data = {'chat_id':webhook['from']['id'],"text":"حساب کار بری شما فعال نشده لطفا برای فعال سازی حساب خود با آقای بغدادی تماس بگیرید. @Abbas2044",'reply_markup':reply_markup})
                requests.post(url+"forwardMessage", data = {'chat_id':13814588,'from_chat_id':webhook['from']['id'],'message_id':webhook['message_id']})
        handle1.close()
    except KeyError:
        requests.post(url+"sendMessage", data = {'chat_id':webhook['from']['id'],"text":"برنامه با مشکل مواجه شده است برای لطفا به آقای بغدادی اطلاع دهید. @Abbas2044"})
    return HttpResponse(json.dumps(context), content_type="application/json")