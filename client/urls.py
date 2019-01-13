from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index,name="home"),
    url(r'^accounts/login/$', views.Login),
    url(r'^accounts/logout/$', views.Logout, name="logout"),
    url(r'^accounts/changepassword/$', views.changepassword,name="changepassword"),
    url(r'^accounts/bankacc/(?P<id>[\w-]+)/$', views.bankacc,name="bankacc"),
    url(r'^accounts/bankacc/$', views.bankaccs, name="bankaccs"),
    url(r'^loan/queue/$', views.ViewQueue, name="loan_queue"),
    url(r'^loan/queue/add/$', views.AddQueue, name="loan_queue_add"),
    url(r'^loan/new/$', views.loan_new, name="loan_new"),
    url(r'^loan/admin/$', views.loan_admin, name="loan_admin"),
    url(r'^loan/view/(?P<id>[\w-]+)/$', views.view_loan_pay, name="view_loan_pay"),
    url(r'^loan/add/(?P<id>[\w-]+)/$', views.add_loan_pay, name="add_loan_pay"),
    url(r'^activate/telegram/(?P<key>[\w-]+)/$', views.active_telegram),
    url(r'^resetpassword/telegram/(?P<key>[\w-]+)/$', views.reset_password_telegram),
    url(r'^loan/$', views.loan, name="loan"),
#    url(r'^operator/(?P<page>[0-9a-z\.-]+)', views.operator,name='operator',),
]
