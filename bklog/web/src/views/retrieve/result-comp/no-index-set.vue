<!--
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
-->

<template>
  <div class="no-index-set-container">
    <span class="icon bklog-icon bklog-index-set"></span>
    <h2 class="main-tip">{{ $t('当前业务无数据可检索') }}</h2>
    <!-- 要使用检索功能，请先创建索引集 -->
    <div
      v-if="space.project_manage"
      class="index-manage-container"
    >
      <!-- 日志数据已进入数据平台或ES 关联已入库的数据 -->
      <div class="index-manage">
        <div class="index-manage-tips">
          <p>{{ $t('日志数据已进入数据平台或ES') }}</p>
          <p>{{ $t('关联已入库的数据') }}</p>
        </div>
        <bk-button
          class="king-button"
          :outline="true"
          theme="primary"
          @click="goToCreateIndex"
        >
          {{ $t('新建索引集') }}
        </bk-button>
      </div>
      <!-- 日志数据还在服务器上 需要采集日志，请先创建采集任务 -->
      <div class="index-manage">
        <div class="index-manage-tips">
          <p>{{ $t('日志数据还在服务器上') }}</p>
          <p>{{ $t('需要采集日志，请先创建采集任务') }}</p>
        </div>
        <bk-button
          class="king-button"
          :outline="true"
          theme="primary"
          @click="goToCreateCollection"
        >
          {{ $t('新建采集接入') }}
        </bk-button>
      </div>
    </div>
    <!-- 请联系业务运维配索引集 -->
    <p
      v-else
      class="side-tip"
    >
      {{ $t('请联系业务运维配索引集') }}
    </p>
  </div>
</template>

<script>
  import { mapGetters } from 'vuex';

  export default {
    computed: {
      ...mapGetters({
        space: 'space',
      }),
    },
    methods: {
      goToCreateIndex() {
        this.$router.push({
          path: '/manage/log-collection/log-index-set',
          query: {
            spaceUid: this.$store.state.spaceUid,
          },
        });
      },
      goToCreateCollection() {
        if (window.FEATURE_TOGGLE.scenario_log === 'on') {
          this.$router.push({
            path: '/manage/log-collection',
            query: {
              spaceUid: this.$store.state.spaceUid,
            },
          });
        } else {
          window.open(window.BKDATA_URL);
        }
      },
    },
  };
</script>

<style scoped lang="scss">
  .no-index-set-container {
    height: calc(100% - 142px);
    margin-top: 142px;
    text-align: center;

    .icon-index-set {
      margin-bottom: 25px;
      font-size: 52px;
      color: #d4d6dd;
    }

    .main-tip {
      margin-bottom: 30px;
      font-size: 18px;
      color: #313238;
    }

    .index-manage-container {
      display: flex;
      align-items: center;
      justify-content: space-between;
      width: 732px;
      margin: 80px auto 0;

      .index-manage {
        display: flex;
        flex-flow: column;
        align-items: center;
        width: 346px;
        height: 200px;
        background: #fff;
        border-radius: 2px;

        .index-manage-tips {
          height: 88px;
          margin: 40px 0 0;
          font-size: 14px;
          font-weight: 600;
          line-height: 24px;
          color: #63656e;

          p:last-child {
            font-weight: normal;
            color: #979ba5;
          }
        }

        .king-button {
          border-radius: 16px;
        }
      }
    }

    .side-tip {
      margin-bottom: 30px;
      font-size: 14px;
      color: #979ba5;
    }
  }
</style>
