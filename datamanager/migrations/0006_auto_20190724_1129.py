# Generated by Django 2.2.3 on 2019-07-24 16:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('datamanager', '0005_comment'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommentDB',
            fields=[
                ('id', models.UUIDField(db_column='id', default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('rate', models.IntegerField(db_column='Rate')),
                ('comment', models.CharField(db_column='Comment', max_length=200)),
            ],
            options={
                'db_table': 'CommentDB',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='Comment',
        ),
    ]
