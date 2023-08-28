# Generated by Django 4.2.4 on 2023-08-28 06:14

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import zelthy.apps.dynamic_models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('dynamic_models', '0006_supplychainnodes_benefitssupplychainnodes'),
    ]

    operations = [
        migrations.CreateModel(
            name='DispensingOptionsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, verbose_name='Label')),
                ('dose', models.IntegerField(blank=True, null=True, verbose_name='Dose')),
                ('min_dose', models.IntegerField(blank=True, null=True, verbose_name='Min Dose')),
                ('max_dose', models.IntegerField(blank=True, null=True, verbose_name='Max Dose')),
                ('min_income', models.BigIntegerField(blank=True, null=True, verbose_name='Minimum Salary')),
                ('max_income', models.BigIntegerField(blank=True, null=True, verbose_name='Maximum Salary')),
                ('order_number', models.CharField(blank=True, max_length=255, verbose_name='Order Number')),
                ('days_since_approval', models.IntegerField(blank=True, null=True, verbose_name='Days since approval')),
                ('days_of_supply', models.IntegerField(blank=True, null=True, verbose_name='Days of supply')),
                ('credit_required', models.FloatField(blank=True, null=True, verbose_name='Credit required')),
                ('credit_deducted', models.FloatField(blank=True, null=True, verbose_name='Credit deducted')),
                ('mrp', models.FloatField(blank=True, null=True, verbose_name='MRP')),
                ('jsonfield_extra1', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SkuModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, verbose_name='SKU Label')),
                ('brand_name', models.CharField(blank=True, max_length=255, verbose_name='Brand Name')),
                ('pack_size', models.CharField(blank=True, max_length=255, verbose_name='Pack Size')),
                ('mrp', models.FloatField(blank=True, null=True, verbose_name='MRP including Taxes')),
                ('molecule', models.CharField(blank=True, max_length=255, verbose_name='Molecule')),
                ('manufacturer', models.CharField(blank=True, max_length=255, verbose_name='Manufacturer')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('is_free', models.BooleanField(default=False, verbose_name='Is Free')),
                ('extrafield1_char', models.CharField(blank=True, max_length=255, verbose_name='Extra Field1 Char')),
                ('extrafield2_char', models.CharField(blank=True, max_length=255, verbose_name='Extra Field2 Char')),
                ('extrafield3_char', models.CharField(blank=True, max_length=255, verbose_name='Extra Field3 Char')),
                ('jsonfield_extra1', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SkuTypes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, unique=True, verbose_name='SKU Types (e.g. Paid, Frre, 75% discount)')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrderItemsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=255, verbose_name='Item Label')),
                ('quantity', models.IntegerField(default=0, verbose_name='Quantity')),
                ('discount', models.FloatField(default=0, verbose_name='Discount')),
                ('is_active', models.BooleanField(default=True, verbose_name='Is active')),
                ('item_type', zelthy.apps.dynamic_models.fields.ZForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dynamic_models.skutypes')),
                ('sku', zelthy.apps.dynamic_models.fields.ZForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynamic_models.skumodel')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DispensingOptionsOrderItemsModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dispensingoption', zelthy.apps.dynamic_models.fields.ZForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynamic_models.dispensingoptionsmodel')),
                ('items', zelthy.apps.dynamic_models.fields.ZForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dynamic_models.orderitemsmodel')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
