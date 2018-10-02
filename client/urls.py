from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^login/', views.Login),
    url(r'^signup/', views.SingUp),
    url(r'^logout/', views.Logout),
#    url(r'^operator/(?P<page>[0-9a-z\.-]+)', views.operator,name='operator',),
]