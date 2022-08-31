# Generated by Django 3.2.15 on 2022-08-31 06:14

from django.conf import settings
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('ratings', models.ManyToManyField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
