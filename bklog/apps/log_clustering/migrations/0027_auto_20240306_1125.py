# Generated by Django 3.2.23 on 2024-03-06 03:25

import hashlib
import json

from django.db import migrations, models
from django.db.models import Q


def insert_data_to_clusteringremark(apps, schema_editor):
    signature_and_pattern = apps.get_model('log_clustering', 'AiopsSignatureAndPattern')
    clustering_remark = apps.get_model('log_clustering', 'ClusteringRemark')
    clustering_config = apps.get_model('log_clustering', 'ClusteringConfig')

    # 所有的signature_and_pattern都需要插入到clustering_remark中
    for s in signature_and_pattern.objects.all():
        bk_biz_id = (
            clustering_config.objects.filter(Q(model_id=s.model_id) | Q(model_output_rt=s.model_id)).first().bk_biz_id
        )
        clustering_remark.objects.create(
            bk_biz_id=bk_biz_id,
            signature=s.signature,
            origin_pattern=s.origin_pattern,
            groups={},
            group_hash=hashlib.md5(json.dumps({}).encode()).hexdigest(),
            label=s.label,
            remark=s.remark,
            owners=s.owners,
        )
    # 创建的所有clustering_remark中signature或者origin_pattern相同的数据，需要把remark合并到一起
    for s in clustering_remark.objects.all():
        same_data = clustering_remark.objects.filter(
            (Q(signature=s.signature) | Q(origin_pattern=s.origin_pattern)) & ~Q(id=s.id)
        )
        print(same_data)
        for data in same_data:
            s.remark += data.remark
        s.save()


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
                ('label', models.TextField(default='', verbose_name='标签')),
                ('remark', models.JSONField(blank=True, default=[], null=True, verbose_name='备注信息')),
                ('owners', models.JSONField(blank=True, default=[], null=True, verbose_name='负责人')),
            ],
            options={
                'index_together': {('signature',)},
            },
        ),
        migrations.RunPython(insert_data_to_clusteringremark),
    ]
