# Generated by Django 5.0.6 on 2024-07-08 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('crece', '0003_post_comment'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='modified',
            new_name='updated_at',
        ),
    ]
