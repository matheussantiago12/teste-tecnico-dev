# Generated by Django 5.0.2 on 2024-02-28 17:51

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_alter_parkmovement_vehicle'),
    ]

    operations = [
        migrations.AddField(
            model_name='parkmovement',
            name='customer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='base.customer'),
            preserve_default=False,
        ),
    ]