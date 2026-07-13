// Registre partagé des steps du pipeline : ordre canonique + clés i18n.
// Utilisé par ActionSteps.js (config des presets) et Processing.js (console
// + preview) pour afficher un nom traduit au lieu de l'action technique brute
// (ex: "rename_columns").

export const STEP_ACTIONS = [
  'rename_columns', 'select_columns', 'cast_types', 'replace_values',
  'clean_text', 'add_computed_column', 'filter_rows', 'deduplicate_rows',
  'sort_rows', 'reorder_columns',
];

const STEP_I18N_KEYS = {
  rename_columns: 'steps.rename',
  select_columns: 'steps.select',
  cast_types: 'steps.cast',
  replace_values: 'steps.replace',
  clean_text: 'steps.clean',
  add_computed_column: 'steps.computed',
  filter_rows: 'steps.filter',
  deduplicate_rows: 'steps.dedupe',
  sort_rows: 'steps.sort',
  reorder_columns: 'steps.reorder',
};

/** Nom traduit d'un step (fallback : l'action technique si inconnue). */
export function stepLabel(action, t) {
  const key = STEP_I18N_KEYS[action];
  return key ? t(key) : action;
}

/** Description traduite d'un step. */
export function stepDesc(action, t) {
  const key = STEP_I18N_KEYS[action];
  return key ? t(`${key}.desc`) : '';
}
