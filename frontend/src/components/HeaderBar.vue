<template>
  <header class="header">
    <div class="header-inner">
      <div class="brand-group">
        <div class="brand-icon">
          <CheckSquare :size="24" />
        </div>
        <div>
          <div class="brand-title-row">
            <h1 class="brand-title">Sistem Todo List</h1>
            <span class="version-tag">v1.0</span>
          </div>
          <div class="tech-stack-row">
            <span class="tech-item">FastAPI</span>
            <span class="dot">·</span>
            <span class="tech-item">MySQL 8.0</span>
            <span class="dot">·</span>
            <span class="tech-item">Vue 3</span>
            <span class="dot">·</span>
            <span class="tech-item">UUID v7</span>
          </div>
        </div>
      </div>

      <div class="header-actions">
        <!-- Live Health Status Badge -->
        <div class="health-badge" :class="`health-${healthStatus}`" :title="`Status Backend: ${healthStatus}`">
          <span class="status-indicator"></span>
          <span class="health-text">{{ healthStatus === 'healthy' ? 'API Online' : 'Connecting...' }}</span>
        </div>

        <button class="btn btn-bulk" @click="$emit('open-bulk')" :disabled="loading">
          <Sparkles :size="16" />
          <span>Generate 1.000 Data</span>
        </button>

        <button class="btn btn-primary" @click="$emit('open-create')" :disabled="loading">
          <Plus :size="16" />
          <span>Tambah Todo</span>
        </button>
      </div>
    </div>
  </header>
</template>

<script setup>
import { CheckSquare, Plus, Sparkles } from 'lucide-vue-next'

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
  background: var(--bg-surface);
  border-bottom: 1px solid var(--border-subtle);
  position: sticky;
  top: 0;
  z-index: 30;
  box-shadow: var(--shadow-sm);
}

.header-inner {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 16px 24px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.brand-group {
  display: flex;
  align-items: center;
  gap: 14px;
}

.brand-icon {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, #1d4ed8, #0ea5e9);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(29, 78, 216, 0.4);
}

.brand-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.brand-title {
  font-size: 19px;
  font-weight: 700;
  letter-spacing: -0.02em;
  color: var(--text-primary);
}

.version-tag {
  font-size: 11px;
  font-weight: 600;
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
  padding: 2px 7px;
  border-radius: var(--radius-full);
}

.tech-stack-row {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.dot {
  opacity: 0.5;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.health-badge {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 6px 12px;
  border-radius: var(--radius-full);
  background: rgba(15, 23, 42, 0.6);
  border: 1px solid var(--border-subtle);
  font-size: 12px;
  font-weight: 500;
}

.status-indicator {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.health-healthy .status-indicator {
  background: #10b981;
  box-shadow: 0 0 8px #10b981;
}
.health-healthy .health-text {
  color: #34d399;
}

.health-degraded .status-indicator {
  background: #f59e0b;
  box-shadow: 0 0 8px #f59e0b;
}
.health-degraded .health-text {
  color: #fbbf24;
}

@media (max-width: 768px) {
  .header-inner {
    flex-direction: column;
    align-items: stretch;
    padding: 12px 16px;
  }
  .header-actions {
    justify-content: stretch;
    width: 100%;
  }
  .header-actions .btn {
    flex: 1;
  }
}
</style>
