# Generated by Django 4.2.6 on 2023-10-24 23:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='nonce',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
