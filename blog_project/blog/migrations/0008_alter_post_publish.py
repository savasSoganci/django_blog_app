# Generated by Django 4.0.2 on 2022-02-22 11:48

import blog.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_alter_post_publish'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='publish',
            field=models.DateTimeField(validators=[blog.models.publish_validate]),
        ),
    ]
