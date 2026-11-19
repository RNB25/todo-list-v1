<template>
  <div class="stats-grid">
    <div class="stat-card">
      <div class="stat-header">
        <span class="stat-label">Total Todos</span>
        <div class="stat-icon-wrapper icon-total">
          <Layers :size="18" />
        </div>
      </div>
      <div class="stat-value">{{ totalItems.toLocaleString('id-ID') }}</div>
      <div class="stat-hint">Terdaftar di database MySQL</div>
    </div>

    <div class="stat-card" @click="$emit('filter-status', 'pending')" style="cursor: pointer;">
      <div class="stat-header">
        <span class="stat-label">Pending</span>
        <div class="stat-icon-wrapper icon-pending">
          <Clock :size="18" />
        </div>
      </div>
      <div class="stat-value">{{ pendingCount.toLocaleString('id-ID') }}</div>
      <div class="stat-hint">Menunggu dikerjakan</div>
    </div>

    <div class="stat-card" @click="$emit('filter-status', 'progress')" style="cursor: pointer;">
      <div class="stat-header">
        <span class="stat-label">In Progress</span>
        <div class="stat-icon-wrapper icon-progress">
          <Activity :size="18" />
        </div>
      </div>
      <div class="stat-value">{{ progressCount.toLocaleString('id-ID') }}</div>
      <div class="stat-hint">Sedang berjalan</div>
    </div>

    <div class="stat-card" @click="$emit('filter-status', 'done')" style="cursor: pointer;">
      <div class="stat-header">
        <span class="stat-label">Done</span>
        <div class="stat-icon-wrapper icon-done">
          <CheckCircle2 :size="18" />
        </div>
      </div>
      <div class="stat-value">{{ doneCount.toLocaleString('id-ID') }}</div>
      <div class="stat-hint">Pekerjaan terselesaikan</div>
    </div>
  </div>
</template>

<script setup>
import { Layers, Clock, Activity, CheckCircle2 } from 'lucide-vue-next'

defineProps({
  totalItems: {
    type: Number,
    default: 0
  },
  pendingCount: {
    type: Number,
    default: 0
  },
  progressCount: {
    type: Number,
    default: 0
  },
  doneCount: {
    type: Number,
    default: 0
  }
})

defineEmits(['filter-status'])
</script>

<style scoped>
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 16px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  box-shadow: var(--shadow-sm);
  transition: all 0.2s ease;
}

.stat-card:hover {
  background: var(--bg-card-hover);
  border-color: var(--border-hover);
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

.stat-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.stat-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.stat-icon-wrapper {
  width: 34px;
  height: 34px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
}

.icon-total {
  background: rgba(59, 130, 246, 0.15);
  color: #60a5fa;
}

.icon-pending {
  background: rgba(148, 163, 184, 0.15);
  color: #cbd5e1;
}

.icon-progress {
  background: rgba(245, 158, 11, 0.15);
  color: #fbbf24;
}

.icon-done {
  background: rgba(16, 185, 129, 0.15);
  color: #34d399;
}

.stat-value {
  font-size: 28px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: var(--text-primary);
  line-height: 1.1;
}

.stat-hint {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 6px;
}
</style>
