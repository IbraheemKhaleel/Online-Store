# Generated by Django 3.2.6 on 2022-06-03 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_product_is_delete'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseproduct',
            name='is_paid',
            field=models.BooleanField(default=False),
        ),
    ]
