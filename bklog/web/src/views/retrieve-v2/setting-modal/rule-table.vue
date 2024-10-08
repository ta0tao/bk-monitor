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
  <div class="cluster-table">
    <!-- 聚类规则 -->
    <div class="container-item table-container">
      <p style="height: 32px">{{ $t('聚类规则') }}</p>
      <div class="table-operate">
        <bk-button
          class="add-box"
          :class="globalEditable ? 'btn-hover' : ''"
          :disabled="!globalEditable"
          size="small"
          @click="isShowAddRule = true"
        >
          <i class="bk-icon icon-plus push"></i>
          {{ $t('添加') }}
        </bk-button>
        <bk-button
          style="min-width: 48px"
          :class="globalEditable ? 'btn-hover' : ''"
          :disabled="!globalEditable"
          data-test-id="LogCluster_button_addNewRules"
          size="small"
          @click="handleFastAddRule"
        >
          {{ $t('导入') }}
        </bk-button>
        <bk-button
          style="min-width: 48px"
          :class="globalEditable ? 'btn-hover' : ''"
          :disabled="!globalEditable"
          size="small"
          @click="() => handleExportRule()"
        >
          {{ $t('导出') }}
        </bk-button>
        <bk-button
          style="min-width: 72px"
          :class="globalEditable ? 'btn-hover' : ''"
          :disabled="!globalEditable"
          data-test-id="LogCluster_button_reductionRules"
          size="small"
          @click="reductionRule"
        >
          {{ $t('恢复默认') }}
        </bk-button>
      </div>

      <div
        class="cluster-table"
        data-test-id="LogCluster_div_rulesTable"
      >
        <div class="table-row flbc">
          <div class="row-left">
            <div class="row-left-index">{{ $t('序号') }}</div>
            <div class="row-left-regular">{{ $t('正则表达式') }}</div>
          </div>
          <div class="row-right flbc">
            <div>{{ $t('占位符') }}</div>
            <div>{{ $t('操作') }}</div>
          </div>
        </div>

        <div
          v-if="rulesList.length > 0"
          v-bkloading="{ isLoading: tableLoading }"
        >
          <vue-draggable
            v-bind="dragOptions"
            v-model="rulesList"
          >
            <transition-group>
              <li
                v-for="(item, index) in rulesList"
                class="table-row table-row-li flbc"
                :key="item.__Index__"
              >
                <div class="row-left">
                  <div class="row-left-index">
                    <span class="icon bklog-icon bklog-drag-dots"></span><span>{{ index }}</span>
                  </div>
                  <div class="regular-container">
                    <register-column
                      :context="Object.values(item)[0]"
                      :root-margin="'-180px 0px 0px 0px'"
                    >
                      <cluster-event-popover
                        :is-cluster="false"
                        :placement="'top'"
                        @event-click="operation => handleMenuClick(operation, item)"
                      >
                        <span class="row-left-regular"> {{ Object.values(item)[0] }}</span>
                      </cluster-event-popover>
                    </register-column>
                  </div>
                </div>
                <div class="row-right flbc">
                  <div>
                    <span
                      class="row-right-item"
                      :ref="`placeholder-${index}`"
                      >{{ Object.keys(item)[0] }}</span
                    >
                  </div>
                  <div class="rule-btn">
                    <bk-button
                      style="margin-right: 10px"
                      :disabled="!globalEditable"
                      theme="primary"
                      text
                      @click="clusterEdit(index)"
                    >
                      {{ $t('编辑') }}
                    </bk-button>
                    <bk-button
                      :disabled="!globalEditable"
                      theme="primary"
                      text
                      @click="clusterRemove(index)"
                    >
                      {{ $t('删除') }}
                    </bk-button>
                  </div>
                </div>
              </li>
            </transition-group>
          </vue-draggable>
        </div>
        <div
          v-else
          class="no-cluster-rule"
        >
          <empty-status
            :show-text="false"
            empty-type="empty"
          >
            <div>{{ $t('暂无聚类规则') }}</div>
          </empty-status>
        </div>
      </div>
    </div>
    <!-- 原始日志 -->
    <div :class="{ 'debug-container': true, 'is-hidden': !isClickAlertIcon }">
      <div
        class="debug-tool"
        @click="handleClickDebugButton"
      >
        <i :class="{ 'bk-icon icon-play-shape': true, 'is-active': isClickAlertIcon }"></i>
        <span>{{ $t('调试工具') }}</span>
      </div>

      <div class="debug-input-box">
        <div class="fl-jfsb mt18">
          <p style="height: 32px">{{ $t('原始日志') }}</p>
          <bk-button
            style="min-width: 48px"
            :class="logOriginal !== '' && rulesList.length !== 0 ? 'btn-hover' : ''"
            :disabled="!globalEditable || logOriginal === '' || rulesList.length === 0"
            :loading="debugRequest"
            size="small"
            @click="debugging"
          >
            {{ $t('调试') }}
          </bk-button>
        </div>

        <div class="log-style">
          <bk-input
            :input-style="{
              'background-color': '#313238',
              height: '100px',
              'line-height': '24px',
              color: '#C4C6CC',
              borderRadius: '2px',
            }"
            v-model.trim="logOriginal"
            :disabled="!globalEditable || logOriginalRequest"
            :rows="3"
            :type="'textarea'"
            placeholder=" "
          >
          </bk-input>
        </div>
        <!-- 效果 -->
        <div class="mt18">
          <p style="height: 32px">{{ $t('效果预览') }}</p>
          <div
            class="effect-container"
            v-bkloading="{ isLoading: debugRequest, size: 'mini' }"
          >
            <text-highlight
              style="word-break: break-all;"
              class="monospace-text"
              :queries="getHeightLightList(effectOriginal)"
            >
              {{ effectOriginal }}
            </text-highlight>
          </div>
        </div>
      </div>
    </div>
    <!-- 添加规则dialog -->
    <bk-dialog
      width="640"
      ext-cls="add-rule"
      v-model="isShowAddRule"
      :mask-close="false"
      :title="isEditRules ? $t('编辑规则') : $t('添加规则')"
      header-position="left"
      @after-leave="cancelAddRuleContent"
    >
      <bk-form
        ref="addRulesRef"
        :label-width="200"
        :model="addRulesData"
        form-type="vertical"
      >
        <bk-form-item
          :label="$t('正则表达式')"
          :property="'regular'"
          :rules="rules.regular"
          required
        >
          <bk-input
            style="width: 560px"
            v-model="addRulesData.regular"
          ></bk-input>
          <p>{{ $t('样例') }}：\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}</p>
        </bk-form-item>
        <bk-form-item
          :label="$t('占位符')"
          :property="'placeholder'"
          :rules="rules.placeholder"
          required
        >
          <bk-input
            style="width: 560px"
            v-model="addRulesData.placeholder"
          ></bk-input>
          <p>{{ $t('样例') }}：IP</p>
        </bk-form-item>
      </bk-form>
      <template #footer>
        <div class="flbc">
          <div class="inspection-status">
            <div
              v-if="isClickSubmit"
              class="inspection-status"
            >
              <div>
                <bk-spin
                  v-if="isDetection"
                  class="spin"
                  size="mini"
                ></bk-spin>
                <span
                  v-else
                  :style="`color:${isRuleCorrect ? '#45E35F' : '#FE5376'}`"
                  :class="['bk-icon spin', isRuleCorrect ? 'icon-check-circle-shape' : 'icon-close-circle-shape']"
                ></span>
              </div>
              <span style="margin-left: 24px">{{ detectionStr }}</span>
            </div>
          </div>

          <div>
            <bk-button
              :disabled="isDetection"
              theme="primary"
              @click="handleRuleSubmit"
            >
              {{ isRuleCorrect ? $t('保存') : $t('检测语法') }}</bk-button
            >
            <bk-button @click="isShowAddRule = false">{{ $t('取消') }}</bk-button>
          </div>
        </div>
      </template>
    </bk-dialog>
  </div>
</template>
<script>
  import { copyMessage, base64Encode, base64Decode } from '@/common/util';
  import EmptyStatus from '@/components/empty-status';
  import RegisterColumn from '@/views/retrieve/result-comp/register-column';
  import ClusterEventPopover from '@/views/retrieve/result-table-panel/log-clustering/components/cluster-event-popover';
  import TextHighlight from 'vue-text-highlight';
  import VueDraggable from 'vuedraggable';

  export default {
    components: {
      VueDraggable,
      ClusterEventPopover,
      RegisterColumn,
      EmptyStatus,
      TextHighlight,
    },
    props: {
      globalEditable: {
        type: Boolean,
        default: true,
      },
      defaultData: {
        type: Object,
        require: true,
      },
      tableStr: {
        type: String,
        require: true,
      },
      cleanConfig: {
        type: Object,
        require: true,
      },
    },
    data() {
      return {
        rulesList: [],
        tableLoading: false,
        logOriginal: '', // 日志源
        effectOriginal: '',
        isShowAddRule: false, // 是否展开添加规则弹窗
        isRuleCorrect: false, // 检测语法是否通过
        isEditRules: false, // 编辑聚类规则
        editRulesIndex: 0, // 当前编辑的index
        isClickSubmit: false, // 是否点击添加
        isDetection: false, // 是否在检测
        debugRequest: false, // 调试中
        detectionStr: '',
        isClickAlertIcon: false,
        addRulesData: {
          regular: '', // 添加聚类规则正则
          placeholder: '', // 添加聚类规则占位符
        },
        rules: {
          regular: [
            {
              validator: this.checkRegular,
              required: true,
              trigger: 'blur',
            },
          ],
          placeholder: [
            {
              regex: /^(?!.*:)\S+/,
              required: true,
              trigger: 'blur',
            },
          ],
        },
        logOriginalRequest: false, // 原始日志是否正在请求
        isFirstInitLogOrigin: false, // 是否第一次点击调试工具按钮
        dragOptions: {
          animation: 150,
          tag: 'ul',
          handle: '.bklog-drag-dots',
          'ghost-class': 'sortable-ghost-class',
        },
        /** 快速导入的dom */
        inputDocument: null,
      };
    },
    watch: {
      tableStr: {
        handler(val) {
          this.rulesList = this.base64ToRuleArr(val);
        },
      },
      addRulesData: {
        deep: true,
        handler() {
          this.resetDetection();
        },
      },
      debugRequest(val) {
        this.$emit('debug-request-change', val);
      },
    },
    mounted() {
      this.initInputType();
    },
    beforeUnmount() {
      this.$emit('debug-request-change', false);
      this.inputDocument.removeEventListener('change', this.inputFileEvent);
      this.inputDocument = null;
    },
    methods: {
      reductionRule() {
        const ruleArr = this.base64ToRuleArr(this.tableStr);
        if (ruleArr.length > 0) {
          this.rulesList = ruleArr;
          this.showTableLoading();
        }
      },
      clusterEdit(index) {
        const [key, val] = Object.entries(this.rulesList[index])[0];
        Object.assign(this.addRulesData, { regular: val, placeholder: key });
        this.editRulesIndex = index;
        this.isEditRules = true;
        this.isShowAddRule = true;
      },
      clusterRemove(index) {
        this.$bkInfo({
          title: this.$t('是否删除该条规则？'),
          confirmFn: () => {
            this.rulesList.splice(index, 1);
            this.showTableLoading();
          },
        });
      },
      /**
       * @desc: 添加规则dialog
       */
      handleRuleSubmit() {
        if (this.isRuleCorrect) {
          this.showTableLoading();
          const newRuleObj = {};
          const { regular, placeholder } = this.addRulesData;
          newRuleObj[placeholder] = regular;
          // 添加渲染列表时不重复的key值
          newRuleObj.__Index__ = new Date().getTime();
          if (this.isEditRules) {
            // 编辑规则替换编辑对象
            this.rulesList.splice(this.editRulesIndex, 1, newRuleObj);
          } else {
            // 检测正则和占位符是否都重复 重复则不添加
            const isRepeat = this.isRulesRepeat(newRuleObj);
            !isRepeat && this.rulesList.push(newRuleObj);
          }
          this.isShowAddRule = false;
        } else {
          // 第一次点击检查时显示文案变化
          this.isDetection = true;
          this.isClickSubmit = true;
          this.detectionStr = this.$t('检验中');
          setTimeout(() => {
            this.isDetection = false;
            this.$refs.addRulesRef.validate().then(
              () => {
                this.isRuleCorrect = true;
                this.detectionStr = this.$t('检验成功');
              },
              () => {
                this.isRuleCorrect = false;
                this.detectionStr = this.$t('检测失败');
              },
            );
          }, 1000);
        }
      },
      /**
       * @desc: 关闭添加规则弹窗重置参数
       */
      cancelAddRuleContent() {
        this.isRuleCorrect = false;
        this.isEditRules = false;
        this.isClickSubmit = false;
        Object.assign(this.addRulesData, { regular: '', placeholder: '' });
        this.$refs.addRulesRef.clearError();
      },
      base64ToRuleArr(str) {
        try {
          const ruleList = JSON.parse(base64Decode(str));
          const ruleNewList = ruleList.reduce((pre, cur, index) => {
            const itemObj = {};
            const matchVal = cur.match(/:(.*)/);
            const key = cur.substring(0, matchVal.index);
            itemObj[key] = matchVal[1];
            itemObj.__Index__ = index;
            pre.push(itemObj);
            return pre;
          }, []);
          return ruleNewList;
        } catch (e) {
          return [];
        }
      },
      ruleArrToBase64(arr = []) {
        arr.length === 0 && (arr = this.rulesList);
        try {
          const ruleNewList = arr.reduce((pre, cur) => {
            const key = Object.keys(cur)[0];
            const val = Object.values(cur)[0];
            const rulesStr = JSON.stringify(`${key}:${val}`);
            pre.push(rulesStr);
            return pre;
          }, []);
          const ruleArrStr = `[${ruleNewList.join(' ,')}]`;
          return base64Encode(ruleArrStr);
        } catch (error) {
          return '';
        }
      },
      debugging() {
        this.debugRequest = true;
        this.effectOriginal = '';
        // const inputData = {
        //   dtEventTimeStamp: Date.parse(new Date()) / 1000,
        //   log: this.logOriginal,
        //   uuid: this.generationUUID(),
        // };
        const predefinedVariables = this.ruleArrToBase64(this.rulesList);
        const query = {
          input_data: this.logOriginal,
          predefined_varibles: predefinedVariables,
        };
        this.$http
          .request('/logClustering/debug', { data: { ...query } })
          .then(res => {
            this.effectOriginal = res.data;
          })
          .finally(() => {
            this.debugRequest = false;
          });
      },
      /**
       * @desc: 检测规则和占位符是否重复
       * @param { Object } newRules 检测对象
       * @returns { Boolean }
       */
      isRulesRepeat(newRules = {}) {
        return this.rulesList.some(listItem => {
          const [regexKey, regexVal] = Object.entries(newRules)[0];
          const [listKey, listVal] = Object.entries(listItem)[0];
          return regexKey === listKey && regexVal === listVal;
        });
      },
      handleClickDebugButton() {
        this.isClickAlertIcon = !this.isClickAlertIcon;
        // 请求了一次原始日志后就不再请求
        if (!this.isFirstInitLogOrigin) {
          this.getLogOriginal();
        }
        this.isFirstInitLogOrigin = true;
      },
      /**
       * @desc: 获取原始日志内容
       */
      getLogOriginal() {
        const {
          extra: { collector_config_id: collectorConfigId },
        } = this.cleanConfig;
        if (!collectorConfigId) return;
        this.logOriginalRequest = true;
        this.$http
          .request('source/dataList', {
            params: {
              collector_config_id: collectorConfigId,
            },
          })
          .then(res => {
            if (res.data?.length) {
              const data = res.data[0];
              this.logOriginal = data.etl.data || '';
            }
          })
          .catch(() => {})
          .finally(() => {
            this.logOriginalRequest = false;
          });
      },
      async checkRegular(val) {
        const result = await this.checkRegularRequest(val);
        return result;
      },
      // 检测数据名是否可用
      async checkRegularRequest(val) {
        try {
          const res = await this.$http.request('logClustering/checkRegexp', {
            data: { regexp: val },
          });
          if (res.data) {
            return res.data;
          }
        } catch (error) {
          return false;
        }
      },
      handleMenuClick(option, item) {
        copyMessage(Object.values(item)[0]);
      },
      resetDetection() {
        this.isDetection = false;
        this.isClickSubmit = false;
        this.isRuleCorrect = false;
      },
      showTableLoading() {
        this.tableLoading = true;
        setTimeout(() => {
          this.tableLoading = false;
        }, 500);
      },
      /** 导出规则 */
      handleExportRule(filename = '') {
        if (!this.rulesList.length) {
          this.$bkMessage({
            theme: 'error',
            message: this.$t('聚类规则为空，无法导出规则'),
          });
          return;
        }
        const eleLink = document.createElement('a');

        const date = new Date();
        const Y = `${date.getFullYear()}`;
        const M = `${date.getMonth() + 1 < 10 ? `0${date.getMonth() + 1}` : date.getMonth() + 1}`;
        const D = `${date.getDate()}`;
        const h = `${date.getHours()}`;
        const m = `${date.getMinutes()}`;
        const s = date.getSeconds();
        const time = `${Y}${M}${D}${h}${m}${s}`;
        eleLink.download = filename || `bk_log_search_download_${time}.json`;
        eleLink.style.display = 'none';
        const jsonStr = this.rulesList.reduce((pre, cur, index) => {
          const entriesArr = Object.entries(cur);
          pre[index] = {
            placeholder: entriesArr[0][0],
            rule: entriesArr[0][1],
          };
          return pre;
        }, {});
        // 字符内容转变成blob地址
        const blob = new Blob([JSON.stringify(jsonStr, null, 4)]);
        eleLink.href = URL.createObjectURL(blob);
        // 触发点击
        document.body.appendChild(eleLink);
        eleLink.click();
        document.body.removeChild(eleLink);
      },
      /** 快速添加规则 */
      handleFastAddRule() {
        this.inputDocument.click(); // 本地文件回填
      },
      initInputType() {
        const inputDocument = document.createElement('input');
        inputDocument.type = 'file';
        inputDocument.style.display = 'none';
        inputDocument.addEventListener('change', this.inputFileEvent);
        this.inputDocument = inputDocument;
      },
      getHeightLightList(str) {
        return str.match(/#.*?#/g) || [];
      },
      inputFileEvent() {
        // 检查文件是否选择:
        if (!this.inputDocument.value) return;
        const file = this.inputDocument.files[0];
        // 读取文件:
        const reader = new FileReader();
        reader.onload = e => {
          try {
            this.rulesList = Object.values(JSON.parse(e.target.result)).map((item, index) => {
              if (!item.placeholder || !String(item.rule)) throw new Error('无效的json');
              return {
                [item.placeholder]: String([item.rule]),
                __Index__: index,
              };
            });
          } catch (err) {
            this.$bkMessage({
              theme: 'error',
              message: this.$t('不是有效的json文件'),
            });
          }
        };
        // 以Text的形式读取文件:
        reader.readAsText(file);
      },
    },
  };
</script>
<style lang="scss" scoped>
  @import '@/scss/mixins/flex.scss';

  .cluster-table {
    /* stylelint-disable no-descending-specificity */
    .container-item {
      margin-bottom: 40px;

      .add-box {
        min-width: 48px;

        .bk-icon {
          left: -3px;
          width: 10px;
        }
      }

      &.table-container {
        position: relative;
      }

      .cluster-table {
        border: 1px solid #dcdee5;
        border-bottom: none;
        border-radius: 2px;
      }
    }

    .debug-container {
      position: fixed;
      bottom: 0;
      left: 0;
      z-index: 999;
      width: 100%;
      min-width: 1460px;
      height: 414px;
      background: #fff;
      transition: bottom 0.3s;

      .debug-tool {
        display: flex;
        align-items: center;
        width: 100%;
        height: 40px;
        padding-left: 26px;
        font-size: 14px;
        color: #313238;
        cursor: pointer;
        background: #f0f1f5;
        box-shadow: 0 -1px 0 0 #dcdee5;

        .icon-play-shape {
          margin-right: 4px;
          font-size: 12px;
          transition: transform 0.3s;
          transform: scale(0.8);
        }

        .is-active {
          transform: scale(0.8) rotateZ(90deg);
        }
      }

      .debug-input-box {
        max-width: 1020px;
        padding: 25px 40px;
        margin: 0 auto;

        .debug-alert {
          margin: 8px 0;
        }
      }

      .effect-container {
        height: 100px;
        padding: 5px 10px;
        font-size: 12px;
        line-height: 24px;
        color: #000;
        background: #fafbfd;
        border: 1px solid#DCDEE5;
        border-radius: 2px;
      }

      &.is-hidden {
        bottom: -374px;
      }
    }

    .table-row {
      min-height: 44px;
      font-size: 12px;
      background-color: #fafbfd;
      border-bottom: 1px solid #dcdee5;

      .icon {
        margin: 0 10px 0 4px;
      }

      .bklog-drag-dots {
        width: 16px;
        font-size: 14px;
        color: #979ba5;
        text-align: left;
        cursor: move;
        opacity: 0;
        transition: opacity 0.2s linear;
      }

      &.sortable-ghost-class {
        background: #eaf3ff;
        transition: background 0.2s linear;
      }

      &:hover {
        background: #eaf3ff;
        transition: background 0.2s linear;

        .bklog-drag-dots {
          opacity: 1;
          transition: opacity 0.2s linear;
        }
      }

      &.table-row-li {
        background-color: #fff;
        transition: background 0.3s;

        &:hover {
          background-color: #f0f1f5;
        }
      }

      .row-left {
        display: flex;
        align-items: center;

        .row-left-index {
          width: 80px;
          margin-left: 14px;
        }

        .regular-container {
          width: 600px;
          padding: 2px 10px 2px 2px;
          word-break: break-all;

          .row-left-regular {
            cursor: pointer;
          }
        }
      }

      .row-right > div {
        width: 100px;

        .row-right-item {
          display: inline-block;
          word-break: break-all;
        }

        .bk-button-text {
          font-size: 12px;
        }
      }
    }

    .table-operate {
      position: absolute;
      top: 0;
      right: 0;

      .bk-button {
        margin-left: 2px;
        border-radius: 3px;
      }

      .btn-hover {
        &:hover {
          color: #3a84ff;
          border: 1px solid #3a84ff;
        }
      }
    }

    .no-cluster-rule {
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      height: 200px;
      border-bottom: 1px solid #dcdee5;

      .icon-empty {
        font-size: 80px;
        color: #c3cdd7;
      }
    }

    .log-style {
      height: 100px;

      :deep(.bk-form-textarea:focus) {
        /* stylelint-disable-next-line declaration-no-important */
        background-color: #313238 !important;
        border-radius: 2px;
      }

      :deep(.bk-form-textarea[disabled]) {
        /* stylelint-disable-next-line declaration-no-important */
        background-color: #313238 !important;
        border-radius: 2px;
      }

      :deep(.bk-textarea-wrapper) {
        border: none;
      }
    }

    .add-rule {
      .bk-form {
        width: 560px;
        margin-left: 15px;

        :deep(.bk-label) {
          text-align: left;
        }
      }
    }

    .fl-jfsb {
      @include flex-justify(space-between);
    }

    .mt18 {
      margin-top: 18px;
    }
  }

  .flbc {
    display: flex;
    align-items: center;
    justify-content: space-between;
  }

  .inspection-status {
    position: relative;
    display: flex;
    font-size: 14px;

    .bk-icon {
      font-size: 18px;
    }

    .spin {
      position: absolute;
      top: 2px;
    }
  }
</style>
