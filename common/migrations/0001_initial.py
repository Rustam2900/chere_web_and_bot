# Generated by Django 5.1 on 2024-10-04 13:48

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='all_media_files/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'mp4', 'mp3', 'wav', 'ogg', 'pdf', 'txt', 'zip'])], verbose_name='file')),
                ('type', models.CharField(choices=[('image', 'Image'), ('video', 'Video'), ('audio', 'Audio'), ('other', 'Other')], default='image', max_length=20, verbose_name='type')),
            ],
            options={
                'verbose_name': 'Media',
                'verbose_name_plural': 'Medias',
            },
        ),
    ]
