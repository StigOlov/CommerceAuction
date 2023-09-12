# Generated by Django 4.2.2 on 2023-09-08 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bid',
            name='status',
            field=models.CharField(choices=[('Won', 'Won'), ('Lost', 'Lost'), ('Winning', 'Winning'), ('Losing', 'Losing')], max_length=10),
        ),
    ]
