import { toRaw } from '../../vendor/vue.esm-browser.prod.js';

const OPS_BASE = [
  { value: 'eq', label: '=' }, { value: 'neq', label: '≠' },
  { value: 'gt', label: '>' }, { value: 'gte', label: '≥' },
  { value: 'lt', label: '<' }, { value: 'lte', label: '≤' },
  { value: 'contains', labelKey: 'table.op_contains' },
  { value: 'startswith', labelKey: 'table.op_startswith' },
  { value: 'endswith', labelKey: 'table.op_endswith' },
];

export default {
  name: 'FilterTable',
  props: { columns: { type: Array, default: () => [] }, payload: { type: Object, default: () => ({}) } },
  emits: ['update:payload'],
  inject: ['i18n'],
  computed: {
    t() { return this.i18n.t; },
    ops() { return OPS_BASE.map(o => ({ value: o.value, label: o.labelKey ? this.t(o.labelKey) : o.label })); },
  },
  data() { return { combine: 'AND', conditions: [] }; },
  watch: {
    payload: {
      immediate: true, handler(v) {
        if (this._emitting) return;
        this.combine = v.combine || 'AND';
        this.conditions = (v.conditions?.length) ? structuredClone(toRaw(v.conditions)) : [];
      }
    },
  },
  methods: {
    emit() {
      this._emitting = true;
      this.$emit('update:payload', {
        action: 'filter_rows',
        combine: this.combine,
        conditions: this.conditions.filter(c => c.column && c.value !== ''),
      });
      this.$nextTick(() => { this._emitting = false; });
    },
    setCombine(v) { this.combine = v; this.emit(); },
    addRow() { this.conditions.push({ column: this.columns[0] || '', operator: 'eq', value: '' }); this.emit(); },
    removeRow(i) { this.conditions.splice(i, 1); this.emit(); },
  },
  template: `
    <div>
      <div class="row-between" style="margin-bottom:14px;">
        <span class="field-label">{{ t('table.filter_keep_matching') }}</span>
        <span class="seg">
          <button :class="{ active: combine === 'AND' }" @click="setCombine('AND')">{{ t('table.filter_all') }}</button>
          <button :class="{ active: combine === 'OR' }"  @click="setCombine('OR')">{{ t('table.filter_any') }}</button>
        </span>
      </div>
      <div v-if="!conditions.length" class="empty-state">
        <span class="es-title">{{ t('table.filter_empty_title') }}</span>
        <span class="es-sub">{{ t('table.filter_empty_sub') }}</span>
      </div>
      <div v-else class="rule-list">
        <div v-for="(c, i) in conditions" :key="i" class="rule-row" style="grid-template-columns:1.2fr 1.2fr 1fr var(--ctl-h);">
          <span class="select-wrap">
            <select v-model="c.column" @change="emit">
              <option v-if="c.column && !columns.includes(c.column)" :value="c.column">{{ c.column }}</option>
              <option v-for="col in columns" :key="col" :value="col">{{ col }}</option>
            </select>
          </span>
          <span class="select-wrap">
            <select v-model="c.operator" @change="emit">
              <option v-for="op in ops" :key="op.value" :value="op.value">{{ op.label }}</option>
            </select>
          </span>
          <input class="input" v-model="c.value" :placeholder="t('table.value')" @input="emit" />
          <button class="rule-del" @click="removeRow(i)" title="Remove">
            <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>
          </button>
        </div>
      </div>
      <button class="add-rule" @click="addRow">
        <svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M12 5v14M5 12h14"/></svg>
        {{ t('table.add_rule') }}
      </button>
    </div>
  `,
};
