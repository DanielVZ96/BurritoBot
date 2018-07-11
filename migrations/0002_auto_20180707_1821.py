# Generated by Django 2.0.7 on 2018-07-07 18:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('burritobot', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TwitchUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('twitch_id', models.IntegerField()),
                ('twitch_name', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('access_token', models.CharField(max_length=200)),
                ('refresh_token', models.CharField(max_length=200)),
                ('expiration_date', models.DateField()),
                ('scope', models.CharField(max_length=500)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='AuthInfo',
        ),
        migrations.AddField(
            model_name='command',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
