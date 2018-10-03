from django.db import models
from django.contrib.auth.models import AbstractUser
import requests,locale
from bank.settings import telegapiKey

# Create your models here.
def upload_to(instance,filename):
    return '%s/%s/%s'%("images/users/",instance.username,filename)
class User(AbstractUser):
    image = models.ImageField(upload_to=upload_to,blank=True)
    birthday=models.DateField(blank=True,null=True)
    cellphone = models.CharField(max_length=15,unique=True,null=True)
    username_clear = models.CharField(max_length=150,unique=True,null=True)
    telegramid = models.CharField(max_length=15,unique=True,null=True,blank=True,default=None)
    gender_list = (
        (True, 'Men'),
        (False, 'Women'),
    )
    gender=models.BooleanField(choices=gender_list,default=True)
    codemelli = models.CharField(max_length=12,unique=True,null=True,blank=True)
#     shenase_hesab = models.IntegerField(unique=True,null=True,blank=True)
class bankaccount(models.Model):
    user = models.ForeignKey(User)
    name = models.CharField(max_length=8,unique=True)
    createTime = models.DateTimeField(auto_now=True)
    count = models.IntegerField(default=0)
    points=models.IntegerField(default=0)
    def __str__(self):
        return self.name+" "+self.user.first_name+" "+self.user.last_name
class catch(models.Model):
    bankaccount = models.ForeignKey(bankaccount)
    date = models.DateTimeField(auto_now=True)
    price = models.FloatField()
    year = models.IntegerField(default=0)
    added_with_bank = models.BooleanField(default=False)
    def save(self):
        super(catch,self).save()
      
      
        locale.setlocale( locale.LC_ALL, 'fa_IR' )
        #locale.setlocale( locale.LC_ALL, 'fa' )
        
        price= self.price*10000
        if self.added_with_bank:
            reply_markup='{"keyboard":[["وضعیت حساب"],["وضعیت وام"]],"one_time_keyboard":true}'
            requests.post("https://api.telegram.org/bot"+telegapiKey+"/sendMessage", data = {'chat_id':self.bankaccount.user.telegramid,"text":"آقای  "+ self.bankaccount.user.first_name+"  "+self.bankaccount.user.last_name + " مبلغ  "+locale.currency( price, grouping=True )+" به عنوان سود سال "+str(self.year)+" به حساب شما با شماره حساب "+self.bankaccount.name+" واریز شد."})
        else:
            reply_markup='{"keyboard":[["وضعیت حساب"],["وضعیت وام"]],"one_time_keyboard":true}'
            #requests.post("https://api.telegram.org/bot"+telegapiKey+"/sendMessage", data = {'chat_id':self.user.telegramid,"text":"���� �����"})
            requests.post("https://api.telegram.org/bot"+telegapiKey+"/sendMessage", data = {'chat_id':self.bankaccount.user.telegramid,"text":"آقای  "+ self.bankaccount.user.first_name+"  "+self.bankaccount.user.last_name +   " مبلغ   "+locale.currency( price, grouping=True )+" به حساب شما با شماره حساب "+self.bankaccount.name+" واریز شد."})

class Message(models.Model):
    Text= models.TextField()
    def has_delete_permission(self, request, obj=None): # note the obj=None
        return False
    def save(self):
        super(Message,self).save()
        listuser= User.objects.all()
        for u in listuser:
            reply_markup='{"keyboard":[["وضعیت حساب"],["وضعیت وام"]],"one_time_keyboard":true}'
            requests.post("https://api.telegram.org/bot"+telegapiKey+"/sendMessage", data = {'chat_id':u.telegramid,"text":self.Text})
            
class Loan (models.Model):
    user =  models.ForeignKey(User) 
    loan_amount=   models.FloatField()
    parts=  models.IntegerField(default=10) 
    part_amount=models.FloatField()
    part_payed=models.IntegerField(default=1)
    start_date=models.DateTimeField(auto_now=True)
    send = models.BooleanField(default=False)
   
    def save(self):
        super(Loan,self).save()
      
        locale.setlocale( locale.LC_ALL, 'fa_IR' )

        loan_amount= (self.loan_amount*10000)
        part_amount=(self.part_amount*10000)
        
        if self.send:
            reply_markup='{"keyboard":[["وضعیت حساب"],["وضعیت وام"]],"one_time_keyboard":true}'
            
            mess="آقای  "+ self.user.first_name+" "+self.user.last_name + "  عزیز \n اطلاعات وام دریافتی شما  : \n"
            mess=mess+"مبلغ وام شما : "+locale.currency(loan_amount, grouping=True)+"\n"
            mess=mess+"تعداد وام های پرداختی : "+str(self.part_payed) + " از "+str(self.parts)+"\n"
            mess=mess+"مبلغ هر وام :"+ locale.currency(part_amount, grouping=True)+"\n "
            
            p1=self.part_payed * part_amount
            p2=loan_amount - p1
            mess=mess+" مبلغ پرداخت شده : "+locale.currency(p1, grouping=True)+" \n مبلغ باقی مانده : "+locale.currency(p2, grouping=True)
            
            requests.post("https://api.telegram.org/bot"+telegapiKey+"/sendMessage", data = {'chat_id':self.user.telegramid,"text":mess})
class Loan_queue(models.Model):
    Status_choice = (
        (-1, 'In Progress'),
        (0, 'Started'),
        (1, 'Done'),
    )
    bankaccount = models.ForeignKey(bankaccount)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status_choice,default=-1)
    amount = models.IntegerField()
    def __str__(self):
        return self.bankaccount.name+" "+self.bankaccount.user.first_name+" "+self.bankaccount.user.last_name
class new_loan(models.Model):
    Status_choice = (
        (0, 'Started'),
        (1, 'Done'),
    )
    loan_queue = models.OneToOneField(Loan_queue,on_delete=models.CASCADE,primary_key=True)
    peak = models.IntegerField(default=0)
    date = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=Status_choice,default=0)
    def save(self, *args, **kwargs):
        self.loan_queue.status=0
        self.loan_queue.save()
        super(new_loan, self).save(*args, **kwargs)


class new_loan_pay(models.Model):
    new_loan = models.ForeignKey(new_loan)
    date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(default="",max_length=20)
    def save(self,*args , **kwargs):
        super(new_loan_pay, self).save(*args, **kwargs)
        locale.setlocale(locale.LC_ALL, 'fa_IR')
        mess = "آقای  " + self.new_loan.loan_queue.bankaccount.user.first_name + " " + self.new_loan.loan_queue.bankaccount.user.last_name  + "  عزیز \n اطلاعات وام دریافتی شما  : \n"
        mess = mess + "مبلغ وام شما : " + locale.currency(self.new_loan.loan_queue.amount*10000, grouping=True) + "\n"
        mess = mess + "مبلغ پرداختی شما : " + locale.currency(self.new_loan.peak*10000, grouping=True) + "\n"
        p1 = self.new_loan.peak * len(new_loan_pay.objects.filter(new_loan = self.new_loan)) *10000
        p2 = self.new_loan.loan_queue.amount *10000 - p1
        mess = mess + " مبلغ پرداخت شده : " + locale.currency(p1,grouping=True) + " \n مبلغ باقی مانده : " + locale.currency(p2, grouping=True)
        mess = mess +"\n شماره تراکنش:"+str(self.id)
        requests.post("https://api.telegram.org/bot" + telegapiKey + "/sendMessage",
                      data={'chat_id': self.new_loan.loan_queue.bankaccount.user.telegramid, "text": mess})
class periodic_payment(models.Model):
    datetime = models.DateTimeField()

def currency(val, symbol=True, grouping=False, international=False):
   
   numb=str(locale.currency(val,symbol=False,grouping=grouping))
   numb = numb[:-3] +' ریال'
   return numb