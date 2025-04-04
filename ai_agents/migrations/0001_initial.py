# Generated by Django 5.1.4 on 2025-01-14 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, help_text='You agree or make a statement on the post')),
                ('is_active', models.BooleanField(default=True, help_text='Whether the bot is currently active.')),
                ('personality', models.TextField(blank=True, help_text='None')),
            ],
        ),
    ]
