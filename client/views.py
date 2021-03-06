from django.db.models import Q
from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.http import JsonResponse
from .models import User,bankaccount,Loan_queue,catch,new_loan,new_loan_pay,telegram_active
from django.contrib.auth import authenticate,login,logout
from django.core.validators import validate_email
from django import forms
import re
import requests
from django.urls import reverse
import json
from django.contrib.auth.decorators import login_required
from django.http import Http404
import jdatetime
import uuid
from .telegramapi import SendMessage
from django.contrib import messages
# Create your views here.
def recaptcha(request):
    recaptcha_response=request.POST.get('g-recaptcha-response','')
    print(recaptcha_response)
    secret="6LekdikTAAAAAP1eXYh_kgz492Q-UNg4KJtWRfBe"
    remoteip=request.META['HTTP_X_FORWARDED_FOR']
    #remoteip=request.META['REMOTE_ADDR']
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data = {'secret':secret,"response":recaptcha_response,"remoteip":remoteip})
    recaptcha=json.loads(r.text)
    return recaptcha
@login_required
def index(request):
    context={}
    context['loan']={}
    context['loan']['count'] = Loan_queue.objects.filter(status__gt=-1).count()
    context['loan']['queue'] = Loan_queue.objects.filter(status=-1).count()
    context['bankaccounts'] = len(bankaccount.objects.all())
    context['useraccounts'] = len(User.objects.all())
    return render(request,'tmp2/dashboard.html', context)
@login_required
def bankaccs(request):
    context={}
    bnk = bankaccount.objects.filter(user=request.user)
    for acc in bnk:
        count = acc.count
        Qr = Q()
        Qr = Qr & (Q(**{"added_with_bank": False}))
        Qr = Qr & (Q(**{"bankaccount": acc}))
        catchs = catch.objects.filter(Qr)
        count = count + len(catchs)
        acc.count = count
    context['bnk']=bnk
    # if bnk.count()>1:
    #     return JsonResponse({})
    # else:
    #     return HttpResponseRedirect(reverse("bankacc", args=[bnk[0].id]))
    return render(request,'tmp2/bankacclist.html', context)
@login_required
def bankacc(request,id):
    context={}
    try:
        bnk=bankaccount.objects.get(id=id,user=request.user)
        context['acc_number'] = bnk.name
        ctch = catch.objects.filter(bankaccount=bnk).order_by("-date")
        context['catch']=[]
        for i in ctch:
            tmp={}
            tmp['date_added'] = i.date
            tmp['price'] = i.price
            tmp['bank']=i.added_with_bank
            context['catch'].append(tmp)
        return render(request,'tmp2/listpyements.html',context)
    except:
        return JsonResponse({"error":"Perimition denided"})
def Login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(request.GET.get("next","/"))
    context ={}
    if request.method == 'POST':
        username=request.POST['username']
        #check if id is phone number convert it to username
        pattern = re.compile("^\+\d{12,13}$", re.IGNORECASE)
        if pattern.match(username) is not None:
            username=User.objects.filter(cellphone=username)
            for items in username:
                username=items
        # Convert Email To username
        try:
            validate_email(username)
            if User.objects.filter(email=username).exists():
                username=User.objects.get(email=username).username
        except:
            pass
        #check user can authenticate
        try:
            user = authenticate(username=username, password=request.POST['password'])
        except:
            user=None
        print(user)
        #request.session['password']=request.POST['password']
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request,user)            
                return HttpResponseRedirect(request.GET.get("next","/"))
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
    return render(request, 'tmp2/login.html',context)

def recovery(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/")
    context ={}
    if request.method == 'POST': 
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        request.session['password']=request.POST['password']
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request,user)            
                return HttpResponseRedirect("/")
        else:
            # the authentication system was unable to verify the username and password
            print("The username and password were incorrect.")
    return render(request,"cloth_v1/accounts/recovery.html",context)
@login_required
def Logout(request):
    logout(request)
    return HttpResponseRedirect("/")
def SingUp(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/")
    context={}
    context['error']=0
    if request.method == 'POST':
        context['request']={}
        context['request']['firstname']=request.POST.get('firstname','')
        context['request']['lastname']=request.POST.get('lastname','')
        context['request']['username']=request.POST.get('username','')
        context['request']['email']=request.POST.get('email','')
        context['request']['password']=request.POST.get('password','')
        context['request']['cellphone']=request.POST.get('cellphone','')
        context['request']['accepttos']=request.POST.get('accepttos','')
        #FirstName Checking
        if recaptcha(request)['success']==False:
            context['captcha']=1
            context['error']=1
        if len(context['request']['firstname'])<3:
            context['Firstname']=1
            context['error']=1
        #LastName Checking
        if len(context['request']['lastname'])<3:
            context['Lastname']=1
            context['error']=1
        #username Checking
        pattern = re.compile("^[a-zA-Z0-9.]{6,}$", re.IGNORECASE)
        if pattern.match(context['request']['username'])is None:
            context['username_length']=1
            context['error']=1
        else:
            if User.objects.filter(username_clear=context['request']['username'].replace(".","")).exists():
                context['username_confilict']=1
                context['error']=1
        #Email Checking
        try:
            validate_email(context['request']['email'])
            if User.objects.filter(email=context['request']['email']).exists():
                context['email_confilict']=1
        except:
            context['email']=1
            context['error']=1
        #password Checking
        if context['request']['password']:
            context['Strength']=pwStrength(context['request']['password'])
            if context['Strength'] < 60:
                context['error']=1
        elif context['request']['password']!=request.POST.get('password2',''):
            context['passconfilict']=1
        else:
            context['error']=1
            context['password']=1
        #postcode Checking
        pattern = re.compile("^09\d{9}$", re.IGNORECASE)
        if pattern.match(context['request']['cellphone']) is None:
            context['cellphone']=1
            context['error']=1
        else:
            if User.objects.filter(cellphone=context['request']['cellphone']).exists():
                context['cellphone_confilict']=1
                context['error']=1
        #Register New User
        if context['error']==0:
            user = User.objects.create_user(context['request']['username'], context['request']['email'], context['request']['password'],cellphone=context['request']['cellphone'],username_clear=context['request']['username'].replace(".",""))
            user.first_name = context['request']['firstname']
            user.last_name = context['request']['lastname']
            user.save()
            context['register']=1
    return render(request,"cloth_v1/accounts/signup.html",context)

def findSeqChar(CharLocs, src):
    AllSeqChars = []
    i = 0
    SeqChars = []
    while i < len(CharLocs) - 1:
        if CharLocs[i + 1] - CharLocs[i] == 1 and \
               ord(src[CharLocs[i+1]]) - ord(src[CharLocs[i]]) == 1:
            # We find a pair of sequential chars!
            if not SeqChars:
                SeqChars = [src[CharLocs[i]], src[CharLocs[i+1]]]
            else:
                SeqChars.append(src[CharLocs[i+1]])
        else:
            if SeqChars:
                AllSeqChars.append(SeqChars)
                SeqChars = []
        i += 1
    if SeqChars:
        AllSeqChars.append(SeqChars)
    return AllSeqChars

def pwStrength(pw):
    Score = 0
    Length = len(pw)
    Score += Length * 4
    NUpper = 0
    NLower = 0
    NNum = 0
    NSymbol = 0
    LocUpper = []
    LocLower = []
    LocNum = []
    LocSymbol = []
    CharDict = {}
    for i in range(Length):
        Ch = pw[i]
        Code = ord(Ch)
        if Code >= 48 and Code <= 57:
            NNum += 1
            LocNum.append(i)
        elif Code >= 65 and Code <= 90:
            NUpper += 1
            LocUpper.append(i)
        elif Code >= 97 and Code <= 122:
            NLower += 1
            LocLower.append(i)
        else:
            NSymbol += 1
            LocSymbol.append(i)
        if not Ch in CharDict:
            CharDict[Ch] = 1
        else:
            CharDict[Ch] += 1
    if NUpper != Length and NLower != Length:
        if NUpper != 0:
            Score += (Length - NUpper) * 2
            # print("Upper case score:", (Length - NUpper) * 2)
        if NLower != 0:
            Score += (Length - NLower) * 2
            # print("Lower case score:", (Length - NLower) * 2)
    if NNum != Length:
        Score += NNum * 4
        # print("Number score:", NNum * 4)
    Score += NSymbol * 6
    # print("Symbol score:", NSymbol * 6)
    # Middle number or symbol
    Score += len([i for i in LocNum if i != 0 and i != Length - 1]) * 2
    # print("Middle number score:", len([i for i in LocNum if i != 0 and i != Length - 1]) * 2)
    Score += len([i for i in LocSymbol if i != 0 and i != Length - 1]) * 2
    # print("Middle symbol score:", len([i for i in LocSymbol if i != 0 and i != Length - 1]) * 2)
    # Letters only?
    if NUpper + NLower == Length:
        Score -= Length
        # print("Letter only:", -Length)
    if NNum == Length:
        Score -= Length
        # print("Number only:", -Length)
    # Repeating chars
    Repeats = 0
    for Ch in CharDict:
        if CharDict[Ch] > 1:
            Repeats += CharDict[Ch] - 1
    if Repeats > 0:
        Score -= int(Repeats / (Length - Repeats)) + 1
        # print("Repeating chars:", -int(Repeats / (Length - Repeats)) - 1)
    if Length > 2:
        # Consequtive letters
        for MultiLowers in re.findall(''.join(["[a-z]{2,", str(Length), '}']), pw):
            Score -= (len(MultiLowers) - 1) * 2
            # print("Consequtive lowers:", -(len(MultiLowers) - 1) * 2)
        for MultiUppers in re.findall(''.join(["[A-Z]{2,", str(Length), '}']), pw):
            Score -= (len(MultiUppers) - 1) * 2
            # print("Consequtive uppers:", -(len(MultiUppers) - 1) * 2)
        # Consequtive numbers
        for MultiNums in re.findall(''.join(["[0-9]{2,", str(Length), '}']), pw):
            Score -= (len(MultiNums) - 1) * 2
            # print("Consequtive numbers:", -(len(MultiNums) - 1) * 2)
        # Sequential letters
        LocLetters = (LocUpper + LocLower)
        LocLetters.sort()
        for Seq in findSeqChar(LocLetters, pw.lower()):
            if len(Seq) > 2:
                Score -= (len(Seq) - 2) * 2
                # print("Sequential letters:", -(len(Seq) - 2) * 2)
        # Sequential numbers
        for Seq in findSeqChar(LocNum, pw.lower()):
            if len(Seq) > 2:
                Score -= (len(Seq) - 2) * 2
                # print("Sequential numbers:", -(len(Seq) - 2) * 2)
    return Score

@login_required
def changepassword(request):
    context={}
    if request.method == "POST":
        if request.POST.get("newpassword",None) and request.POST.get("password",None):
            if authenticate(username=request.user.username, password=request.POST.get("password",None)):
                if pwStrength(request.POST.get("newpassword",""))>60:
                    user = request.user
                    user.set_password(request.POST["newpassword"])
                    user.save()
                    context['result'] = "گذر واژه با موفقیت تغییر کرد."
                    messages.error(request, 'گذر واژه با موفقیت تغییر کرد')
                else:
                    context['error'] = "گذر واژه ی جدید آسان می باشد."
                    messages.error(request, 'گذر واژه ی جدید آسان می باشد')
            else:
                context['error'] = "گذرواژه صحیح نیست."
                messages.error(request, 'گذرواژه صحیح نیست')
        else:
            context['error']="گذرواژه صحیح نیست."
            messages.error(request, 'گذرواژه صحیح نیست')
    return render(request,'tmp2/changepassword.html',context)

@login_required
def ViewQueue(request):
    context = {}
    if request.user.is_superuser:
        ln = Loan_queue.objects.filter()
        context['loanqueue'] = ln
    else:
        raise Http404("access denided")
    return render(request,'tmp2/loanqueue.html',context)

@login_required
def AddQueue(request):
    context = {}
    if request.user.is_superuser:
        bacc = bankaccount.objects.all()
        context['bacc'] = bacc
        if request.method == "POST":
            context['fadate'] = request.POST.get("date")
            context['date'] = (context['fadate']).split("/")
            context['date'] = jdatetime.date(int(context['date'][0]), int(context['date'][1]), int(context['date'][2]))
            context['date'] = context['date'].togregorian()
            if Loan_queue.objects.filter(bankaccount = bankaccount.objects.get(id=int(request.POST.get("acc"))),status__lt=1).exists() or int(request.POST.get("amount")) <=0:
                context['error']=True
            else:
                lq = Loan_queue()
                lq.date = context['date']
                lq.bankaccount = bankaccount.objects.get(id=int(request.POST.get("acc")))
                lq.amount = int(request.POST.get("amount"))
                lq.save()
                context['success'] = True
    else:
        raise Http404("access denided")
    return render(request, "tmp2/newqueue.html", context)

@login_required
def loan_new(request):
    context = {}
    if request.user.is_superuser:
        bacc = Loan_queue.objects.filter(status=-1)
        context['bacc'] = bacc
        if request.method == "POST":
            context['fadate'] = request.POST.get("date")
            context['date'] = (context['fadate']).split("/")
            context['date'] = jdatetime.date(int(context['date'][0]), int(context['date'][1]), int(context['date'][2]))
            context['date'] = context['date'].togregorian()
            if int(request.POST.get("peak")) <=0:
                context['error']=True
            else:
                lq = new_loan()
                lq.date = context['date']
                lq.loan_queue = Loan_queue.objects.get(id=int(request.POST.get("acc")))
                lq.peak = int(request.POST.get("peak"))
                lq.save()
                context['success'] = True
    else:
        raise Http404("access denided")
    return render(request,'tmp2/newloan.html',context)

@login_required
def loan(request):
    context = {}
    try:
        bk = bankaccount.objects.filter(user = request.user)
        lq = Loan_queue.objects.filter(bankaccount__in = bk)
        context['qloan'] = []
        for i in lq:
            tmp = new_loan.objects.filter(loan_queue=i)
            if tmp.exists():
                context['qloan'].append(tmp[0])
    except:
        pass
    print(context['qloan'])
    return render(request, 'tmp2/loan.html', context)
@login_required
def loan_admin(request):
    context = {}
    if request.user.is_superuser:
        context['loan'] = new_loan.objects.filter()
#        print(context['loan'][0].loan_queue)
    else:
        raise Http404("access denided")
    return render(request, 'tmp2/loan_admin.html', context)

@login_required
def view_loan_pay(request,id):
    context = {}
    context['loan'] = new_loan.objects.get(loan_queue__pk=id)
    if request.user.is_superuser:
        context['nlp'] = new_loan_pay.objects.filter(new_loan=context['loan'])
        print(context['nlp'])
    else:
        if context['loan'].loan_queue.bankaccount.user is not request.user:
            raise Http404("access denided")
    return render(request,'tmp2/listpeymentLoan.html',context)

@login_required
def add_loan_pay(request,id):
    context = {}
    if request.user.is_superuser:
        context['loan'] = new_loan.objects.get(loan_queue__pk=id)
        if context['loan'] == 1:
            return HttpResponseRedirect(request.GET.get("next", "/loan/view/"+id+"/"))
        elif request.method == "POST":
            context['fadate'] = request.POST.get("date")
            context['date'] = (context['fadate']).split("/")
            context['date'] = jdatetime.date(int(context['date'][0]), int(context['date'][1]), int(context['date'][2]))
            context['date'] = context['date'].togregorian()
            context['description'] = request.POST.get("description")
            nlp = new_loan_pay()
            nlp.date = context['date']
            nlp.description = context['description']
            nlp.new_loan = context['loan']
            nlp.save()
            context['loan'].UnpaidLoan()
            return HttpResponseRedirect(request.GET.get("next", "/loan/view/" + id + "/"))
    else:
        raise Http404("access denided")
    return render(request, 'tmp2/addpeymentToLoan.html', context)

@login_required
def active_telegram(request,key):
    try:
        tg = telegram_active.objects.get(key=key)
        request.user.telegramid=tg.telegramid
        request.user.save()
        reply_markup = {"keyboard":[["وضعیت حساب"],["وضعیت وام"]],"one_time_keyboard":True}
        SendMessage(request.user.telegramid,"تلگرام شما با موفقیت فعال شد.",reply_markup)
    except:
        pass
    return HttpResponseRedirect("/")

def reset_password_telegram(request,key):
    try:
        tg = telegram_active.objects.get(key=key)
        u = User.objects.get(telegramid = tg.telegramid)
        if u.password=="":
            newpass = str(uuid.uuid1())[:4]
            u.set_password(newpass)
            u.save()
            tg.key=None
            tg.save()
            reply_markup = {"keyboard":[["وضعیت حساب"],["وضعیت وام"]],"one_time_keyboard":True}
            SendMessage(u.telegramid,"پسورد جدید:"+newpass,reply_markup)
    except:
        pass
    return HttpResponseRedirect("/")

def aboutUs(request):
    return render(request, 'tmp2/aboutus.html')