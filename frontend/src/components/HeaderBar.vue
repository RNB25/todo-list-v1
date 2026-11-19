<template>
  <header class="header">
    <div class="header-inner">
      <div class="brand-group">
        <div class="brand-logo" aria-hidden="true">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
            <polyline points="9 11 12 14 22 4"></polyline>
            <path d="M21 12v7a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h11"></path>
          </svg>
        </div>
        <div class="brand-meta">
          <div class="brand-title-row">
            <h1 class="brand-title">Todo Studio</h1>
            <span class="engine-badge">MySQL 8.0</span>
          </div>
          <div class="brand-sub">
            <span>FastAPI Backend</span>
            <span class="sep">/</span>
            <span>UUIDv7 Binary</span>
            <span class="sep">/</span>
            <a href="http://127.0.0.1:8000/docs" target="_blank" class="docs-link" title="Buka dokumentasi Swagger UI">
              Swagger <ArrowUpRight :size="11" />
            </a>
          </div>
        </div>
      </div>

      <div class="header-actions">
        <!-- Live Health Status Badge -->
        <div 
          class="health-badge" 
          :class="`health-${healthStatus}`" 
          :title="`Health Check: ${healthStatus === 'healthy' ? 'MySQL & FastAPI Terhubung' : 'Terputus'}`"
        >
          <span class="pulse-dot"></span>
          <span class="health-label">{{ healthStatus === 'healthy' ? 'MySQL Online' : 'Degraded' }}</span>
        </div>

        <button 
          class="btn btn-bulk" 
          @click="$emit('open-bulk')" 
          :disabled="loading"
          title="Tekan tombol 'B' untuk shortcut"
        >
          <Database :size="14" />
          <span>Generate Data</span>
          <kbd>B</kbd>
        </button>

        <button 
          class="btn btn-primary" 
          @click="$emit('open-create')" 
          :disabled="loading"
          title="Tekan tombol 'N' untuk shortcut"
        >
          <Plus :size="15" />
          <span>Buat Todo</span>
          <kbd class="kbd-inverse">N</kbd>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { Plus, Database, ArrowUpRight } from 'lucide-vue-next'

defineProps({
  healthStatus: {
    type: String,
    default: 'healthy'
  },
  loading: {
    type: Boolean,
    default: false
  }
})

defineEmits(['open-create', 'open-bulk'])
</script>

<style scoped>
.header {
  background: rgba(14, 16, 19, 0.85);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-subtle);
  position: sticky;
  top: 0;
  z-index: 30;
}

.header-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.brand-group {
  display: flex;
  align-items: center;
  gap: 12px;
}

.brand-logo {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  background: #181b21;
  border: 1px solid var(--border-default);
  color: #f4f4f5;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.15);
}

.brand-meta {
  display: flex;
  flex-direction: column;
  gap: 1px;
}

.brand-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand-title {
  font-size: 15px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: #ffffff;
}

.engine-badge {
  font-family: var(--font-mono);
  font-size: 10px;
  font-weight: 600;
  color: #38bdf8;
  background: rgba(56, 189, 248, 0.1);
  border: 1px solid rgba(56, 189, 248, 0.25);
  padding: 1px 6px;
  border-radius: var(--radius-xs);
  letter-spacing: 0.02em;
}

.brand-sub {
  font-size: 11px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  gap: 6px;
}

.sep {
  opacity: 0.4;
}

.docs-link {
  color: var(--text-secondary);
  text-decoration: none;
  display: inline-flex;
  align-items: center;
  gap: 2px;
  transition: color 0.12s;
}

.docs-link:hover {
  color: #ffffff;
  text-decoration: underline;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 10px;
}

/* Health Badge */
.health-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 4px 10px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 500;
  font-family: var(--font-mono);
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  transition: all 0.2s;
}

.pulse-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  position: relative;
}

.health-healthy .pulse-dot {
  background-color: #10b981;
  box-shadow: 0 0 0 3px rgba(16, 185, 129, 0.2);
}

.health-degraded .pulse-dot {
  background-color: #f59e0b;
  box-shadow: 0 0 0 3px rgba(245, 158, 11, 0.2);
}

.health-healthy {
  color: #a7f3d0;
}

.health-degraded {
  color: #fde68a;
}

.kbd-inverse {
  background: rgba(0, 0, 0, 0.12);
  border-color: rgba(0, 0, 0, 0.2);
  color: #27272a;
}

@media (max-width: 640px) {
  .brand-sub, kbd {
    display: none;
  }
}
</style>
