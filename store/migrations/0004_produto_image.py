# Generated by Django 3.0.7 on 2020-08-23 12:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_remove_produto_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
