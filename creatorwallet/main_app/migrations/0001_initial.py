# Generated by Django 4.2.3 on 2023-08-03 22:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PlatformContent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('url', models.URLField(max_length=100)),
                ('platform_username', models.CharField(blank=True, default='', max_length=50)),
                ('platform_type', models.CharField(blank=True, default='', max_length=1)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Deal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10)),
                ('details', models.TextField(blank=True, default='', max_length=500)),
                ('due_date', models.DateField(blank=True)),
                ('url', models.URLField(blank=True, default='', max_length=100)),
                ('promo_code', models.CharField(blank=True, default='', max_length=100)),
                ('done', models.BooleanField(blank=True, default=False)),
                ('created_date', models.DateField(default=datetime.date.today)),
                ('platformscontent', models.ManyToManyField(to='main_app.platformcontent')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Attachment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('filename', models.CharField(max_length=200)),
                ('url', models.CharField(max_length=200)),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.deal')),
            ],
        ),
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('notes', models.CharField(max_length=200)),
                ('activity', models.CharField(max_length=200)),
                ('deal', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.deal')),
            ],
            options={
                'ordering': ['-date'],
            },
        ),
    ]
