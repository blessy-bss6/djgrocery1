# Generated by Django 4.0.4 on 2022-04-21 09:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('restapi', '0003_product_cartitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='upload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]