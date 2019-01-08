from django.core.management.base import BaseCommand, CommandError
from client.models import bankaccount,catch
from client.models import new_loan,new_loan_pay,Loan_queue,periodic_payment
import datetime
from bank.settings import BASE_DIR
import os
class Command(BaseCommand):
    # calculate point backaccounts
    file = open(os.path.join(BASE_DIR,"datetime.txt"),"r")
    datetimeset = file.read()
    file.close()
    datetimeset = datetimeset.split("-")
    datetimeset=datetime.date(int(datetimeset[0]),int(datetimeset[1]),int(datetimeset[2]))
    acc =  bankaccount.objects.all()
    for i in acc:
        try:
            loan = Loan_queue.objects.get(bankaccount=i,status=0)
            loan = new_loan.objects.get(loan_queue = loan,status=0)
            CountPayLoan = new_loan_pay.objects.filter(new_loan=loan,date__lte=datetimeset).count()
            if loan.loan_queue.amount % loan.peak > 0:
                CountAllLoan = loan.loan_queue.amount // loan.peak + 1
            else:
                CountAllLoan = loan.loan_queue.amount // loan.peak
            last_day_date_time = datetimeset - datetime.timedelta(days=1)
            if CountAllLoan == CountPayLoan:
                Negative_point = 0
            elif periodic_payment.objects.filter(datetime__lte=last_day_date_time,datetime__gte=loan.date).count()<=CountPayLoan:
                Negative_point = 0
            else:
                if periodic_payment.objects.filter(datetime__lte=last_day_date_time,datetime__gte=loan.date).count()>CountAllLoan:
                    Negative_point = CountAllLoan - CountPayLoan
                else:
                    Negative_point = periodic_payment.objects.filter(datetime__lte=last_day_date_time,datetime__gte=loan.date).count()-CountPayLoan
            Negative_point = Negative_point * loan.peak // 10
        except:
            Negative_point=0
        calsum = 0
        colcatchsum = catch.objects.raw('SELECT id,price/10 as price FROM client_catch WHERE  bankaccount_id = '+str(i.id)+" and date <'"+str(datetimeset)+"' GROUP BY id")
        for i in colcatchsum:
            calsum +=price
        i.points += int(calsum)
        i.points -= Negative_point
        i.save()
        print(i.id,"updated.")
    datetimeset = datetimeset + datetime.timedelta(days=1)
    file = open(os.path.join(BASE_DIR, "datetime.txt"), "w")
    file.write(str(datetimeset))
    file.close()
    print("date:" + str(datetimeset))
    print('the End')