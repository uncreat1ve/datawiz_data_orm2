from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^1/$', views.new),
    url(r'^2/$', views.slq_first),
    url(r'^3/$', views.sel_second),
    url(r'^4/$', views.three),
    url(r'^5/$', views.four),
    url(r'^6/$', views.five),
    url(r'^form_select/$', views.form_select, name='form_select'),

]
