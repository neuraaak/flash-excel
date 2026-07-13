export default {
  name: 'ReorderTable',
  props: { columns: { type: Array, default: () => [] }, payload: { type: Object, default: () => ({}) } },
  emits: ['update:payload'],
  inject: ['i18n'],
  computed: {
    t() { return this.i18n.t; },
  },
  data() { return { order: [], dragIndex: null, dragOverIndex: null }; },
  watch: {
    columns: { immediate: true, handler(v) { if (!this.order.length && v.length) this.order = [...v]; } },
    payload: {
      immediate: true, handler(v) {
        const cols = v.columns?.length ? v.columns : this.columns;
        this.order = cols.length ? [...cols] : [...this.order];
      }
    },
  },
  methods: {
    move(i, dir) {
      const j = i + dir;
      if (j < 0 || j >= this.order.length) return;
      const next = [...this.order];
      [next[i], next[j]] = [next[j], next[i]];
      this.order = next;
      this.emitOrder();
    },
    emitOrder() {
      this.$emit('update:payload', { action: 'reorder_columns', columns: [...this.order] });
    },
    onDragStart(i, evt) {
      this.dragIndex = i;
      evt.dataTransfer.effectAllowed = 'move';
      evt.dataTransfer.setData('text/plain', String(i));
    },
    onDragOver(i) { this.dragOverIndex = i; },
    onDrop(i) {
      if (this.dragIndex === null || this.dragIndex === i) { this.dragOverIndex = null; return; }
      const next = [...this.order];
      const [moved] = next.splice(this.dragIndex, 1);
      next.splice(i, 0, moved);
      this.order = next;
      this.dragIndex = null;
      this.dragOverIndex = null;
      this.emitOrder();
    },
    onDragEnd() { this.dragIndex = null; this.dragOverIndex = null; },
  },
  template: `
    <div>
      <div class="panel-sub">{{ t('table.col_order') }}</div>
      <div class="order-list">
        <div v-for="(col, i) in order" :key="col" class="order-row"
          :class="{ dragging: dragIndex === i, 'drag-over': dragOverIndex === i && dragIndex !== i }"
          draggable="true"
          @dragstart="onDragStart(i, $event)"
          @dragover.prevent="onDragOver(i)"
          @drop.prevent="onDrop(i)"
          @dragend="onDragEnd">
          <span class="order-grip" title="Reorder" style="cursor:grab">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="currentColor"><circle cx="9" cy="6" r="1.6"/><circle cx="15" cy="6" r="1.6"/><circle cx="9" cy="12" r="1.6"/><circle cx="15" cy="12" r="1.6"/><circle cx="9" cy="18" r="1.6"/><circle cx="15" cy="18" r="1.6"/></svg>
          </span>
          <span class="order-idx">{{ i + 1 }}</span>
          <span class="order-dot"></span>
          <span class="order-name">{{ col }}</span>
          <span class="order-arrows">
            <span class="arr" :class="{ disabled: i === 0 }" @click="move(i, -1)" title="Move up">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M18 15l-6-6-6 6"/></svg>
            </span>
            <span class="arr" :class="{ disabled: i === order.length - 1 }" @click="move(i, 1)" title="Move down">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M6 9l6 6 6-6"/></svg>
            </span>
          </span>
        </div>
      </div>
    </div>
  `,
};
