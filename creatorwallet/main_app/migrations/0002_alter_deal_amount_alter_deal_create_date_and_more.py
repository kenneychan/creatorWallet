# Generated by Django 4.2.3 on 2023-08-02 15:45

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='deal',
            name='amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='deal',
            name='create_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='deal',
            name='details',
            field=models.TextField(blank=True, default='', max_length=500),
        ),
        migrations.AlterField(
            model_name='deal',
            name='done',
            field=models.BooleanField(blank=True, default=False),
        ),
        migrations.AlterField(
            model_name='deal',
            name='due_date',
            field=models.DateField(blank=True, default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='deal',
            name='promo_code',
            field=models.CharField(blank=True, default='', max_length=100),
        ),
        migrations.AlterField(
            model_name='deal',
            name='url',
            field=models.URLField(blank=True, default='', max_length=100),
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
    ]
