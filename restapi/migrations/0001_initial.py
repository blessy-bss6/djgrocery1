# Generated by Django 4.0.4 on 2022-05-13 10:31

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import restapi.managers
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('phone', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^[789]\\d{9}$')])),
                ('fullname', models.CharField(blank=True, max_length=130, null=True, verbose_name='full name')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='emailaddress')),
                ('is_phone_verfied', models.BooleanField(default=False)),
                ('is_staff', models.BooleanField(default=False, verbose_name='is_staff')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('date_joined', models.DateField(default=datetime.date.today, verbose_name='date_joined')),
                ('change_pw', models.BooleanField(default=True)),
                ('isIdType', models.BooleanField(blank=True, default=False, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Accounts',
                'verbose_name_plural': 'Acconts',
                'ordering': ('id',),
            },
            managers=[
                ('objects', restapi.managers.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('fullname', models.CharField(max_length=130, verbose_name='full name')),
                ('phone', models.CharField(max_length=15, validators=[django.core.validators.RegexValidator('^[789]\\d{9}$')])),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='emailaddress')),
                ('house', models.CharField(blank=True, max_length=300, null=True)),
                ('trade', models.CharField(blank=True, max_length=200, null=True)),
                ('area', models.CharField(blank=True, max_length=200, null=True)),
                ('city', models.CharField(blank=True, max_length=100, null=True)),
                ('pinCode', models.CharField(max_length=100, validators=[django.core.validators.RegexValidator('^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$')])),
                ('delTime', models.CharField(default='AnyTime', max_length=100)),
                ('state', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='CartProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('salesPrice', models.FloatField(default=0)),
                ('discountPrice', models.FloatField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('offPrice', models.FloatField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='MobileOtp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone', models.CharField(max_length=15, unique=True, validators=[django.core.validators.RegexValidator('^[789]\\d{9}$')])),
                ('otp', models.CharField(max_length=6)),
                ('is_phone_verfied', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('selOrderStatus', models.CharField(blank=True, max_length=100, null=True)),
                ('ammount', models.FloatField(default=0)),
                ('shipPrice', models.FloatField(default=50)),
                ('totalAmmount', models.FloatField(default=0)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('ref_code', models.CharField(blank=True, max_length=20, null=True)),
                ('transcationId', models.CharField(blank=True, max_length=30, null=True)),
                ('being_delivered', models.BooleanField(default=False)),
                ('received', models.BooleanField(default=False)),
                ('refund_requested', models.BooleanField(default=False)),
                ('refund_granted', models.BooleanField(default=False)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restapi.address')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=300)),
                ('salesPrice', models.FloatField()),
                ('discountPrice', models.FloatField()),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('stock', models.PositiveIntegerField()),
                ('pic', models.FileField(blank=True, null=True, upload_to='ProdcutImg')),
                ('pic1', models.FileField(blank=True, null=True, upload_to='ProdcutImg')),
                ('pic2', models.FileField(blank=True, null=True, upload_to='ProdcutImg')),
                ('pic3', models.FileField(blank=True, null=True, upload_to='ProdcutImg')),
                ('offers', models.IntegerField(blank=True, default=1, null=True)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('ammount', models.PositiveIntegerField(default=0)),
                ('cartItem', models.BooleanField(default=False)),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restapi.category')),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.order')),
            ],
        ),
        migrations.CreateModel(
            name='ProfileWishList',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ammount', models.FloatField(default=0)),
                ('shipPrice', models.FloatField(default=50)),
                ('totalAmmount', models.FloatField(default=0)),
                ('upload', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileSeller',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('isSeller', models.BooleanField(default=False)),
                ('fullname', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='emailaddress')),
                ('gender', models.CharField(blank=True, max_length=200, null=True)),
                ('businesspic', models.ImageField(blank=True, null=True, upload_to='SellerImg')),
                ('businessname', models.CharField(blank=True, max_length=100, null=True)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='SellerImg')),
                ('upload', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileCart',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('ammount', models.FloatField(default=0)),
                ('shipPrice', models.FloatField(default=50)),
                ('totalAmmount', models.FloatField(default=0)),
                ('offPrice', models.FloatField(default=0)),
                ('cartUpload', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restapi.cartproduct')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='seller', to=settings.AUTH_USER_MODEL)),
                ('upload', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customer', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.UUIDField(primary_key=True, serialize=False)),
                ('isIdType', models.BooleanField(blank=True, default=False, null=True)),
                ('fullname', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='emailaddress')),
                ('gender', models.CharField(blank=True, max_length=200, null=True)),
                ('pic', models.ImageField(blank=True, null=True, upload_to='CustomerImg')),
                ('businesspic', models.ImageField(blank=True, null=True, upload_to='SellerImg')),
                ('businessname', models.CharField(blank=True, max_length=100, null=True)),
                ('upload', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stripe_charge_id', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('order_id', models.UUIDField(blank=True, default=uuid.uuid4, editable=False, null=True)),
                ('status', models.CharField(default='Pending', max_length=100)),
                ('selOrderStatus', models.CharField(blank=True, max_length=100, null=True)),
                ('ammount', models.FloatField(default=0)),
                ('shipPrice', models.FloatField(default=50)),
                ('totalAmmount', models.FloatField(default=0)),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('end_date', models.DateTimeField(blank=True, null=True)),
                ('ref_code', models.CharField(blank=True, max_length=20, null=True)),
                ('being_delivered', models.BooleanField(default=False)),
                ('received', models.BooleanField(default=False)),
                ('refund_requested', models.BooleanField(default=False)),
                ('refund_granted', models.BooleanField(default=False)),
                ('address', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restapi.address')),
                ('cartUpload', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restapi.profilecart')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restapi.coupon')),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restapi.product')),
                ('seller', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sellerOrderItem', to=settings.AUTH_USER_MODEL)),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='cartUpload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.profilecart'),
        ),
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restapi.coupon'),
        ),
        migrations.AddField(
            model_name='order',
            name='orderItem',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restapi.orderitem'),
        ),
        migrations.AddField(
            model_name='order',
            name='payment',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='restapi.payment'),
        ),
        migrations.AddField(
            model_name='order',
            name='upload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customerOrder', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('checked', models.BooleanField(default=False)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('msg', models.TextField()),
                ('recevier', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sellerNotification', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='customerNotification', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='cartProfile',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='restapi.profilecart'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.product'),
        ),
        migrations.AddField(
            model_name='cartproduct',
            name='upload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='address',
            name='upload',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addressuser', to='restapi.profile'),
        ),
        migrations.CreateModel(
            name='WishListProduct',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('salesPrice', models.FloatField(default=0)),
                ('discountPrice', models.FloatField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='restapi.product')),
                ('upload', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('upload', 'product')},
            },
        ),
        migrations.AlterUniqueTogether(
            name='cartproduct',
            unique_together={('upload', 'product')},
        ),
    ]
