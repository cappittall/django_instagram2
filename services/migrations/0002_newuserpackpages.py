# Generated by Django 3.2 on 2023-03-06 18:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewUserPackpages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, verbose_name='Paket Adı')),
                ('country_code', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.countrycodes', verbose_name='Ülke Kodu')),
                ('gender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='services.genders', verbose_name='Cinsiyet')),
            ],
            options={
                'verbose_name_plural': 'Kullanıcı Paketleri',
                'ordering': ['-id'],
            },
        ),
    ]
