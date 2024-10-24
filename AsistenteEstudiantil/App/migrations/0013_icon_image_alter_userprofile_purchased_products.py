# Generated by Django 4.2.7 on 2024-01-04 02:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0012_userprofile_purchased_products'),
    ]

    operations = [
        migrations.AddField(
            model_name='icon',
            name='image',
            field=models.ImageField(default='path/to/default/image.jpg', upload_to='icon_images/'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='purchased_products',
            field=models.ManyToManyField(related_name='purchased_by', to='App.product'),
        ),
    ]
