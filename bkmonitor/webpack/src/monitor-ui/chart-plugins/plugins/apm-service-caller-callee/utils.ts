/*
/*
 * Tencent is pleased to support the open source community by making
 * 蓝鲸智云PaaS平台 (BlueKing PaaS) available.
 *
 * Copyright (C) 2021 THL A29 Limited, a Tencent company.  All rights reserved.
 *
 * 蓝鲸智云PaaS平台 (BlueKing PaaS) is licensed under the MIT License.
 *
 * License for 蓝鲸智云PaaS平台 (BlueKing PaaS):
 *
 * ---------------------------------------------------
 * Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
 * documentation files (the "Software"), to deal in the Software without restriction, including without limitation
 * the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and
 * to permit persons to whom the Software is furnished to do so, subject to the following conditions:
 *
 * The above copyright notice and this permission notice shall be included in all copies or substantial portions of
 * the Software.
 *
 * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
 * THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
 * CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
 * IN THE SOFTWARE.
 */

import { EKind, type ITabItem } from './type';

export const CALLER_CALLEE_TYPE: ITabItem[] = [
  {
    label: '主调',
    id: EKind.caller,
  },
  {
    label: '被调',
    id: EKind.callee,
  },
];
export type CallerCalleeType = (typeof CALLER_CALLEE_TYPE)[number]['id'];
export const PERSPECTIVE_TYPE = [
  {
    label: '单视角',
    id: 'single',
  },
  {
    label: '多视角',
    id: 'multiple',
  },
];

export const CHART_TYPE = [
  {
    label: '饼图',
    id: 'caller-pie-chart',
  },
  {
    label: '柱状图',
    id: 'caller-bar-chart',
  },
];

export const TAB_TABLE_REQUEST_COLUMN = [
  {
    label: '数值',
    prop: 'request_total_0s',
  },
  {
    label: '占比',
    prop: 'proportions_request_total_0s',
  },
];

export const TAB_TABLE_TYPE = [
  {
    label: '请求量',
    id: 'request',
    columns: TAB_TABLE_REQUEST_COLUMN,
  },
  {
    label: '成功/异常/超时率',
    id: 'timeout',
    columns: [],
  },
  {
    label: '耗时（ms）',
    id: 'consuming',
    columns: [],
  },
];

export const SYMBOL_LIST = [
  {
    value: 'eq',
    label: '等于',
  },
  {
    value: 'neq',
    label: '不等于',
  },
  {
    value: 'before_req',
    label: '前匹配',
  },
  {
    value: 'after_req',
    label: '后匹配',
  },
  {
    value: 'include',
    label: '包含',
  },
  {
    value: 'exclude',
    label: '不包含',
  },
  {
    value: 'reg',
    label: '正则',
  },
];
const CALL_INTERVAL_LIST = [1, 2, 3, 4, 5, 6, 10, 12, 15, 20, 30, 60, 120, 180, 240, 300, 600];
/**
 *
 * @param rawInterval 原始周期
 * @description 修正周期 (只能从上面的周期列表中向上取值) api仅支持 单位 m
 */
export const intervalLowBound = (rawInterval: number) => {
  const list = CALL_INTERVAL_LIST.map(v => v - rawInterval);
  const index = list.findIndex(v => v > 0);
  return CALL_INTERVAL_LIST.at(index) || CALL_INTERVAL_LIST.at(-1);
};

const recordCallOptionKindKey = '____apm-service-caller-callee-kind____';
/**
 * @description 记录调用者调用被调用者的图表类型
 * @param keyObject
 * @param kind
 * @returns
 */
export function setRecordCallOptionKind(keyObject, kind: EKind) {
  if (!(keyObject?.app_name && keyObject?.service_name)) {
    return;
  }
  try {
    const listStr = localStorage.getItem(recordCallOptionKindKey);
    const obj = {
      key: `__${keyObject.app_name}__${keyObject.service_name}__`,
      value: kind,
    };
    if (listStr) {
      const list = JSON.parse(listStr);
      const resultList = [];
      if (list.length > 50) {
        list.splice(list.length - 1, list.length - 50);
      }
      for (const item of list) {
        if (item.key !== obj.key) {
          resultList.push(item);
        }
      }
      resultList.unshift(obj);
      localStorage.setItem(recordCallOptionKindKey, JSON.stringify(resultList));
    } else {
      localStorage.setItem(recordCallOptionKindKey, JSON.stringify([obj]));
    }
  } catch (err) {
    console.log(err);
  }
}
/**
 * @description 获取调用者调用被调用者的图表类型
 * @param keyObject
 * @returns
 */
export function getRecordCallOptionKind(keyObject) {
  console.log(keyObject);
  if (!(keyObject?.app_name && keyObject?.service_name)) {
    return EKind.callee;
  }
  try {
    let kind = EKind.callee;
    const key = `__${keyObject.app_name}__${keyObject.service_name}__`;
    const listStr = localStorage.getItem(recordCallOptionKindKey);
    if (listStr) {
      const list = JSON.parse(listStr) as any[];
      for (const item of list) {
        if (item.key === key) {
          kind = item.value || EKind.callee;
          break;
        }
      }
    }
    return kind;
  } catch (err) {
    console.log(err);
    return EKind.callee;
  }
}
