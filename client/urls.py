from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index,name="home"),
    url(r'^accounts/login/', views.Login),
    url(r'^accounts/logout/', views.Logout, name="logout"),
    url(r'^accounts/changepassword/', views.changepassword,name="changepassword"),
#    url(r'^operator/(?P<page>[0-9a-z\.-]+)', views.operator,name='operator',),
]