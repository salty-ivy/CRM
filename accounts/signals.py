from django.db.models.signals import post_save
from django.contrib.auth.models import User ,Group
from .models import *
from django.dispatch import receiver

@receiver(post_save,sender=User)
def customer_profile(sender , instance,created,**kwargs):
	if created:
		group = Group.objects.get(name="customer")
		instance.groups.add(group)
		Customers.objects.create(user=instance,email=instance.email,name=instance.username)
		print("profile created")

#post_save.connect(customer_profile,sender=User)