<template>
  <div class="table-container">
    <!-- Skeleton Loading -->
    <div v-if="loading" class="skeleton-wrapper" aria-label="Memuat data...">
      <div v-for="i in 6" :key="i" class="skeleton-row">
        <div class="skeleton-cell cell-checkbox"></div>
        <div class="skeleton-cell cell-title"></div>
        <div class="skeleton-cell cell-badge"></div>
        <div class="skeleton-cell cell-badge"></div>
        <div class="skeleton-cell cell-uuid"></div>
        <div class="skeleton-cell cell-date"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!todos || todos.length === 0" class="empty-state">
      <div class="empty-icon-wrap">
        <Inbox :size="28" />
      </div>
      <h3 class="empty-title">Tidak ada todo yang cocok</h3>
      <p class="empty-desc">
        {{ hasFilters ? 'Filter pencarian Anda tidak menghasilkan data apapun.' : 'Belum ada data todo di database MySQL. Buat todo pertama Anda atau gunakan tombol Generate Data!' }}
      </p>
      <div class="empty-actions">
        <button v-if="hasFilters" class="btn btn-secondary btn-sm" @click="$emit('reset-filters')">
          Reset Filter
        </button>
        <button class="btn btn-primary btn-sm" @click="$emit('open-create')">
          <Plus :size="14" />
          <span>Tambah Todo Baru</span>
        </button>
      </div>
    </div>

    <!-- Data Table -->
    <div v-else class="table-responsive">
      <table class="data-table">
        <thead>
          <tr>
            <th class="th-status" style="width: 140px;">Status</th>
            <th class="th-title">Judul & Deskripsi</th>
            <th class="th-priority" style="width: 110px;">Prioritas</th>
            <th class="th-uuid" style="width: 130px;">UUID v7</th>
            <th class="th-date" style="width: 140px;">Waktu Dibuat</th>
            <th class="th-actions" style="width: 100px;">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr 
            v-for="todo in todos" 
            :key="todo.id" 
            class="table-row"
            :class="{ 'row-done': todo.status === 'done' }"
          >
            <!-- Status Column with 1-click toggle -->
            <td class="td-status">
              <button
                class="status-toggle-pill"
                :class="`status-${todo.status}`"
                @click="cycleStatus(todo)"
                title="Klik untuk mengubah status (Pending → Progress → Done)"
              >
                <span class="status-indicator-dot"></span>
                <span class="status-text">{{ todo.status }}</span>
              </button>
            </td>

            <!-- Title & Description Column -->
            <td class="td-title" @click="$emit('view-detail', todo)">
              <div class="title-cell-wrap">
                <span class="todo-title" :class="{ 'title-done': todo.status === 'done' }">
                  {{ todo.title }}
                </span>
                <span v-if="todo.description" class="todo-desc">
                  {{ truncate(todo.description, 80) }}
                </span>
              </div>
            </td>

            <!-- Priority Column -->
            <td class="td-priority">
              <div class="priority-chip" :class="`priority-${todo.priority}`">
                <span class="priority-bars" aria-hidden="true">
                  <span class="bar bar-1"></span>
                  <span class="bar bar-2" :class="{ active: todo.priority === 'medium' || todo.priority === 'high' }"></span>
                  <span class="bar bar-3" :class="{ active: todo.priority === 'high' }"></span>
                </span>
                <span class="priority-text">{{ todo.priority }}</span>
              </div>
            </td>

            <!-- UUID v7 Column -->
            <td class="td-uuid">
              <button
                class="uuid-pill"
                @click="copyUuid(todo.id)"
                :title="`Klik untuk menyalin UUID: ${todo.id}`"
              >
                <span>{{ todo.id.substring(0, 8) }}</span>
                <Check v-if="copiedId === todo.id" :size="11" class="copy-success-icon" />
                <Copy v-else :size="11" class="copy-icon" />
              </button>
            </td>

            <!-- Date Column -->
            <td class="td-date" :title="`ISO: ${todo.created_at}`">
              <div class="date-main">{{ formatDate(todo.created_at) }}</div>
              <div class="date-sub">{{ formatRelative(todo.created_at) }}</div>
            </td>

            <!-- Actions Column -->
            <td class="td-actions">
              <div class="action-buttons-group">
                <button
                  class="action-btn"
                  @click="$emit('view-detail', todo)"
                  title="Lihat Detail Todo"
                >
                  <Eye :size="13" />
                </button>
                <button
                  class="action-btn"
                  @click="$emit('edit-todo', todo)"
                  title="Edit Todo"
                >
                  <Pencil :size="13" />
                </button>
                <button
                  class="action-btn btn-action-delete"
                  @click="$emit('delete-todo', todo)"
                  title="Hapus Todo"
                >
                  <Trash2 :size="13" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Footer -->
    <div v-if="todos && todos.length > 0" class="pagination-footer">
      <div class="pagination-info">
        Menampilkan 
        <span class="info-highlight">{{ rangeStart }} - {{ rangeEnd }}</span> 
        dari 
        <span class="info-highlight">{{ (meta.total_items ?? 0).toLocaleString('id-ID') }}</span> 
        todo
      </div>

      <div class="pagination-controls">
        <button
          class="btn btn-secondary btn-sm"
          :disabled="meta.page <= 1"
          @click="goToPage(meta.page - 1)"
        >
          <ChevronLeft :size="14" />
          <span>Sebelumnya</span>
        </button>

        <span class="page-current">
          Hal <span class="page-num">{{ meta.page }}</span> / {{ meta.total_pages || 1 }}
        </span>

        <button
          class="btn btn-secondary btn-sm"
          :disabled="meta.page >= meta.total_pages"
          @click="goToPage(meta.page + 1)"
        >
          <span>Berikutnya</span>
          <ChevronRight :size="14" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  Inbox,
  Plus,
  Eye,
  Pencil,
  Trash2,
  Copy,
  Check,
  ChevronLeft,
  ChevronRight
} from 'lucide-vue-next'

const props = defineProps({
  todos: { type: Array, default: () => [] },
  meta: {
    type: Object,
    default: () => ({ page: 1, page_size: 20, total: 0, total_pages: 1 })
  },
  loading: { type: Boolean, default: false },
  hasFilters: { type: Boolean, default: false }
})

const emit = defineEmits([
  'view-detail',
  'edit-todo',
  'delete-todo',
  'cycle-status',
  'open-create',
  'reset-filters',
  'page-change',
  'copy-success'
])

const copiedId = ref(null)

const rangeStart = computed(() => {
  if (props.meta.total_items === 0) return 0
  return (props.meta.page - 1) * props.meta.page_size + 1
})

const rangeEnd = computed(() => {
  return Math.min(props.meta.page * props.meta.page_size, props.meta.total_items)
})

function cycleStatus(todo) {
  const map = {
    pending: 'progress',
    progress: 'done',
    done: 'pending'
  }
  const nextStatus = map[todo.status] || 'pending'
  emit('cycle-status', { id: todo.id, status: nextStatus })
}

function copyUuid(id) {
  navigator.clipboard.writeText(id).then(() => {
    copiedId.value = id
    emit('copy-success', `UUID tersalin: ${id}`)
    setTimeout(() => {
      if (copiedId.value === id) {
        copiedId.value = null
      }
    }, 2000)
  })
}

function truncate(str, maxLen) {
  if (!str) return ''
  return str.length > maxLen ? str.substring(0, maxLen) + '...' : str
}

function formatDate(dateStr) {
  if (!dateStr) return '-'
  try {
    const d = new Date(dateStr)
    return d.toLocaleDateString('id-ID', {
      day: '2-digit',
      month: 'short',
      year: 'numeric'
    })
  } catch {
    return dateStr
  }
}

function formatRelative(dateStr) {
  if (!dateStr) return ''
  try {
    const d = new Date(dateStr)
    const diffSec = Math.floor((new Date() - d) / 1000)
    if (diffSec < 60) return 'Baru saja'
    if (diffSec < 3600) return `${Math.floor(diffSec / 60)} mnt lalu`
    if (diffSec < 86400) return `${Math.floor(diffSec / 3600)} jam lalu`
    const diffDays = Math.floor(diffSec / 86400)
    return `${diffDays} hari lalu`
  } catch {
    return ''
  }
}

function goToPage(p) {
  if (p >= 1 && p <= props.meta.total_pages) {
    emit('page-change', p)
  }
}
</script>

<style scoped>
.table-container {
  background: var(--bg-surface);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-card);
}

.table-responsive {
  width: 100%;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 13px;
  text-align: left;
}

.data-table thead {
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid var(--border-subtle);
}

.data-table th {
  padding: 10px 14px;
  font-size: 11px;
  font-weight: 600;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  user-select: none;
}

.table-row {
  border-bottom: 1px solid var(--border-subtle);
  transition: background 0.1s ease;
}

.table-row:hover {
  background: rgba(255, 255, 255, 0.025);
}

.table-row:last-child {
  border-bottom: none;
}

.data-table td {
  padding: 12px 14px;
  vertical-align: middle;
}

/* Status Pill */
.status-toggle-pill {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 8px;
  border-radius: var(--radius-full);
  font-size: 11px;
  font-weight: 500;
  font-family: var(--font-mono);
  background: transparent;
  border: 1px solid transparent;
  cursor: pointer;
  transition: all 0.12s ease;
  user-select: none;
}

.status-toggle-pill:hover {
  transform: translateY(-1px);
}

.status-indicator-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
}

.status-pending {
  background: var(--status-pending-bg);
  border-color: var(--status-pending-border);
  color: #cbd5e1;
}
.status-pending .status-indicator-dot { background-color: var(--status-pending); }

.status-progress {
  background: var(--status-progress-bg);
  border-color: var(--status-progress-border);
  color: #fde68a;
}
.status-progress .status-indicator-dot { 
  background-color: var(--status-progress);
  box-shadow: 0 0 6px rgba(245, 158, 11, 0.5);
}

.status-done {
  background: var(--status-done-bg);
  border-color: var(--status-done-border);
  color: #a7f3d0;
}
.status-done .status-indicator-dot { background-color: var(--status-done); }

/* Title Cell */
.title-cell-wrap {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.todo-title {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.35;
  transition: color 0.12s;
}

.title-cell-wrap:hover .todo-title {
  color: #ffffff;
  text-decoration: underline;
}

.title-done {
  text-decoration: line-through;
  color: var(--text-muted) !important;
}

.todo-desc {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.3;
}

/* Priority Chip with Signal Bars */
.priority-chip {
  display: inline-flex;
  align-items: center;
  gap: 5px;
  font-family: var(--font-mono);
  font-size: 11px;
  text-transform: uppercase;
}

.priority-bars {
  display: inline-flex;
  align-items: flex-end;
  gap: 1.5px;
  height: 10px;
}

.priority-bars .bar {
  width: 2.5px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 1px;
}
.bar-1 { height: 4px; }
.bar-2 { height: 7px; }
.bar-3 { height: 10px; }

.priority-low { color: #38bdf8; }
.priority-low .bar-1 { background: #38bdf8; }

.priority-medium { color: #fbbf24; }
.priority-medium .bar-1, .priority-medium .bar-2.active { background: #fbbf24; }

.priority-high { color: #f43f5e; }
.priority-high .bar-1, .priority-high .bar-2.active, .priority-high .bar-3.active { background: #f43f5e; }

/* UUID Pill */
.copy-icon {
  color: var(--text-muted);
}
.copy-success-icon {
  color: #10b981;
}

/* Date */
.date-main {
  font-size: 12px;
  color: var(--text-secondary);
}
.date-sub {
  font-size: 10px;
  color: var(--text-muted);
}

/* Action Buttons */
.action-buttons-group {
  display: flex;
  align-items: center;
  gap: 4px;
}

.action-btn {
  background: transparent;
  border: 1px solid transparent;
  color: var(--text-muted);
  padding: 5px;
  border-radius: var(--radius-xs);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.12s;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
  border-color: var(--border-subtle);
}

.btn-action-delete:hover {
  background: rgba(244, 63, 94, 0.15);
  color: #fb7185;
  border-color: rgba(244, 63, 94, 0.3);
}

/* Pagination Footer */
.pagination-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 18px;
  border-top: 1px solid var(--border-subtle);
  background: rgba(255, 255, 255, 0.015);
  flex-wrap: wrap;
  gap: 12px;
}

.pagination-info {
  font-size: 12px;
  color: var(--text-muted);
}

.info-highlight {
  font-family: var(--font-mono);
  color: var(--text-primary);
  font-weight: 600;
}

.pagination-controls {
  display: flex;
  align-items: center;
  gap: 10px;
}

.page-current {
  font-size: 12px;
  color: var(--text-muted);
}

.page-num {
  font-family: var(--font-mono);
  color: #ffffff;
  font-weight: 600;
}

/* Empty State */
.empty-state {
  padding: 48px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.empty-icon-wrap {
  width: 48px;
  height: 48px;
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 14px;
}

.empty-title {
  font-size: 15px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 6px;
}

.empty-desc {
  font-size: 13px;
  color: var(--text-muted);
  max-width: 420px;
  margin-bottom: 18px;
  line-height: 1.45;
}

.empty-actions {
  display: flex;
  gap: 8px;
}

/* Skeleton Loading */
.skeleton-wrapper {
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton-row {
  display: flex;
  align-items: center;
  gap: 16px;
  height: 42px;
}

.skeleton-cell {
  background: rgba(255, 255, 255, 0.04);
  border-radius: var(--radius-xs);
  height: 14px;
  animation: pulse 1.5s infinite;
}

.cell-checkbox { width: 16px; height: 16px; }
.cell-title { flex: 1; height: 16px; }
.cell-badge { width: 70px; }
.cell-uuid { width: 90px; }
.cell-date { width: 100px; }

@keyframes pulse {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 0.7; }
}
</style>
