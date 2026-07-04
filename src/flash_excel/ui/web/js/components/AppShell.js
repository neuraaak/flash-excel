import SettingsModal from './SettingsModal.js';
import LucideIcon    from './LucideIcon.js';
import { api }       from '../api.js';

export default {
  name: 'AppShell',
  components: { SettingsModal, LucideIcon },
  props: { currentPage: { type: String, default: 'processing' } },
  emits: ['navigate'],

  data() {
    return {
      showSettings:    false,
      sidebarExpanded: false,
      _windowWide:     false,
      version:         '',
      update:          { available: false, version: null },
      updating:        false,
    };
  },

  mounted() {
    const BREAKPOINT = 860;
    const update = () => {
      const wide = window.innerWidth >= BREAKPOINT;
      if (wide !== this._windowWide) {
        this._windowWide = wide;
        this.sidebarExpanded = wide;
      }
    };
    this._ro = new ResizeObserver(update);
    this._ro.observe(document.documentElement);
    update();

    // Version + vérification de mise à jour (attend que pywebview soit prêt).
    if (globalThis.pywebview?.api) this._initVersion();
    else globalThis.addEventListener('pywebviewready', () => this._initVersion(), { once: true });
  },

  beforeUnmount() {
    this._ro?.disconnect();
  },

  methods: {
    toggleSidebar() {
      this.sidebarExpanded = !this.sidebarExpanded;
    },

    async _initVersion() {
      try {
        const v = await api.getVersion();
        this.version = v.version;
      } catch (e) { console.debug('getVersion failed', e); }
      try {
        this.update = await api.checkUpdate();
      } catch (e) { console.debug('checkUpdate failed', e); }
    },

    async applyUpdate() {
      if (this.updating) return;
      this.updating = true;
      try {
        await api.applyUpdate();
        // Si la maj s'applique, l'app se ferme puis redémarre (tufup).
      } catch (e) {
        console.debug('applyUpdate failed', e);
        this.updating = false;
      }
    },
  },

  template: `
    <div class="app">

      <!-- Main (sidebar + page area) -->
      <div class="main">
        <nav class="sidebar" :class="{ expanded: sidebarExpanded }">

          <!-- Toggle -->
          <button class="nav-btn nav-toggle" @click="toggleSidebar" title="Toggle menu">
            <span class="nav-ico">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round">
                <path d="M4 6h16M4 12h16M4 18h16"/>
              </svg>
            </span>
            <span class="nav-label">Menu</span>
          </button>

          <div class="nav-sep"></div>

          <!-- Processing -->
          <button class="nav-btn" :class="{ active: currentPage === 'processing' }"
            title="Processing" @click="$emit('navigate', 'processing')">
            <span class="nav-ico">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                <path d="M13 2L4.5 13H11l-1 9 8.5-11.5H12z"/>
              </svg>
            </span>
            <span class="nav-label">Processing</span>
          </button>

          <!-- Presets -->
          <button class="nav-btn" :class="{ active: currentPage === 'presets' }"
            title="Presets" @click="$emit('navigate', 'presets')">
            <span class="nav-ico">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
                <path d="M5 7h6M5 12h10M5 17h6"/>
                <circle cx="17" cy="7" r="2"/>
                <circle cx="18" cy="17" r="2"/>
              </svg>
            </span>
            <span class="nav-label">Presets</span>
          </button>

          <div class="nav-spacer"></div>
          <div class="nav-sep"></div>

          <!-- Settings -->
          <button class="nav-btn" :class="{ active: showSettings }"
            title="Settings" @click="showSettings = true">
            <span class="nav-ico">
              <LucideIcon name="settings" :size="18" />
            </span>
            <span class="nav-label">Settings</span>
          </button>

        </nav>

        <div class="page-area">
          <slot />
        </div>
      </div>

      <!-- Footer -->
      <footer class="footer">
        <div class="footer-left">Made with <span class="heart">&#10084;</span> by Flash-Excel</div>
        <div class="footer-version">
          <a v-if="update.available" class="update-link" href="#" @click.prevent="applyUpdate"
             :title="'Update to v' + update.version">
            {{ updating ? 'Updating…' : 'Update to v' + update.version }}
          </a>
          <span>v{{ version || '—' }}</span>
        </div>
      </footer>

      <!-- Settings popup -->
      <SettingsModal v-if="showSettings" @close="showSettings = false" />

    </div>
  `,
};
