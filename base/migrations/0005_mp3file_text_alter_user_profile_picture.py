# Generated by Django 4.2.3 on 2023-08-05 14:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_alter_user_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='mp3file',
            name='text',
            field=models.CharField(default='', max_length=4096),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.CharField(default='defaut.jpg', max_length=64),
        ),
    ]