from django.urls import path,reverse_lazy
from accounts import views
from django.contrib.auth import views as auth_views

app_name="accounts"
urlpatterns=[

	path('',views.home,name="home"),
	path('products/',views.products,name="products"),
	path('customers/<int:pk>/',views.customers,name="customer"),
	path('create_order/<int:pk>/',views.CreateOrder,name="create-order"),
	path('update_order/<int:pk>/',views.UpdateOrder,name="update-order"),
	path('delete_order/<int:pk>/',views.DeleteOrder,name="delete-order"),
	path('register/',views.register,name="register"),
	path('login/',views.UserLogin,name="login"),
	path('logout/',views.UserLogout,name="logout"),
	path('user/',views.userpage,name="user"),
	path('account/',views.accountSettings,name='account'),

	#form-success-passwordForm-success
	#name=is defined you can't define of your own

]