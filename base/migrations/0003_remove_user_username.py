# Generated by Django 4.2.3 on 2023-07-23 15:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_user_profile_picture_alter_user_email_mp3file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='username',
        ),
    ]
