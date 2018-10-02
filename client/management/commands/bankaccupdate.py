from django.core.management.base import BaseCommand, CommandError
from client.models import bankaccount,catch
from client.models import new_loan,new_loan_pay,Loan_queue,periodic_payment
import datetime

class Command(BaseCommand):
    # calculate point backaccounts
    acc =  bankaccount.objects.all()
    for i in acc:
        try:
            loan = Loan_queue.objects.get(bankaccount=i,status=0)
            loan = new_loan.objects.get(loan_queue = loan,status=0)
            CountPayLoan = new_loan_pay.objects.filter(new_loan=loan).count()
            if loan.loan_queue.amount % loan.peak > 0:
                CountAllLoan = loan.loan_queue.amount // loan.peak + 1
            else:
                CountAllLoan = loan.loan_queue.amount // loan.peak
            last_day_date_time = datetime.datetime.now() - datetime.timedelta(days=1)
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
        i.points += int(catch.objects.raw('SELECT id,sum(price)/10 as sum FROM client_catch WHERE  `bankaccount_id` = '+str(i.id))[0].sum)
        i.points -= Negative_point
        i.save()
        print(i.id,"updated.")
    print('the End')