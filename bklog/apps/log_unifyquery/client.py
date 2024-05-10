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
from typing import Any, Dict
from apps.api import UnifyQueryApi


class UnifyQuery(object):
    def __init__(self, search_dict):
        self.search_dict: Dict[str, Any] = search_dict
        self.include_nested_fields: bool = search_dict.get("include_nested_fields", True)

    def query_ts(self):
        return UnifyQueryApi.unify_query.query_ts(self.search_dict)

    def query_fields(self):
        pass
