from django.contrib import admin
import locale
from .models import User,catch,Message,Loan,bankaccount,periodic_payment
from .models import new_loan,new_loan_pay,Loan_queue
import datetime
from django.contrib.auth.admin import UserAdmin
# Register your models here.
class CatchInline(admin.StackedInline):
    model = catch
    extra = 1
class loanPayInline(admin.StackedInline):
    model = new_loan_pay
    extra = 1
class UserAdmin2(UserAdmin):
    list_display=["username","email","first_name","last_name","is_active","is_staff","is_superuser","gender"]
    search_fields=["id","username","email","first_name","last_name"]
    list_filter=["is_active","is_staff","is_superuser","gender"]
    readonly_fields = ('username_clear',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                       'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Extra Information'), {'fields': ('image', 'birthday', 'cellphone', 'username_clear', 'telegramid', 'gender', 'codemelli')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2'),
        }),
    )
    pass


def BankaccoutName(obj):
    return ("%s %s" % (obj.user.first_name, obj.user.last_name))
def Inventory(obj):
    input = catch.objects.filter(bankaccount=obj)
    value=0
    for i in input:
        value += i.price
    locale.setlocale(locale.LC_ALL, 'fa_IR')
    return locale.currency( int(value)*10000, grouping=True )
def CountAllLoan(obj):
    if obj.status==1:
        return "done"
    if obj.peak ==0:
        return "Error"
    if obj.loan_queue.amount % obj.peak >0:
        value = obj.loan_queue.amount // obj.peak +1
    else:
        value= obj.loan_queue.amount // obj.peak
    return value
def CountPayLoan(obj):
    if obj.status==1:
        return "done"
    else:
        return new_loan_pay.objects.filter(new_loan=obj).count()
def UnpaidLoan(obj):
    if obj.status==1:
        return "done"
    else:
        if CountAllLoan(obj) == CountPayLoan(obj):
            obj.status=1
            obj.loan_queue.status=1
            obj.loan_queue.save()
            obj.save()
            return "0"
        elif periodic_payment.objects.filter(datetime__lte=datetime.datetime.now(),datetime__gte=obj.date).count()<=CountPayLoan(obj):
            return 0
        else:
            if periodic_payment.objects.filter(datetime__lte=datetime.datetime.now(),datetime__gte=obj.date).count()>CountAllLoan(obj):
                return CountAllLoan(obj) - CountPayLoan(obj)
            else:
                return periodic_payment.objects.filter(datetime__lte=datetime.datetime.now(),datetime__gte=obj.date).count()-CountPayLoan(obj)
def percentage(obj):
    bnk = bankaccount.objects.all()
    j=0
    for i in bnk:
        j += i.points
    if j:
        value = round(obj.points / j * 100,2)
    else:
        value = "تعریف نشده"
    return str(value)+"%"

class bankaccountAdmin(admin.ModelAdmin):
    search_fields=["user__username","user__first_name","user__last_name","name"]
    list_display=["name",BankaccoutName,Inventory,percentage]
    list_filter=["createTime"]
    inlines=[CatchInline,]
    readonly_fields = ('points',)

class catchAdmin(admin.ModelAdmin):
    search_fields=["bankaccount__user__username","bankaccount__user__first_name","bankaccount__user__last_name"]
    list_display=["bankaccount","date"]
    list_filter=["date"]
    pass

class catchLoan(admin.ModelAdmin):
    search_fields=["user__username","user__first_name","user__last_name"]
    list_display=["user","loan_amount","parts","part_amount","part_payed"]
    list_filter=["loan_amount"]
    pass
class new_LoanAdmin(admin.ModelAdmin):
    inlines=[loanPayInline,]
    list_display=["loan_queue","date",CountAllLoan,CountPayLoan,UnpaidLoan]
    list_filter=["date","status"]

class LoanQueueAdmin(admin.ModelAdmin):
    list_display=["bankaccount","date"]
    list_filter=["date","status"]

admin.site.register(bankaccount, bankaccountAdmin)
admin.site.register(User, UserAdmin2)
admin.site.register(catch,catchAdmin)
admin.site.register(Message)
admin.site.register(Loan,catchLoan)
admin.site.register(Loan_queue,LoanQueueAdmin)
admin.site.register(new_loan,new_LoanAdmin)
admin.site.register(periodic_payment)