# Generated by Django 4.2.7 on 2024-03-07 14:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0015_remove_product_image_product_gif'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avatar',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('slug', models.SlugField(blank=True, unique=True)),
                ('background_image', models.ImageField(default='path/to/default/background.jpg', upload_to='avatar_images/backgrounds/')),
                ('head_image', models.ImageField(default='path/to/default/head.jpg', upload_to='avatar_images/heads/')),
                ('torso_image', models.ImageField(default='path/to/default/torso.jpg', upload_to='avatar_images/torsos/')),
                ('legs_image', models.ImageField(default='path/to/default/legs.jpg', upload_to='avatar_images/legs/')),
                ('feet_image', models.ImageField(default='path/to/default/feet.jpg', upload_to='avatar_images/feet/')),
            ],
        ),
        migrations.AddField(
            model_name='userprofile',
            name='selected_background',
            field=models.ImageField(blank=True, null=True, upload_to='user_selected_images/backgrounds/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='selected_feet',
            field=models.ImageField(blank=True, null=True, upload_to='user_selected_images/feet/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='selected_head',
            field=models.ImageField(blank=True, null=True, upload_to='user_selected_images/heads/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='selected_legs',
            field=models.ImageField(blank=True, null=True, upload_to='user_selected_images/legs/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='selected_torso',
            field=models.ImageField(blank=True, null=True, upload_to='user_selected_images/torsos/'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='avatar',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.avatar'),
        ),
    ]
