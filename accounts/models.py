from django.db import models

# Create your models here.
from django.contrib.auth.models import User
class Customers(models.Model):
	user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)
	name= models.CharField(max_length=200,null=True)
	phone = models.CharField(max_length=200,null=True)
	email = models.EmailField(null=True)
	profile_pic = models.ImageField(default='default.jpg',null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True,null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Customer"
		verbose_name_plural="Customers"

	def get_orders(self):
		customer = Customers.objects.get(id=self.id)
		return str(customer.orders.all().count())

class Tag(models.Model):
	name=models.CharField(max_length=100,null=True)

	def __str__(self):
		return self.name


class Products(models.Model):
	CATEGORY = (
			('Indoor','Indoor'),
			('Outdoor','Outdoor'),
		)#same as below

	name = models.CharField(max_length=200,null=True)
	price = models.FloatField(null=True)
	category = models.CharField(max_length=200,null=True,choices=CATEGORY)
	description = models.TextField(max_length=200,null=True,blank=True)
	date_created = models.DateTimeField(auto_now_add=True)
	tag = models.ManyToManyField(Tag)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name="Product"
		verbose_name_plural="Products"



class Orders(models.Model):
	STATUS = (
			('pending','pending'),
			('Out for delivery','Out for delivery'),
			('Delivered','Delivered',),
		)#dropdown option in admin panel
	customer = models.ForeignKey(Customers,null=True,on_delete=models.SET_NULL,related_name="orders")
	product = models.ForeignKey(Products,null=True,on_delete=models.SET_NULL,related_name="orders")
	date_created = models.DateTimeField(auto_now_add=True,null=True)
	status = models.CharField(max_length=200,null=True,choices=STATUS)#dropdown option in admin panel
	note = models.CharField(max_length=100,null=True)

	def __str__(self):
		return str(self.id)

	class Meta:
		verbose_name="Order"
		verbose_name_plural="Orders"

	def __str__(self):
		return self.product.name