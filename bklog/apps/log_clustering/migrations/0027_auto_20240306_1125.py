# Generated by Django 3.2.23 on 2024-03-06 03:25

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('log_clustering', '0026_auto_20231108_1624'),
    ]

    operations = [
        migrations.AddField(
            model_name='aiopssignatureandpattern',
            name='origin_pattern',
            field=models.TextField(default='', verbose_name='原始pattern'),
        ),
        migrations.AddField(
            model_name='clusteringconfig',
            name='group_fields',
            field=models.JSONField(blank=True, null=True, default=dict, verbose_name='分组字段 kv格式'),
        ),
        migrations.CreateModel(
            name='ClusteringRemark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='创建时间')),
                ('created_by', models.CharField(default='', max_length=32, verbose_name='创建者')),
                ('updated_at', models.DateTimeField(auto_now=True, db_index=True, null=True, verbose_name='更新时间')),
                ('updated_by', models.CharField(blank=True, default='', max_length=32, verbose_name='修改者')),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
                ('deleted_at', models.DateTimeField(blank=True, null=True, verbose_name='删除时间')),
                ('deleted_by', models.CharField(blank=True, max_length=32, null=True, verbose_name='删除者')),
                ('bk_biz_id', models.IntegerField(verbose_name='业务id')),
                ('signature', models.CharField(max_length=256, verbose_name='数据指纹')),
                ('origin_pattern', models.TextField(default='', verbose_name='原始pattern')),
                ('groups', models.JSONField(blank=True, default=dict, null=True, verbose_name='分组信息 kv格式')),
                ('group_hash', models.CharField(max_length=256, verbose_name='分组hash')),
                ('remark', models.JSONField(blank=True, default=[], null=True, verbose_name='备注信息')),
                ('owners', models.JSONField(blank=True, default=[], null=True, verbose_name='负责人')),
            ],
            options={
                'index_together': {('signature', 'group_hash')},
            },
        ),
    ]