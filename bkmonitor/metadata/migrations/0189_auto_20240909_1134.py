# Generated by Django 3.2.15 on 2024-09-09 03:34

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('metadata', '0188_esstorage_need_create_index'),
    ]

    operations = [
        migrations.RenameField(
            model_name='bcsfederalclusterinfo',
            old_name='fed_buildin_event_table_id',
            new_name='fed_builtin_metric_table_id',
        ),
        migrations.RemoveField(
            model_name='bcsfederalclusterinfo',
            name='fed_buildin_metric_table_id',
        ),
        migrations.AddField(
            model_name='bcsfederalclusterinfo',
            name='fed_builtin_event_table_id',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='内置事件结果表'),
        ),
    ]
