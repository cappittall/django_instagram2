# Generated by Django 3.2 on 2023-02-11 12:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_alter_orderlist_service'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orderlist',
            options={'ordering': ('-id',), 'verbose_name_plural': 'order Listesi'},
        ),
    ]
