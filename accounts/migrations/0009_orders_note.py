# Generated by Django 3.2.5 on 2021-12-09 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0008_alter_orders_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='note',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
