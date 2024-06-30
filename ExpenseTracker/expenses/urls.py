from django.contrib import admin
from django.urls import path
from django.urls import include
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('index/', views.index, name='index'),
    path('register/',views.register,name='register'),
    path('Signup/',views.Signup,name='Signup'),
    path('login/',views.login,name='login'),
    path('Logout/',views.Logout,name='Logout'),
    path('addmoney/',views.addmoney,name='addmoney'),
    path('addbudget/',views.addbudget,name='addbudget'),
    path('addcategory/',views.add_category,name='addcategory'),
    path('tables/',views.tables,name='tables'),
    path('expense_edit/<int:id>',views.expense_edit,name='expense_edit'),
    path('<int:id>/addmoney_update/', views.addmoney_update, name="addmoney_update") ,
    path('expense_delete/<int:id>',views.expense_delete,name='expense_delete'),
    path('budget_edit/<int:id>',views.budget_edit,name='budget_edit'),
    path('<int:id>/addbudget_update/', views.addbudget_update, name="addbudget_update") ,
    path('budget_delete/<int:id>',views.budget_delete,name='budget_delete'),
    path('category_edit/<int:id>',views.category_edit,name='category_edit'),
    path('<int:id>/addcategory_update/', views.addcategory_update, name="addcategory_update") ,
    path('category_delete/<int:id>',views.category_delete,name='category_delete'),
    path('profile/',views.profile,name = 'profile'),
    path('budget/', views.budget, name='budget'),
    path('category/', views.category_list, name='category_list'),
    path('search/',views.search,name="search"),
    path('<int:id>/profile_edit/',views.profile_edit,name="profile_edit"),
    path('<int:id>/profile_update/',views.profile_update,name="profile_update"),
    path('summary/', views.expense_budget_summary, name='summary'),
   
]
