export default {
  name: 'SelectTable',
  props: { columns: { type: Array, default: () => [] }, payload: { type: Object, default: () => ({}) } },
  emits: ['update:payload'],
  inject: ['i18n'],
  computed: {
    t() { return this.i18n.t; },
    effectiveColumns() {
      return this.columns.length ? this.columns : (this.payload.columns || []);
    },
    selected() {
      const s = this.payload.columns;
      return Array.isArray(s) && s.length ? s : [...this.effectiveColumns];
    },
  },
  methods: {
    isOn(col) { return this.selected.includes(col); },
    toggle(col) {
      const set = new Set(this.selected);
      if (set.has(col)) set.delete(col); else set.add(col);
      const cols = this.effectiveColumns.filter(c => set.has(c));
      this.$emit('update:payload', { action: 'select_columns', columns: cols });
    },
  },
  template: `
    <div>
      <div class="row-between" style="margin-bottom:10px;">
        <span class="panel-sub" style="margin:0;">{{ t('table.keep_cols') }}</span>
        <span style="font-size:var(--fs-xs);color:var(--text_secondary);">{{ t('table.select_kept', { n: selected.length, total: effectiveColumns.length }) }}</span>
      </div>
      <div class="toggle-list">
        <div v-for="col in effectiveColumns" :key="col" class="toggle-row" :class="{ on: isOn(col) }">
          <span class="tr-name">{{ col }}</span>
          <label class="switch">
            <input type="checkbox" :checked="isOn(col)" @change="toggle(col)">
            <span class="track"></span>
          </label>
        </div>
      </div>
      <div class="panel-hint">{{ t('table.select_hint') }}</div>
    </div>
  `,
};
