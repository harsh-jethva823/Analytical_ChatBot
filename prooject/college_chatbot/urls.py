from django.urls import path
from . import views

app_name = 'college_chatbot'

urlpatterns = [
    path('', views.chat_interface, name='chat_interface'),
    path('keyword-chart/', views.keyword_chart, name='keyword_chart'),
    path('show-keywords/', views.show_chart_page, name='show_chart'),

]