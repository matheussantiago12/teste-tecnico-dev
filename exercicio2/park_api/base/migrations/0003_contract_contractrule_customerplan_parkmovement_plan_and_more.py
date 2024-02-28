# Generated by Django 5.0.2 on 2024-02-27 22:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_vehicle'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('max_value', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ContractRule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('until', models.IntegerField()),
                ('value', models.FloatField()),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.contract')),
            ],
        ),
        migrations.CreateModel(
            name='CustomerPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('due_date', models.DateTimeField()),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.customer')),
            ],
        ),
        migrations.CreateModel(
            name='ParkMovement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry_date', models.DateTimeField()),
                ('exit_date', models.DateTimeField(null=True)),
                ('value', models.FloatField(null=True)),
                ('vehicle', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='base.vehicle')),
            ],
        ),
        migrations.CreateModel(
            name='Plan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=50)),
                ('value', models.FloatField()),
                ('customers', models.ManyToManyField(through='base.CustomerPlan', to='base.customer')),
            ],
        ),
        migrations.AddField(
            model_name='customerplan',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.plan'),
        ),
    ]