from django.urls import path

from ToDoapp import views

urlpatterns = [
    path('',views.log_fun,name="log"),
    path('login',views.login_fun),

    path('regpage',views.regpage,name="reg"),
    path('regdata',views.regdata,name='regd'),

    path('home',views.home_fun,name="tasklist"),
    path('add',views.add_task,name='add_task'),
    path('edit/<int:pk>',views.edit_task,name='edit_task'),
    path('delete/<int:pk>',views.delete_task,name='delete_task')
]