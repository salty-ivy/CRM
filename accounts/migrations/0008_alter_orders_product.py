# Generated by Django 3.2.5 on 2021-12-07 19:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_auto_20211207_1826'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='orders', to='accounts.products'),
        ),
    ]
