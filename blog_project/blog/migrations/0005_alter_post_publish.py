# Generated by Django 4.0.2 on 2022-02-21 07:43

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0004_alter_post_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(validators=[blog.models.publish_validate]),
        ),
    ]
