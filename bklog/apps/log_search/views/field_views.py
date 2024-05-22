# -*- coding: utf-8 -*-
"""
Tencent is pleased to support the open source community by making 蓝鲸智云 - 监控平台 (BlueKing - Monitor) available.
Copyright (C) 2017-2021 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except in compliance with the License.
You may obtain a copy of the License at http://opensource.org/licenses/MIT
Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on
an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.
"""
from django.conf import settings
from rest_framework import serializers
from rest_framework.response import Response

from apps.generic import APIViewSet
from apps.iam.handlers.drf import ViewBusinessPermission
from apps.log_search.constants import FieldTypeMap
from apps.log_search.permission import Permission
from apps.log_search.serializers import (
    FetchStatisticsGraphSerializer,
    FetchStatisticsInfoSerializer,
    FetchTopkListSerializer,
)
from apps.log_unifyquery.handler import UnifyQueryHandler
from apps.utils.drf import list_route


class FieldViewSet(APIViewSet):
    """
    字段统计&分析
    """

    serializer_class = serializers.Serializer

    def get_permissions(self):
        if settings.BKAPP_IS_BKLOG_API:
            # 只在后台部署时做白名单校验
            auth_info = Permission.get_auth_info(self.request, raise_exception=False)
            # ESQUERY白名单不需要鉴权
            if auth_info and auth_info["bk_app_code"] in settings.ESQUERY_WHITE_LIST:
                return []

        return [ViewBusinessPermission()]

    @list_route(methods=["POST"], url_path="fetch_topk_list")
    def fetch_topk_list(self, request, *args, **kwargs):
        """
        @api {get} /field/index_set/fetch_topk_list/ 获取字段topk计数列表
        @apiName fetch_topk_list
        """
        params = self.params_valid(FetchTopkListSerializer)
        query_handler = UnifyQueryHandler(params)
        total_count = query_handler.get_total_count()
        field_count = query_handler.get_field_count()
        distinct_count = query_handler.get_distinct_count()
        topk_list = query_handler.get_topk_list(params["limit"])
        return Response(
            {
                "name": params["agg_field"],
                "columns": ["_value", "_count"],
                "types": ["float", "float"],
                "limit": params["limit"],
                "total_count": total_count,
                "field_count": field_count,
                "distinct_count": distinct_count,
                "values": topk_list,
            }
        )

    @list_route(methods=["POST"], url_path="statistics/info")
    def fetch_statistics_info(self, request, *args, **kwargs):
        """
        @api {get} /field/index_set/statistics/info/ 获取字段统计信息
        @apiName fetch_statistics_info
        """
        params = self.params_valid(FetchStatisticsInfoSerializer)
        query_handler = UnifyQueryHandler(params)

        total_count = query_handler.get_total_count()
        field_count = query_handler.get_field_count()
        distinct_count = query_handler.get_distinct_count()
        if total_count and field_count:
            field_percent = round(field_count / total_count, 2)
        else:
            field_percent = 0

        data = {
            "total_count": total_count,
            "field_count": field_count,
            "distinct_count": distinct_count,
            "field_percent": field_percent,
        }
        if FieldTypeMap[params["field_type"]] == "int":
            max_value = query_handler.get_agg_value("max")
            min_value = query_handler.get_agg_value("min")
            avg_value = query_handler.get_agg_value("avg")
            median_value = query_handler.get_agg_value("median")
            data["value_analysis"] = {"max": max_value, "min": min_value, "avg": avg_value, "median": median_value}

        return Response(data)

    @list_route(methods=["POST"], url_path="statistics/graph")
    def fetch_statistics_graph(self, request, *args, **kwargs):
        """constants.py:1515
        @api {get} /field/index_set/statistics/graph/ 获取字段统计图表
        @apiName fetch_statistics_graph
        """
        params = self.params_valid(FetchStatisticsGraphSerializer)
        query_handler = UnifyQueryHandler(params)
        if FieldTypeMap[params["field_type"]] == "int":
            if params["distinct_count"] < 10:
                return Response(query_handler.get_topk_list(10))
            else:
                return Response(query_handler.get_bucket_data())
        else:
            return Response(query_handler.get_topk_ts_data(5))
