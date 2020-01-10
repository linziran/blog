
from django.urls import path
from blog.views import *

urlpatterns = [
    path('',index,name='index'),
    path('archive/',archive,name='archive'),
    path('article/',article,name='article'),
    path('commentpost/',comment_post,name='comment_post'),
    path('logout/',do_logout,name='do_logout'),
    path('reg/',do_reg,name='reg'),
    path('login/',do_login,name='login')
]
