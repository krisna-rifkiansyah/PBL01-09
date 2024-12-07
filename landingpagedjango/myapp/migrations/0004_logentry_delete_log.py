# Generated by Django 5.1.1 on 2024-12-05 07:30

import django.utils.timezone
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_alter_post_image_log'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('key', models.CharField(max_length=50)),
                ('txt', models.CharField(max_length=255)),
                ('session', models.CharField(max_length=50)),
                ('ipaddr', models.GenericIPAddressField()),
                ('app', models.CharField(default='PBL01LOGS', max_length=50)),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.DeleteModel(
            name='Log',
        ),
    ]
