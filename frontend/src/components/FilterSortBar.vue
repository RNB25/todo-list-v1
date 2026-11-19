<template>
  <div class="toolbar-card">
    <div class="toolbar-primary">
      <!-- Search Input with Keyboard Shortcut -->
      <div class="search-field">
        <Search :size="15" class="search-icon" />
        <input
          ref="searchInput"
          type="text"
          v-model="localQ"
          placeholder="Cari judul atau deskripsi..."
          class="search-input"
          @keydown.enter="applySearch"
          aria-label="Cari todo"
        />
        <div class="search-extras">
          <button
            v-if="localQ"
            class="clear-btn"
            @click="clearSearch"
            title="Hapus pencarian"
          >
            <X :size="13" />
          </button>
          <kbd class="shortcut-hint" title="Tekan / untuk fokus pencarian">/</kbd>
        </div>
      </div>

      <!-- Segmented Status Switcher -->
      <div class="segmented-control" role="tablist">
        <button
          v-for="tab in statusTabs"
          :key="tab.value"
          class="segment-btn"
          :class="{ active: currentStatus === tab.value }"
          @click="selectStatus(tab.value)"
          role="tab"
          :aria-selected="currentStatus === tab.value"
        >
          {{ tab.label }}
        </button>
      </div>
    </div>

    <div class="toolbar-secondary">
      <div class="filter-controls-group">
        <!-- Priority Dropdown -->
        <div class="control-item">
          <label class="control-label" for="priority-select">Prioritas</label>
          <select
            id="priority-select"
            :value="currentPriority"
            @change="onPriorityChange($event.target.value)"
            class="styled-select"
          >
            <option value="">Semua Prioritas</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
          </select>
        </div>

        <!-- Sort By Dropdown -->
        <div class="control-item">
          <label class="control-label" for="sortby-select">Urutkan</label>
          <select
            id="sortby-select"
            :value="currentSortBy"
            @change="onSortByChange($event.target.value)"
            class="styled-select"
          >
            <option value="created_at">Waktu Dibuat</option>
            <option value="updated_at">Waktu Diperbarui</option>
            <option value="title">Judul (A-Z)</option>
            <option value="status">Status</option>
            <option value="priority">Prioritas</option>
          </select>
        </div>

        <!-- Sort Direction Toggle -->
        <button
          class="btn btn-secondary btn-sm sort-direction-btn"
          @click="toggleSortOrder"
          :title="`Arah urutan: ${currentSortOrder.toUpperCase()}`"
        >
          <ArrowDownNarrowWide v-if="currentSortOrder === 'desc'" :size="14" />
          <ArrowUpWideNarrow v-else :size="14" />
          <span>{{ currentSortOrder === 'desc' ? 'Desc' : 'Asc' }}</span>
        </button>

        <!-- Page Size Selector -->
        <div class="control-item">
          <label class="control-label" for="pagesize-select">Per Halaman</label>
          <select
            id="pagesize-select"
            :value="currentPageSize"
            @change="onPageSizeChange(Number($event.target.value))"
            class="styled-select select-narrow"
          >
            <option :value="10">10</option>
            <option :value="20">20</option>
            <option :value="50">50</option>
            <option :value="100">100</option>
          </select>
        </div>
      </div>

      <!-- Reset Filters Button if active -->
      <button
        v-if="hasActiveFilters"
        class="btn btn-sm btn-secondary reset-filter-btn"
        @click="$emit('reset-filters')"
      >
        <RotateCcw :size="12" />
        <span>Reset Filter</span>
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed, onMounted, onUnmounted } from 'vue'
import { Search, X, ArrowDownNarrowWide, ArrowUpWideNarrow, RotateCcw } from 'lucide-vue-next'

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
const searchInput = ref(null)

const statusTabs = [
  { label: 'Semua', value: '' },
  { label: 'Pending', value: 'pending' },
  { label: 'In Progress', value: 'progress' },
  { label: 'Done', value: 'done' }
]

watch(() => props.currentQ, (newVal) => {
  localQ.value = newVal
})

let debounceTimer = null
watch(localQ, (newVal) => {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(() => {
    emit('update:q', newVal.trim())
  }, 250)
})

function applySearch() {
  clearTimeout(debounceTimer)
  emit('update:q', localQ.value.trim())
}

function clearSearch() {
  localQ.value = ''
  emit('update:q', '')
  if (searchInput.value) {
    searchInput.value.focus()
  }
}

function selectStatus(statusVal) {
  emit('update:status', statusVal)
}

function onPriorityChange(val) {
  emit('update:priority', val)
}

function onSortByChange(val) {
  emit('update:sortBy', val)
}

function toggleSortOrder() {
  emit('update:sortOrder', props.currentSortOrder === 'desc' ? 'asc' : 'desc')
}

function onPageSizeChange(val) {
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

function handleGlobalKeydown(e) {
  if (e.key === '/' && document.activeElement !== searchInput.value && !['INPUT', 'TEXTAREA'].includes(document.activeElement.tagName)) {
    e.preventDefault()
    searchInput.value?.focus()
  }
}

onMounted(() => {
  window.addEventListener('keydown', handleGlobalKeydown)
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleGlobalKeydown)
})
</script>

<style scoped>
.toolbar-card {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  padding: 12px 16px;
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
  box-shadow: var(--shadow-card);
}

.toolbar-primary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
}

.search-field {
  position: relative;
  flex: 1;
  min-width: 260px;
  display: flex;
  align-items: center;
}

.search-icon {
  position: absolute;
  left: 12px;
  color: var(--text-muted);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 8px 64px 8px 34px;
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  color: var(--text-primary);
  font-size: 13px;
  transition: all 0.12s ease;
}

.search-input:focus {
  outline: none;
  border-color: var(--border-strong);
  box-shadow: 0 0 0 1px var(--border-strong);
}

.search-extras {
  position: absolute;
  right: 8px;
  display: flex;
  align-items: center;
  gap: 4px;
}

.clear-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 2px;
  display: flex;
  border-radius: 2px;
}

.clear-btn:hover {
  color: #ffffff;
}

.shortcut-hint {
  pointer-events: none;
}

/* Segmented Control */
.segmented-control {
  display: flex;
  align-items: center;
  background: var(--bg-input);
  padding: 3px;
  border-radius: var(--radius-sm);
  border: 1px solid var(--border-subtle);
}

.segment-btn {
  padding: 4px 12px;
  border: none;
  background: transparent;
  color: var(--text-muted);
  font-size: 12px;
  font-weight: 500;
  border-radius: var(--radius-xs);
  cursor: pointer;
  transition: all 0.12s ease;
  user-select: none;
}

.segment-btn:hover {
  color: var(--text-primary);
}

.segment-btn.active {
  background: rgba(255, 255, 255, 0.1);
  color: #ffffff;
  font-weight: 600;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.4);
}

/* Toolbar Secondary */
.toolbar-secondary {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  flex-wrap: wrap;
  padding-top: 10px;
  border-top: 1px solid var(--border-subtle);
}

.filter-controls-group {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.control-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.control-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}

.styled-select {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xs);
  color: var(--text-secondary);
  font-size: 12px;
  padding: 4px 8px;
  cursor: pointer;
  outline: none;
  transition: all 0.12s;
}

.styled-select:focus {
  border-color: var(--border-strong);
  color: #ffffff;
}

.select-narrow {
  width: 60px;
}

.sort-direction-btn {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
}

.reset-filter-btn {
  color: var(--text-muted);
  gap: 5px;
}

.reset-filter-btn:hover {
  color: #ffffff;
}
</style>
