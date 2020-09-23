from client.models import User,catch,bankaccount,telegram_active,Loan_queue,new_loan
import json,locale
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import jdatetime
from client.views import SendMessage
from client.admin import Inventory,CountAllLoan,CountPayLoan,UnpaidLoan
from datetime import datetime, timedelta
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
    tempdata=request.POST.get('data',"")
    webhook=json.loads(tempdata)['message']
    try:
        Qr = Q()
        context['chat_id']=webhook['from']['id']
        #handle1=open('/home/mrprogramer/bank/static/test.txt','r+')
        Qr = Qr & (Q(**{"telegramid": webhook['from']['id']}))
        u=User.objects.filter(Qr)
        if u.exists():
            # try:
            #     webhook['contact']
            #     if webhook['from']['id'] != 13814588:#13814588 #57113444
            #         #handle1.write(str(webhook['from']['id']))
            #         r = requests.post(url+"sendMessage", data = {'chat_id':webhook['from']['id'],"text":"شما نمیتوانید حساب کسی را فعال کنید برای فعال کردن حساب کاربری با @Abbas2044 ارتباط بر قرار کنید."})
            #     else:
            #         context['cellphone']=webhook['contact']['phone_number'][-10:]
            #         Qr = Q()
            #         Qr = Qr & (Q(**{"cellphone__contains": context['cellphone']}))
            #         u=User.objects.filter(Qr)
            #         if u.exists():
            #             u=u[0]
            #             context['contact_user_id']=webhook['contact']['user_id']
            #             reply_markup='{"keyboard":[["وضعیت حساب"],["وضعیت وام"],["تغییر گذرواژه سایت"]],"one_time_keyboard":true}'
            #             requests.post(url+"sendMessage", data = {'chat_id':webhook['from']['id'],"text":"تلگرام حساب کاربری آقای "+u.first_name+" "+u.last_name+" با شماره تلفن"+u.cellphone + " فعال شد."})
            #             requests.post(url+"sendMessage", data = {'chat_id':webhook['contact']['user_id'],"text":"حساب کاربری شما فعال شد.",'reply_markup':reply_markup})
            #             u.telegramid=str(webhook['contact']['user_id'])
            #             u.save()
            #     return HttpResponse(json.dumps(context), content_type="application/json")
            # except KeyError:
            #     pass
            u=u[0]
            if webhook['text'] == "وضعیت حساب":
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
                    reply_markup = {"keyboard":[["وضعیت حساب"],["وضعیت وام"],["تغییر گذرواژه سایت"],["یک سال من چگونه گذشت؟"]],"one_time_keyboard":True}
                    Message = "تاریخ:" + str(jdatetime.datetime.now().year)+"/"+str(jdatetime.datetime.now().month)+"/"+str(jdatetime.datetime.now().day)+"\n"
                    Message+="شماره حساب: "+acc.name+"\n"
                    Message=Message+"تعداد قسط پرداختی توسط شما:"+str(count)+"\nموجودی حساب شما:"+locale.currency( price, grouping=True )
                    Message=Message+"\n"
                    for item in catchs:
                        Message=Message+"\nسود سال "+str(item.year)+" مبلغ "+locale.currency( item.price*10000, grouping=True )+" می باشد."
                        price=price+item.price*10000
                    Message=Message+"\nکل موجودی شما مبلغ "+locale.currency( price, grouping=True )+" می باشد."
                    try:
                        Message += "\nسود شما :" + percentage(acc)
                        Message += "\nبالاترین سود :" + percentage(bankaccount.objects.filter().order_by("-points")[0])
                    except:
                        Message += "\nسود شما : در حال حاضر محاسبه نشده است."
                        Message += "\nبالاترین سود :در حال حاضر محاسبه نشده است."
                    Message += "\nتعداد افرادی که بیشتر از شما واریزی داشته اند :" + str(bankaccount.objects.filter(points__gt=acc.points).count())
                    SendMessage(webhook['from']['id'], Message, reply_markup)
                return HttpResponse(json.dumps(context), content_type="application/json")
            elif webhook['text'] == "یک سال من چگونه گذشت؟":
                Qr = Q()
                Qr = Qr & (Q(**{"user": u}))
                bankaccounts = bankaccount.objects.filter(Qr)
                count= 0
                for acc in bankaccounts:
                    Qr = Q()
                    Qr = Qr & (Q(**{"added_with_bank": False}))
                    Qr = Qr & (Q(**{"bankaccount": acc}))
                    Qr = Qr & (Q(**{"date__gt": datetime(year=datetime.now().year-1,month=datetime.now().month,day=datetime.now().day)}))
                    catchs=catch.objects.filter(Qr)
                    count=count+len(catchs)
                    price=0
                    for item in catchs:
                        price= price + item.price
                    Qr = Q()
                    Qr = Qr & (Q(**{"bankaccount": acc}))
                    Qr = Qr & (Q(**{"added_with_bank": True}))
                    Qr = Qr & (Q(**{"date__gt": datetime(year=datetime.now().year-1,month=datetime.now().month,day=datetime.now().day)}))
                    catchs=catch.objects.filter(Qr)
                    price=price*10000
                    locale.setlocale( locale.LC_ALL, 'fa_IR' )
                    reply_markup = {"keyboard":[["وضعیت حساب"],["وضعیت وام"],["تغییر گذرواژه سایت"],["یک سال من چگونه گذشت؟"]],"one_time_keyboard":True}
                    Message = "از تاریخ:" + str(jdatetime.datetime.now().year-1)+"/"+str(jdatetime.datetime.now().month)+"/"+str(jdatetime.datetime.now().day)+"\n"
                    Message += "تا تاریخ:" + str(jdatetime.datetime.now().year)+"/"+str(jdatetime.datetime.now().month)+"/"+str(jdatetime.datetime.now().day)+"\n"
                    Message += "شماره حساب: "+acc.name+"\n"
                    Message=Message+"تعداد قسط پرداختی توسط شما:"+str(count)+"\nموجودی حساب شما:"+locale.currency( price, grouping=True )
                    Message=Message+"\n"
                    for item in catchs:
                        Message=Message+"\nسود امسال "+str(item.year)+" مبلغ "+locale.currency( item.price*10000, grouping=True )+" می باشد."
                        price=price+item.price*10000
                    Message=Message+"\nکل موجودی شما مبلغ "+locale.currency( price, grouping=True )+" می باشد."
                    SendMessage(webhook['from']['id'], Message, reply_markup)
                return HttpResponse(json.dumps(context), content_type="application/json")
            elif webhook['text'] == "وضعیت وام":
                bk = bankaccount.objects.filter(user=u)
                lq = Loan_queue.objects.filter(bankaccount__in=bk)
                lo={}
                reply_markup = {"keyboard":[["وضعیت حساب"],["وضعیت وام"],["تغییر گذرواژه سایت"],["یک سال من چگونه گذشت؟"]],"one_time_keyboard":True}
               
                
                 
                locale.setlocale( locale.LC_ALL, 'fa_IR' )
                #locale.setlocale( locale.LC_ALL, 'fa' )
                
                # loan_amount= ( lo.loan_amount*10000)
                # part_amount=( lo.part_amount*10000)
                
                mess="آقای  "+ bk[0].user.first_name+" "+bk[0].user.last_name + "  عزیز \n"
                mess += "تعداد وام هایی که به شما داده شده است:"+str(len(lq))+"\n"
                mess += "تعداد وام های تسویه شده:"+str(len(Loan_queue.objects.filter(bankaccount__in=bk,status=1)))+"\n"
                mess += "تعداد وام های در حال پردازش:" + str(len(Loan_queue.objects.filter(bankaccount__in=bk, status=-1))) + "\n"
                if len(Loan_queue.objects.filter(bankaccount__in=bk, status=0)):
                    new_los=new_loan.objects.filter(loan_queue__in=Loan_queue.objects.filter(bankaccount__in=bk, status=0))
                    for new_lo in new_los:
                        mess +="---------------\n"
                        mess +="تعداد قسط عقب افتاده ی شما:"+str(UnpaidLoan(new_lo))+"\n"
                        mess += "تعداد قسط پرداخت شده ی شما:" + str(CountPayLoan(new_lo))+"\n"
                        mess += "تعداد کل قسط های شما:" + str(CountAllLoan(new_lo))+"\n"
                        mess += "مبلغ کل وام:" + locale.currency(Loan_queue.objects.filter(bankaccount__in=bk, status=0)[0].amount*1000, grouping=True )+" تومان\n"
                        mess += "مبلغ هر قسط:" + locale.currency(new_lo.peak*1000, grouping=True)+" تومان\n"
                        mess += "مبلغ باقیمانده:" + locale.currency(Loan_queue.objects.filter(bankaccount__in=bk, status=0)[0].amount*1000 - (new_lo.peak*1000*CountPayLoan(new_lo)), grouping=True)+"\n"
                        mess += "مبلغ پرداخت شده توسط شما:" + locale.currency(-1 * (Loan_queue.objects.filter(bankaccount__in=bk, status=0)[0].amount*1000 - Loan_queue.objects.filter(bankaccount__in=bk, status=0)[0].amount*1000 - (new_lo.peak*1000*CountPayLoan(new_lo))), grouping=True)+"\n"
                # p1=lo.part_payed * part_amount
                # p2=loan_amount - p1
                # mess=mess+" مبلغ پرداخت شده : "+locale.currency(p1, grouping=True)+" \n مبلغ باقی مانده : "+locale.currency(p2, grouping=True)
                SendMessage(bk[0].user.telegramid, mess,reply_markup)
                return HttpResponse(json.dumps(context), content_type="application/json")
            elif webhook['text'] == "تغییر گذرواژه سایت":
                reply_markup = {"keyboard":[["وضعیت حساب"],["وضعیت وام"],["تغییر گذرواژه سایت"]],"one_time_keyboard":True}
                tgact = telegram_active.objects.filter(telegramid=str(webhook['from']['id']))
                if tgact.exists():
                    tgact = tgact[0]
                    if u.telegramid == tgact.telegramid:
                        tgact.key=None
                        tgact.save()
                        u.password = ""
                        u.save()
                        text = "با آدرس زیر وارد سامانه صندوق شده و لاگین کنین\nhttp://sandogh-zainab.vps-vds.com/resetpassword/telegram/" + tgact.key
                        SendMessage(webhook['from']['id'], text, reply_markup)
                    else:
                        text = "تلگرام شما به هیچ حسابی وصل نمی باشد. توسط مدیر آن را بازیابی کنید."
                        SendMessage(webhook['from']['id'], text, reply_markup)
                else:
                    text = "تلگرام شما به هیچ حسابی وصل نمی باشد. توسط مدیر آن را بازیابی کنید."
                    SendMessage(webhook['from']['id'], text, reply_markup)
                return HttpResponse(json.dumps(context), content_type="application/json")
            reply_markup = {"keyboard":[["وضعیت حساب"],["وضعیت وام"],["تغییر گذرواژه سایت"]],"one_time_keyboard":True}
            text = "این دستور وجود ندارد."
            SendMessage(webhook['from']['id'], text, reply_markup)
        else:
            #reply_markup='{"keyboard":[["Yes","No"],["Maybe"],["1","2","3"]],"one_time_keyboard":true}'
            reply_markup={"keyboard":[["درخواست فعال سازی"]],"one_time_keyboard":True}
            if webhook['text'] == "/start":
                text="بر روی دکمه فعالسازی کلیک کنید."
            else:
                try:
                    tgact = telegram_active.objects.get(telegramid=str(webhook['from']['id']))
                    tgact.key=None
                    tgact.save()
                except:
                    tgact = telegram_active()
                    tgact.telegramid=str(webhook['from']['id'])
                    tgact.save()
                text = "برای فعال سازی تلگرام میبایست با آدرس زیر احراز هویت بشوید.\nhttps://sandogh-zainab.vps-vds.com/activate/telegram/"+tgact.key
            SendMessage(webhook['from']['id'],text,reply_markup)
        #handle1.close()
    except KeyError:
        SendMessage(webhook['from']['id'],"برنامه با مشکل مواجه شده است برای لطفا به آقای بغدادی اطلاع دهید. @Abbas2044")
    return HttpResponse(json.dumps(context), content_type="application/json")