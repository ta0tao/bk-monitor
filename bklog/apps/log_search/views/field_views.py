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
from apps.log_search.exceptions import GetMultiResultFailException
from apps.log_search.handlers.search.mapping_handlers import MappingHandlers
from apps.log_search.models import LogIndexSet, LogIndexSetData
from apps.log_search.permission import Permission
from apps.log_search.serializers import (
    FetchStatisticsGraphSerializer,
    FetchStatisticsInfoSerializer,
    FetchTopkListSerializer, QueryFieldBaseSerializer,
)
from apps.log_unifyquery.constants import FIELD_TYPE_MAP
from apps.log_unifyquery.handler import UnifyQueryHandler
from apps.utils.drf import list_route
from apps.utils.thread import MultiExecuteFunc


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

    @list_route(methods=["POST"], url_path="fetch_distinct_count_list")
    def fetch_distinct_count_list(self, request, *args, **kwargs):
        """
        @api {get} /field/index_set/fetch_distinct_count_list/ 获取字段去重计数列表
        @apiName fetch_topk_list
        """
        count_list = []
        params = self.params_valid(QueryFieldBaseSerializer)
        index_set_id = params["index_set_ids"][0]
        index_set_obj: LogIndexSet = LogIndexSet.objects.filter(index_set_id=index_set_id).first()
        index_set_data_obj: LogIndexSetData = LogIndexSetData.objects.filter(index_set_id=index_set_id).first()

        mapping_handlers = MappingHandlers(
            index_set_data_obj.result_table_id,
            index_set_obj.index_set_id,
            index_set_obj.scenario_id,
            index_set_obj.storage_cluster_id,
            "dtEventTimeStamp",
            start_time=params["start_time"],
            end_time=params["end_time"],
        )
        mapping_list = mapping_handlers._get_mapping()
        property_dict: dict = mapping_handlers.find_merged_property(mapping_list)
        fields_result: list = MappingHandlers.get_all_index_fields_by_mapping(property_dict)
        fields_set = set([field["name"] for field in fields_result])
        multi_execute_func = MultiExecuteFunc()

        for field_name in fields_set:
            query_handler = UnifyQueryHandler({"agg_field": field_name, **params})
            multi_execute_func.append(field_name, query_handler.get_distinct_count)

        multi_result = multi_execute_func.run()

        if not multi_result:
            raise GetMultiResultFailException(
                GetMultiResultFailException.MESSAGE.format(func_name="fetch_distinct_count_list")
            )
        for field_name, distinct_count in multi_result.items():
            count_list.append({
                "field_name": field_name,
                "distinct_count": distinct_count
            })
        return Response(count_list)

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
        if FIELD_TYPE_MAP.get(params["field_type"], "string") == "int":
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
        if FIELD_TYPE_MAP[params["field_type"]] == "int":
            if params["distinct_count"] < 10:
                return Response(query_handler.get_topk_list(10))
            else:
                return Response(query_handler.get_bucket_data(params["min"], params["max"]))
        else:
            return Response(query_handler.get_topk_ts_data(5))
