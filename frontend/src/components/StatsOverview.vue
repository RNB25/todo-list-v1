<template>
  <div class="metrics-ribbon">
    <div class="metrics-grid">
      <!-- Total metric -->
      <div class="metric-item metric-all" @click="$emit('filter-status', '')" role="button" tabindex="0">
        <div class="metric-top">
          <span class="metric-name">Total Items</span>
          <span class="metric-badge">All</span>
        </div>
        <div class="metric-value">{{ totalItems.toLocaleString('id-ID') }}</div>
        <div class="metric-sub">Tersimpan di MySQL</div>
      </div>

      <!-- Pending metric -->
      <div 
        class="metric-item metric-pending" 
        :class="{ active: currentStatus === 'pending' }"
        @click="$emit('filter-status', 'pending')" 
        role="button" 
        tabindex="0"
      >
        <div class="metric-top">
          <span class="metric-name">Pending</span>
          <span class="status-indicator-dot dot-pending"></span>
        </div>
        <div class="metric-value">{{ pendingCount.toLocaleString('id-ID') }}</div>
        <div class="metric-sub">{{ calculatePercent(pendingCount) }}% antrean</div>
      </div>

      <!-- In Progress metric -->
      <div 
        class="metric-item metric-progress" 
        :class="{ active: currentStatus === 'progress' }"
        @click="$emit('filter-status', 'progress')" 
        role="button" 
        tabindex="0"
      >
        <div class="metric-top">
          <span class="metric-name">In Progress</span>
          <span class="status-indicator-dot dot-progress"></span>
        </div>
        <div class="metric-value">{{ progressCount.toLocaleString('id-ID') }}</div>
        <div class="metric-sub">{{ calculatePercent(progressCount) }}% aktif</div>
      </div>

      <!-- Done metric -->
      <div 
        class="metric-item metric-done" 
        :class="{ active: currentStatus === 'done' }"
        @click="$emit('filter-status', 'done')" 
        role="button" 
        tabindex="0"
      >
        <div class="metric-top">
          <span class="metric-name">Completed</span>
          <span class="status-indicator-dot dot-done"></span>
        </div>
        <div class="metric-value">{{ doneCount.toLocaleString('id-ID') }}</div>
        <div class="metric-sub">{{ calculatePercent(doneCount) }}% selesai</div>
      </div>
    </div>

    <!-- Segmented Completion Meter -->
    <div class="completion-bar-wrapper">
      <div class="completion-meta">
        <div class="completion-rate">
          <span class="rate-value">{{ completionRate }}%</span>
          <span class="rate-label">Tingkat Penyelesaian</span>
        </div>
        <div class="completion-legend">
          <span class="legend-item"><span class="legend-dot dot-done"></span> Done</span>
          <span class="legend-item"><span class="legend-dot dot-progress"></span> Progress</span>
          <span class="legend-item"><span class="legend-dot dot-pending"></span> Pending</span>
        </div>
      </div>
      <div class="progress-bar-track" :title="`Done: ${doneCount}, Progress: ${progressCount}, Pending: ${pendingCount}`">
        <div 
          class="progress-segment segment-done" 
          :style="{ width: `${calculatePercent(doneCount)}%` }"
        ></div>
        <div 
          class="progress-segment segment-progress" 
          :style="{ width: `${calculatePercent(progressCount)}%` }"
        ></div>
        <div 
          class="progress-segment segment-pending" 
          :style="{ width: `${calculatePercent(pendingCount)}%` }"
        ></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
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
  },
  currentStatus: {
    type: String,
    default: ''
  }
})

defineEmits(['filter-status'])

function calculatePercent(count) {
  if (!props.totalItems || props.totalItems === 0) return 0
  return Math.round((count / props.totalItems) * 100)
}

const completionRate = computed(() => {
  if (!props.totalItems || props.totalItems === 0) return 0
  return Math.round((props.doneCount / props.totalItems) * 100)
})
</script>

<style scoped>
.metrics-ribbon {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 18px 20px;
  margin-bottom: 20px;
  box-shadow: var(--shadow-card);
}

.metrics-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 16px;
}

.metric-item {
  padding: 12px 14px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.14s ease;
  user-select: none;
}

.metric-item:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: var(--border-default);
  transform: translateY(-1px);
}

.metric-item.active {
  background: rgba(255, 255, 255, 0.08);
  border-color: rgba(255, 255, 255, 0.3);
}

.metric-top {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.metric-name {
  font-size: 11px;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.metric-badge {
  font-family: var(--font-mono);
  font-size: 10px;
  color: var(--text-muted);
  background: rgba(255, 255, 255, 0.06);
  padding: 1px 5px;
  border-radius: var(--radius-xs);
}

.status-indicator-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.dot-pending { background-color: var(--status-pending); }
.dot-progress { background-color: var(--status-progress); }
.dot-done { background-color: var(--status-done); }

.metric-value {
  font-size: 22px;
  font-weight: 700;
  letter-spacing: -0.03em;
  color: #ffffff;
  font-family: var(--font-mono);
  line-height: 1.1;
  margin-bottom: 4px;
}

.metric-sub {
  font-size: 11px;
  color: var(--text-muted);
}

/* Completion Bar */
.completion-bar-wrapper {
  padding-top: 14px;
  border-top: 1px solid var(--border-subtle);
}

.completion-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 8px;
}

.completion-rate {
  display: flex;
  align-items: baseline;
  gap: 6px;
}

.rate-value {
  font-size: 14px;
  font-weight: 700;
  font-family: var(--font-mono);
  color: #ffffff;
}

.rate-label {
  font-size: 11px;
  color: var(--text-muted);
}

.completion-legend {
  display: flex;
  align-items: center;
  gap: 14px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 11px;
  color: var(--text-secondary);
}

.legend-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.progress-bar-track {
  height: 6px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: var(--radius-full);
  display: flex;
  overflow: hidden;
  gap: 2px;
}

.progress-segment {
  height: 100%;
  transition: width 0.4s cubic-bezier(0.16, 1, 0.3, 1);
}

.segment-done { background: var(--status-done); }
.segment-progress { background: var(--status-progress); }
.segment-pending { background: rgba(148, 163, 184, 0.5); }

@media (max-width: 768px) {
  .metrics-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
