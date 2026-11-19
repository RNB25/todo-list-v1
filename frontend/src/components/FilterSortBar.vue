<template>
  <div class="filter-card">
    <div class="filter-row primary-row">
      <!-- Search Input -->
      <div class="search-box">
        <Search :size="16" class="search-icon" />
        <input
          type="text"
          v-model="localQ"
          placeholder="Cari berdasarkan judul atau deskripsi..."
          class="search-input"
          @keydown.enter="applySearch"
        />
        <button
          v-if="localQ"
          class="clear-search-btn"
          @click="clearSearch"
          title="Hapus pencarian"
        >
          <X :size="14" />
        </button>
      </div>

      <!-- Quick Status Filters -->
      <div class="status-tabs" role="tablist">
        <button
          v-for="tab in statusTabs"
          :key="tab.value"
          class="status-tab"
          :class="{ active: currentStatus === tab.value }"
          @click="selectStatus(tab.value)"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <div class="filter-row secondary-row">
      <!-- Priority Dropdown -->
      <div class="filter-item">
        <label class="filter-label">Prioritas:</label>
        <select
          :value="currentPriority"
          @change="onPriorityChange($event.target.value)"
          class="filter-select"
        >
          <option value="">Semua Prioritas</option>
          <option value="low">Low</option>
          <option value="medium">Medium</option>
          <option value="high">High</option>
        </select>
      </div>

      <!-- Sort By Dropdown -->
      <div class="filter-item">
        <label class="filter-label">Urutkan:</label>
        <select
          :value="currentSortBy"
          @change="onSortByChange($event.target.value)"
          class="filter-select"
        >
          <option value="created_at">Waktu Dibuat</option>
          <option value="updated_at">Waktu Diperbarui</option>
          <option value="title">Judul (A-Z)</option>
          <option value="status">Status</option>
          <option value="priority">Prioritas</option>
        </select>
      </div>

      <!-- Sort Order Toggle -->
      <button
        class="btn btn-secondary btn-sm sort-toggle-btn"
        @click="toggleSortOrder"
        :title="`Arah urutan: ${currentSortOrder.toUpperCase()}`"
      >
        <ArrowDownNarrowWide v-if="currentSortOrder === 'desc'" :size="15" />
        <ArrowUpWideNarrow v-else :size="15" />
        <span>{{ currentSortOrder === 'desc' ? 'Terbaru / Desc' : 'Terlama / Asc' }}</span>
      </button>

      <!-- Page Size Selector -->
      <div class="filter-item">
        <label class="filter-label">Per Halaman:</label>
        <select
          :value="currentPageSize"
          @change="onPageSizeChange(Number($event.target.value))"
          class="filter-select select-compact"
        >
          <option :value="10">10</option>
          <option :value="20">20</option>
          <option :value="50">50</option>
          <option :value="100">100</option>
        </select>
      </div>

      <!-- Reset Filters Button -->
      <button
        v-if="hasActiveFilters"
        class="btn btn-sm btn-secondary reset-btn"
        @click="$emit('reset-filters')"
        title="Reset semua filter ke pengaturan default"
      >
        <RotateCcw :size="13" />
        <span>Reset Filter</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import {
  Search,
  X,
  RotateCcw,
  ArrowDownNarrowWide,
  ArrowUpWideNarrow
} from 'lucide-vue-next'

const props = defineProps({
  currentStatus: { type: String, default: '' },
  currentPriority: { type: String, default: '' },
  currentQ: { type: String, default: '' },
  currentSortBy: { type: String, default: 'created_at' },
  currentSortOrder: { type: String, default: 'desc' },
  currentPageSize: { type: Number, default: 20 }
})

const emit = defineEmits([
  'update:status',
  'update:priority',
  'update:q',
  'update:sortBy',
  'update:sortOrder',
  'update:pageSize',
  'reset-filters'
])

const localQ = ref(props.currentQ)

watch(() => props.currentQ, (newVal) => {
  localQ.value = newVal
})

let searchTimeout = null
watch(localQ, (newVal) => {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    emit('update:q', newVal)
  }, 400)
})

const applySearch = () => {
  clearTimeout(searchTimeout)
  emit('update:q', localQ.value)
}

const clearSearch = () => {
  localQ.value = ''
  emit('update:q', '')
}

const statusTabs = [
  { label: 'Semua Status', value: '' },
  { label: 'Pending', value: 'pending' },
  { label: 'Progress', value: 'progress' },
  { label: 'Done', value: 'done' }
]

const selectStatus = (val) => {
  emit('update:status', val)
}

const onPriorityChange = (val) => {
  emit('update:priority', val)
}

const onSortByChange = (val) => {
  emit('update:sortBy', val)
}

const toggleSortOrder = () => {
  const nextOrder = props.currentSortOrder === 'desc' ? 'asc' : 'desc'
  emit('update:sortOrder', nextOrder)
}

const onPageSizeChange = (val) => {
  emit('update:pageSize', val)
}

const hasActiveFilters = computed(() => {
  return (
    props.currentStatus !== '' ||
    props.currentPriority !== '' ||
    props.currentQ !== '' ||
    props.currentSortBy !== 'created_at' ||
    props.currentSortOrder !== 'desc' ||
    props.currentPageSize !== 20
  )
})
</script>

<style scoped>
.filter-card {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 16px 20px;
  margin-bottom: 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.filter-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.primary-row {
  justify-content: space-between;
}

.search-box {
  position: relative;
  flex: 1;
  min-width: 260px;
}

.search-icon {
  position: absolute;
  left: 12px;
  top: 50%;
  transform: translateY(-50%);
  color: var(--text-muted);
}

.search-input {
  width: 100%;
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 10px 36px 10px 36px;
  color: var(--text-primary);
  font-size: 14px;
  transition: all 0.15s;
}

.search-input:focus {
  outline: none;
  border-color: var(--border-focus);
  box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
}

.clear-search-btn {
  position: absolute;
  right: 10px;
  top: 50%;
  transform: translateY(-50%);
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
}
.clear-search-btn:hover {
  color: var(--text-primary);
}

.status-tabs {
  display: flex;
  background: var(--bg-input);
  padding: 3px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
}

.status-tab {
  padding: 6px 12px;
  border: none;
  background: none;
  color: var(--text-secondary);
  font-size: 13px;
  font-weight: 500;
  border-radius: var(--radius-sm);
  cursor: pointer;
  transition: all 0.15s;
}

.status-tab.active {
  background: var(--bg-card);
  color: var(--text-primary);
  box-shadow: var(--shadow-sm);
  font-weight: 600;
}

.secondary-row {
  padding-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.filter-item {
  display: flex;
  align-items: center;
  gap: 8px;
}

.filter-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.03em;
}

.filter-select {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 7px 12px;
  color: var(--text-primary);
  font-size: 13px;
  cursor: pointer;
}

.filter-select:focus {
  outline: none;
  border-color: var(--border-focus);
}

.select-compact {
  padding: 7px 8px;
}

.reset-btn {
  margin-left: auto;
  color: #f87171;
}
.reset-btn:hover {
  background: var(--danger-subtle);
}

@media (max-width: 768px) {
  .primary-row {
    flex-direction: column;
    align-items: stretch;
  }
  .status-tabs {
    overflow-x: auto;
  }
  .secondary-row {
    gap: 8px;
  }
  .reset-btn {
    margin-left: 0;
    width: 100%;
  }
}
</style>
