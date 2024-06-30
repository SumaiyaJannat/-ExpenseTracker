from django.shortcuts import render,HttpResponse,redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate ,logout
from django.contrib.auth import login as dj_login
from django.contrib.auth.models import User
from .models import UserProfile,Category,Expense, Budget
from django.contrib.sessions.models import Session
from django.core.paginator import Paginator, EmptyPage , PageNotAnInteger
from django.db.models import Sum
from django.http import JsonResponse
import datetime
from django.utils import timezone
from .forms import EditExpenseForm,EditBudgetForm, EditCategoryForm,AddMoneyForm, AddBudgetForm
# Create your views here.

def register(request):
    return render(request,'home/register.html')
def home(request):
    if request.session.has_key('is_logged'):
        return redirect('/index')
    return render(request,'home/login.html')
  
def index(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        addmoney_info = Expense.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(addmoney_info , 4)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {
           'page_obj' : page_obj
        }
        return render(request,'home/index.html',context)
    return redirect('home')


def budget(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        addbudget_info = Budget.objects.filter(user=user)
        paginator = Paginator(addbudget_info , 4)
        page_number = request.GET.get('page')
        page_obj = Paginator.get_page(paginator,page_number)
        context = {
        
           'page_obj' : page_obj
        }
  
        return render(request,'home/budget.html',context)
    return redirect('home')
def category_list(request):
    if request.session.has_key('is_logged'):
        categories = Category.objects.all().order_by('name') 
       
        return render(request, 'home/category.html', {'categories': categories})
    
    return redirect('home')

       
def password(request):
    return render(request,'home/password.html')

def search(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        fromdate = request.GET['fromdate']
        todate = request.GET['todate']
        addmoney = Expense.objects.filter(user=user, Date__range=[fromdate,todate]).order_by('-Date')
        return render(request,'home/tables.html',{'addmoney':addmoney})
    return redirect('home')

def tables(request):
    if request.session.has_key('is_logged'):
        user_id = request.session["user_id"]
        user = User.objects.get(id=user_id)
        fromdate = request.POST.get('fromdate')
        todate = request.POST.get('todate')
        addmoney = Expense.objects.filter(user=user).order_by('-Date')
        return render(request,'home/tables.html',{'addmoney':addmoney})
    return redirect('home')

def add_category(request):
    return render(request,'home/addcategory.html')

def profile(request):
    if request.session.has_key('is_logged'):
        return render(request,'home/profile.html')
    return redirect('/home')

def profile_edit(request,id):
    if request.session.has_key('is_logged'):
        add = User.objects.get(id=id)
        # user_id = request.session["user_id"]
        # user1 = User.objects.get(id=user_id)
        return render(request,'home/profile_edit.html',{'add':add})
    return redirect("/home")

def profile_update(request,id):
    if request.session.has_key('is_logged'):
        if request.method == "POST":
            user = User.objects.get(id=id)
            user.first_name = request.POST["fname"]
            user.last_name = request.POST["lname"]
            user.email = request.POST["email"]
            user.userprofile.Savings = request.POST["Savings"]
            user.userprofile.income = request.POST["income"]
            user.userprofile.profession = request.POST["profession"]
            user.userprofile.save()
            user.save()
            return redirect("/profile")
    return redirect("/home")   

def Signup(request):
    if request.method =='POST':
            username = request.POST["uname"]
            firstname=request.POST["fname"]
            lastname=request.POST["lname"]
            email = request.POST["email"]
            profession = request.POST['profession']
            pass1 = request.POST["pass1"]
            pass2 = request.POST["pass2"]
            profile = UserProfile(profession=profession)
           
            if request.method == 'POST':
                try:
                    user_exists = User.objects.get(username=request.POST['userame'])
                    messages.error(request," Username already taken, Try something else!!!")
                    return redirect("/register")    
                except User.DoesNotExist:
                    if len(username)>15:
                        messages.error(request," Username must be max 15 characters, Please try again")
                        return redirect("/register")
            
                    if not username.isalnum():
                        messages.error(request," Username should only contain letters and numbers, Please try again")
                        return redirect("/register")
            
                    if pass1 != pass2:
                        messages.error(request," Password do not match, Please try again")
                        return redirect("/register")
            
          
            user = User.objects.create_user(username, email, pass1)
            user.first_name=firstname
            user.last_name=lastname
            user.email = email
           

            user.save()
            profile.user = user
            profile.save()
            messages.success(request," Your account has been successfully created")
            return redirect("/")
    else:
        return HttpResponse('404 - NOT FOUND ')
    return redirect('/login')

def login(request):
    if request.method =='POST':
        # get the post parameters
        loginuname = request.POST["loginuname"]
        loginpassword1=request.POST["loginpassword1"]
        user = authenticate(username=loginuname, password=loginpassword1)
        if user is not None:
            dj_login(request, user)
            request.session['is_logged'] = True
            user = request.user.id 
            request.session["user_id"] = user
            messages.success(request, " Successfully logged in")
            return redirect('/index')
        else:
            messages.error(request," Invalid Credentials, Please try again")  
            return redirect("/")  
    return HttpResponse('404-not found')
def Logout(request):
        del request.session['is_logged']
        del request.session["user_id"] 
        logout(request)
        messages.success(request, " Successfully logged out")
        return redirect('home')

def add_category(request):
 if request.session.has_key('is_logged'):
    if request.method == 'POST':
        name = request.POST['name']
        is_active = request.POST['is_active'] == 'true'
        category = Category(name=name, is_active=is_active)
        category.save()
        
        return redirect('category_list')
    return render(request, 'home/addcategory.html')


def addmoney(request):
    
    if request.method == 'POST':
        form = AddMoneyForm(request.POST)
        if form.is_valid():
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            
            title = form.cleaned_data["title"]
            quantity = form.cleaned_data["quantity"]
            Date = form.cleaned_data["Date"]
            category = form.cleaned_data["category"]
            
            add = Expense(user=user1, title=title, quantity=quantity, Date=Date, category=category)
            add.save()
          # Check if total expenses exceed the budget for this category
            total_expense = Expense.objects.filter(user=user1, category=category).aggregate(Sum('quantity'))['quantity__sum'] or 0
            budget = Budget.objects.filter(user=user1, category=category).first()
            if budget and total_expense > budget.budget_limit:
                messages.error(request, f"Alert: Your total expenses for {category.name} have exceeded your budget limit.")
    
            return redirect('/')
        else:
            print(form.errors)  
    else:
        form = AddMoneyForm()
    context = {
        'form': form,
        'categories': Category.objects.all(), 
    }
    return render(request, 'home/addmoney.html', context)

def addbudget(request):
    if request.method == 'POST':
        form = AddBudgetForm(request.POST)
        if form.is_valid():
            user_id = request.session["user_id"]
            user1 = User.objects.get(id=user_id)
            budget_limit = form.cleaned_data["budget_limit"]
            category = form.cleaned_data["category"]  
            add = Budget(user=user1, budget_limit=budget_limit, category=category)
            add.save()
            
            # Redirect to the same page with a GET request to clear the form
            return redirect('budget')
        else:
            print(form.errors)  
    else:
        form = AddBudgetForm()
    context = {
        'form': form,
        'categories': Category.objects.all(),  
    }
    return render(request, 'home/add_budget.html', context)

def addmoney_update(request, id):
    if request.session.has_key('is_logged'):
        add = get_object_or_404(Expense, id=id)
        if request.method == "POST":
            form = EditExpenseForm(request.POST, instance=add)
            if form.is_valid():
                form.save()
                return redirect("/index")
        else:
            form = EditExpenseForm(instance=add)
        return render(request, 'home/expense_edit.html', {'form': form, 'addmoney_info': add})
    return redirect("/home")

def expense_edit(request, id):
    if request.session.has_key('is_logged'):
        addmoney_info = get_object_or_404(Expense, id=id)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        form = EditExpenseForm(instance=addmoney_info)
        return render(request, 'home/expense_edit.html', {'form': form, 'addmoney_info': addmoney_info})
    return redirect("/index")
def expense_delete(request,id):
    if request.session.has_key('is_logged'):
        addmoney_info = Expense.objects.get(id=id)
        addmoney_info.delete()
        return redirect("/index")
    return redirect("/home")  

def addbudget_update(request, id):
    if request.session.has_key('is_logged'):
        add = get_object_or_404(Budget, id=id)
        if request.method == "POST":
            form = EditBudgetForm(request.POST, instance=add)
            if form.is_valid():
                form.save()
                return redirect("/budget")
        else:
            form = EditBudgetForm(instance=add)
        return render(request, 'home/budget_edit.html', {'form': form, 'addbudget_info': add})
    return redirect("/home")

def budget_edit(request, id):
    if request.session.has_key('is_logged'):
        addbudget_info = get_object_or_404(Budget, id=id)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        form = EditBudgetForm(instance=addbudget_info)
        return render(request, 'home/budget_edit.html', {'form': form, 'addbudget_info': addbudget_info})
    return redirect("/budget")

def budget_delete(request,id):
    if request.session.has_key('is_logged'):
        addbudget_info = Budget.objects.get(id=id)
        addbudget_info.delete()
        return redirect("/budget")
    return redirect("/home")  

def addcategory_update(request, id):
    if request.session.has_key('is_logged'):
        add = get_object_or_404(Category, id=id)
        if request.method == "POST":
            form = EditCategoryForm(request.POST, instance=add)
            if form.is_valid():
                form.save()
                return redirect("/category")
        else:
            form = EditBudgetForm(instance=add)
        return render(request, 'home/category_edit.html', {'form': form, 'addcategory_info': add})
    return redirect("/home")

def category_edit(request, id):
    if request.session.has_key('is_logged'):
        addcategory_info = get_object_or_404(Category, id=id)
        user_id = request.session["user_id"]
        user1 = User.objects.get(id=user_id)
        form = EditCategoryForm(instance=addcategory_info)
        return render(request, 'home/category_edit.html', {'form': form, 'addcategory_info': addcategory_info})
    return redirect("/category")

def category_delete(request,id):
    if request.session.has_key('is_logged'):
        addcategory_info = Category.objects.get(id=id)
        addcategory_info.delete()
        return redirect("/category")
    return redirect("/home")  

def expense_budget_summary(request):
    categories = Category.objects.filter(is_active=True).order_by('name')
    category_summaries = []

    for category in categories:
        total_expense = Expense.objects.filter(category=category).aggregate(Sum('quantity'))['quantity__sum'] or 0
        budget = Budget.objects.filter(category=category).first()
        budget_limit = budget.budget_limit if budget else 0

        # Calculate remaining budget
        remaining_budget = budget_limit - total_expense


        category_summary = {
            'category': category,
            'total_expense': total_expense,
            'budget_limit': budget_limit,
            'remaining_budget': remaining_budget,
        }
        category_summaries.append(category_summary)

    context = {
        'category_summaries': category_summaries,
    }

    return render(request, 'home/summary.html', context)
