# Generated by Django 2.2.4 on 2019-12-15 01:59

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('tipi', models.CharField(default='0', max_length=2)),
                ('durum', models.CharField(default='0', max_length=2)),
                ('aktif_firma', models.IntegerField(default=0)),
                ('aktif_teslimat', models.IntegerField(default=0)),
                ('aktif_islem', models.IntegerField(default=0)),
                ('sira', models.IntegerField(default=0)),
                ('enlem', models.DecimalField(decimal_places=12, default='0.0', max_digits=16)),
                ('boylam', models.DecimalField(decimal_places=12, default='0.0', max_digits=16)),
                ('aktif', models.BooleanField(default=True)),
                ('tel_no', models.CharField(default='', max_length=10)),
                ('pin', models.CharField(default='', max_length=6)),
                ('kaydolunan_restoranlar', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('device_platform', models.CharField(choices=[('0', 'Android'), ('1', 'IOS')], default='0', max_length=1)),
                ('device_id', models.CharField(default='0', max_length=100)),
                ('pic_profile', models.ImageField(blank=True, null=True, upload_to='pic_profile/%Y/%m/%d/')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='AnaFirma',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('anafirma_adi', models.CharField(max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Fiyat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_motorcu', models.PositiveIntegerField(default=0)),
                ('fiyat', models.PositiveIntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Il',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('il', models.CharField(default='İstanbul', max_length=80)),
            ],
        ),
        migrations.CreateModel(
            name='Ilce',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ilce', models.CharField(default='Kadıköy', max_length=80)),
                ('il', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ilce_il', to='kurye.Il')),
            ],
        ),
        migrations.CreateModel(
            name='Firma',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('firma_adi', models.CharField(max_length=80)),
                ('tel_no', models.CharField(default='', max_length=10)),
                ('pin', models.CharField(default='', max_length=6)),
                ('allow_self_delivery', models.BooleanField(default=False)),
                ('kayitli_motorcular', django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), blank=True, null=True, size=None)),
                ('adres', models.TextField()),
                ('mahalle', models.CharField(max_length=80)),
                ('ilce', models.CharField(max_length=80)),
                ('il', models.CharField(max_length=80)),
                ('enlem', models.DecimalField(decimal_places=12, default='0.0', max_digits=16)),
                ('boylam', models.DecimalField(decimal_places=12, default='0.0', max_digits=16)),
                ('belge_1', models.ImageField(blank=True, null=True, upload_to='belge_1/%Y/%m/%d/')),
                ('belge_2', models.ImageField(blank=True, null=True, upload_to='belge_2/%Y/%m/%d/')),
                ('belge_3', models.ImageField(blank=True, null=True, upload_to='belge_3/%Y/%m/%d/')),
                ('belge_4', models.ImageField(blank=True, null=True, upload_to='belge_4/%Y/%m/%d/')),
                ('belge_5', models.ImageField(blank=True, null=True, upload_to='belge_5/%Y/%m/%d/')),
                ('belge_6', models.ImageField(blank=True, null=True, upload_to='belge_6/%Y/%m/%d/')),
                ('belge_7', models.ImageField(blank=True, null=True, upload_to='belge_7/%Y/%m/%d/')),
                ('belge_8', models.ImageField(blank=True, null=True, upload_to='belge_8/%Y/%m/%d/')),
                ('anafirma', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='kurye.AnaFirma')),
            ],
        ),
        migrations.CreateModel(
            name='WSClient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('channel_name', models.CharField(default='', max_length=200)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='wsclient', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Teslimat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('onay', models.BooleanField(default=False)),
                ('adet', models.PositiveIntegerField(default=0)),
                ('gecerli_adet', models.PositiveIntegerField(default=0)),
                ('sos', models.BooleanField(default=False)),
                ('sos_sebep', models.CharField(default='0', max_length=2)),
                ('sos_sonuc', models.CharField(default='0', max_length=2)),
                ('zaman', models.DateTimeField(auto_now=True)),
                ('kurye', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teslimat', to=settings.AUTH_USER_MODEL)),
                ('firma', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teslimat_firma', to='kurye.Firma')),
            ],
        ),
        migrations.CreateModel(
            name='Mahalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mahalle', models.CharField(default='Fenerbahçe', max_length=80)),
                ('ilce', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='mahalle_ilce', to='kurye.Ilce')),
            ],
        ),
        migrations.CreateModel(
            name='IslemTeslimat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('islem_tipi', models.CharField(default='0', max_length=2)),
                ('tam_isim', models.CharField(default='', max_length=60)),
                ('tel_no', models.CharField(default='', max_length=10)),
                ('address', models.CharField(max_length=200)),
                ('enlem', models.DecimalField(decimal_places=12, default='0.0', max_digits=16)),
                ('boylam', models.DecimalField(decimal_places=12, default='0.0', max_digits=16)),
                ('teslim_edilmedi_sebep', models.CharField(default='0', max_length=2)),
                ('odeme_alinmadi_sebep', models.CharField(default='0', max_length=2)),
                ('sos_sebep', models.CharField(default='0', max_length=2)),
                ('sos_sonuc', models.CharField(default='0', max_length=2)),
                ('zaman', models.DateTimeField(auto_now=True)),
                ('teslimat', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='teslimat', to='kurye.Teslimat')),
            ],
        ),
        migrations.CreateModel(
            name='FaturaToplam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yil', models.PositiveIntegerField(default=0)),
                ('ay', models.PositiveIntegerField(default=0)),
                ('odendi', models.BooleanField(blank=True)),
                ('tutar', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='faturatoplam', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FaturaDetay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('yil', models.PositiveIntegerField(default=0)),
                ('ay', models.PositiveIntegerField(default=0)),
                ('max_motorcu', models.PositiveIntegerField(default=0)),
                ('standart_ek', models.BooleanField(blank=True)),
                ('ek_kisi', models.PositiveIntegerField(default=0)),
                ('ek_toplam', models.PositiveIntegerField(default=0)),
                ('standart_tutar', models.PositiveIntegerField(default=0)),
                ('ek_tutar', models.PositiveIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='faturadetay', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='EkFiyat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ek_motorcu', models.PositiveIntegerField(default=0)),
                ('fiyat', models.PositiveIntegerField(default=0)),
                ('max_motorcu', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ek_fiyat', to='kurye.Fiyat')),
            ],
        ),
        migrations.CreateModel(
            name='Bildirim',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipi', models.CharField(default='0', max_length=2)),
                ('message', models.TextField(blank=True, null=True)),
                ('viewed', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('receiver', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='receiver', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bahsis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zaman', models.DateTimeField(auto_now=True)),
                ('miktar', models.DecimalField(decimal_places=2, max_digits=6)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bahsis', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ArtiMotorcu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_motorcu', models.PositiveIntegerField(default=0)),
                ('gecen_motorcu_adedi', models.PositiveIntegerField(default=0)),
                ('zaman', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='artimotorcu', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
