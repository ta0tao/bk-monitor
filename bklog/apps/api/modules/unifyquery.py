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

"""
UNIFYQUERY 模块，调用接口汇总
"""
from django.utils.translation import ugettext_lazy as _  # noqa

from apps.api.base import DataAPI  # noqa
from apps.api.modules.utils import add_esb_info_before_request  # noqa
from config.domains import UNIFYQUERY_APIGATEWAY_ROOT  # noqa


class _UnifyQueryApi(object):
    MODULE = _("UNIFYQUERY模块")

    def __init__(self):
        self.query_ts = DataAPI(
            method="POST",
            url=UNIFYQUERY_APIGATEWAY_ROOT + "query/ts/",
            module=self.MODULE,
            description="时序型检索",
            default_return_value=None,
            before_request=add_esb_info_before_request,
        )
