# Generated by Django 2.0.6 on 2018-06-13 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('IndrasNet', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='modelparam',
            name='default_val',
            field=models.CharField(max_length=16, null=True),
        ),
    ]
