from django.shortcuts import render,redirect

# Create your views here.
from django.http import HttpResponse
from accounts.models import *
from .forms import *

from .filters import *

from django.forms import inlineformset_factory

from django.contrib.auth.forms import UserCreationForm

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout

from django.contrib.auth.decorators import login_required

from accounts.decorators import *

from django.contrib.auth.models import Group

@unauthenticated_user #not gonna let see register to authenticated user
def register(request):
	form = CreateUserForm()
	if request.method == 'POST':
		form = CreateUserForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request,"Account has been created for " + form.cleaned_data.get('username'))
			return redirect('accounts:login')
	context={
		'form':form,
	}
	return render(request,"accounts/register.html",context)

@unauthenticated_user
def UserLogin(request):
	if request.method=="POST":
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request,username=username,password=password)
		if user is not None:
			login(request,user)
			return redirect('accounts:home')
		else:
			messages.info(request,'Username or password is incorrect')
	context={}
	return render(request,'accounts/login.html',context)

def UserLogout(request):
	logout(request)
	return redirect('accounts:login')

@login_required(login_url="accounts:login")
@admin_only
def home(request):
	customers = Customers.objects.all()
	orders = Orders.objects.all()
	orders_delivered = orders.filter(status="Delivered").count()
	orders_pending = orders.filter(status="pending").count()

	context = {
		'customers':customers,
		'orders':orders,
		'orders_delivered':orders_delivered,
		'orders_pending':orders_pending,
	}
	return render(request,'accounts/dashboard.html',context)

@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['customer'])
def userpage(request):
	orders = request.user.customers.orders.all()
	orders_delivered = orders.filter(status="Delivered").count()
	orders_pending = orders.filter(status="pending").count()
	#print(orders)
	context={
		'orders':orders,
		'orders_delivered':orders_delivered,
		'orders_pending':orders_pending,
	}
	return render(request,'accounts/userpage.html',context)

@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['admin'])
def products(request):
	products=Products.objects.all()
	context = {
		'products':products,
	}
	return render(request,'accounts/products.html',context)

@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['admin'])
def customers(request,pk):
	customer = Customers.objects.get(id=pk)
	orders = Orders.objects.filter(customer=customer)
	myFilter = OrderFilter(request.GET,queryset = orders)
	orders = myFilter.qs
	#orders=customer.orders.all()
	context = {
		'customer':customer,
		'orders':orders,
		'myFilter':myFilter,
	}
	return render(request,'accounts/customers.html',context)

@login_required
@allowed_users(allowed_roles=['customer'])
def accountSettings(request):
	customer = request.user.customers
	if request.method=='POST':
		form = CustomerForm(request.POST,request.FILES,instance=customer)
		if form.is_valid():
			form.save()
	else:
		form = CustomerForm(instance=customer)
	context={
		'form':form,
	}
	return render(request,'accounts/accountSettings.html',context)


@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['admin'])
def CreateOrder(request,pk):
	OrderFormSet = inlineformset_factory(Customers,Orders,fields=('product','status'),extra=5)
	customer = Customers.objects.get(id=pk)
	formset = OrderFormSet(queryset=Orders.objects.none(),instance = customer)
	if request.method=="POST":
		#print("printing",request.POST)
		#form = OrderForm(request.POST)
		formset = OrderFormSet(request.POST,instance=customer)
		if formset.is_valid():
			#form.save()#saves the data
			formset.save()
			return redirect('accounts:customer',pk=pk)
	else:
		form = OrderForm(initial={'customer':customer})
	context = {
		'formset':formset,
	}

	return render(request,'accounts/order_form.html',context)

@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['admin'])
def UpdateOrder(request,pk):
	order = Orders.objects.get(id=pk)
	if request.method=="POST":
		form = OrderForm(request.POST,instance=order)
		if form.is_valid():
			form.save()
			return redirect("accounts:home")
	else:
		form = OrderForm(instance=order)
	context={
		'form':form,
	}

	return render(request,'accounts/update_order_form.html',context)

@login_required(login_url="accounts:login")
@allowed_users(allowed_roles=['admin'])
def DeleteOrder(request,pk):
	order = Orders.objects.get(id=pk)
	if request.method=="POST":
		order.delete()
		return redirect('accounts:home')
	context = {
		'order':order,
	}
	return render(request,'accounts/delete.html',context)
