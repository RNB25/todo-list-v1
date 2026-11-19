<template>
  <div class="table-container">
    <!-- Loading State Skeleton -->
    <div v-if="loading" class="skeleton-wrapper" aria-label="Memuat data todo...">
      <div v-for="i in 5" :key="i" class="skeleton-row">
        <div class="skeleton-box skeleton-title"></div>
        <div class="skeleton-box skeleton-badge"></div>
        <div class="skeleton-box skeleton-badge"></div>
        <div class="skeleton-box skeleton-date"></div>
        <div class="skeleton-box skeleton-actions"></div>
      </div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!todos || todos.length === 0" class="empty-state">
      <div class="empty-icon-wrap">
        <Inbox :size="36" />
      </div>
      <h3 class="empty-title">Tidak ada todo ditemukan</h3>
      <p class="empty-desc">
        {{ hasFilters ? 'Coba ubah kata kunci atau setel ulang filter pencarian Anda.' : 'Belum ada item todo tersimpan. Klik tombol di bawah untuk membuat todo pertama Anda!' }}
      </p>
      <div class="empty-actions">
        <button v-if="hasFilters" class="btn btn-secondary btn-sm" @click="$emit('reset-filters')">
          Reset Filter
        </button>
        <button class="btn btn-primary btn-sm" @click="$emit('open-create')">
          <Plus :size="15" />
          <span>Tambah Todo Baru</span>
        </button>
      </div>
    </div>

    <!-- Table with Data -->
    <div v-else class="table-responsive">
      <table class="data-table">
        <thead>
          <tr>
            <th class="th-title">Judul & Deskripsi</th>
            <th class="th-status">Status</th>
            <th class="th-priority">Prioritas</th>
            <th class="th-uuid">UUID v7</th>
            <th class="th-date">Waktu Dibuat</th>
            <th class="th-actions">Aksi</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="todo in todos" :key="todo.id" class="table-row">
            <!-- Title & Description -->
            <td class="td-title">
              <div class="title-cell" @click="$emit('view-detail', todo)">
                <div class="todo-title" :class="{ 'title-done': todo.status === 'done' }">
                  {{ todo.title }}
                </div>
                <div v-if="todo.description" class="todo-desc">
                  {{ truncate(todo.description, 75) }}
                </div>
              </div>
            </td>

            <!-- Status Badge with quick dropdown/click -->
            <td class="td-status">
              <button
                class="badge badge-btn"
                :class="`badge-${todo.status}`"
                @click="cycleStatus(todo)"
                title="Klik untuk mengubah status dengan cepat"
              >
                <Clock v-if="todo.status === 'pending'" :size="12" />
                <Activity v-else-if="todo.status === 'progress'" :size="12" />
                <CheckCircle2 v-else :size="12" />
                <span>{{ todo.status }}</span>
              </button>
            </td>

            <!-- Priority Badge -->
            <td class="td-priority">
              <span class="badge" :class="`badge-${todo.priority}`">
                <span class="priority-dot"></span>
                <span>{{ todo.priority }}</span>
              </span>
            </td>

            <!-- UUID v7 -->
            <td class="td-uuid">
              <button
                class="uuid-pill"
                @click="copyUuid(todo.id)"
                :title="`Klik untuk menyalin UUID: ${todo.id}`"
              >
                {{ todo.id.substring(0, 8) }}...{{ todo.id.substring(todo.id.length - 4) }}
                <Copy :size="10" class="copy-icon" />
              </button>
            </td>

            <!-- Date -->
            <td class="td-date">
              <div class="date-main">{{ formatDate(todo.created_at) }}</div>
              <div class="date-sub">{{ formatRelative(todo.created_at) }}</div>
            </td>

            <!-- Action buttons -->
            <td class="td-actions">
              <div class="action-btn-group">
                <button
                  class="btn btn-secondary btn-icon"
                  @click="$emit('view-detail', todo)"
                  title="Lihat Detail"
                >
                  <Eye :size="14" />
                </button>
                <button
                  class="btn btn-secondary btn-icon"
                  @click="$emit('edit-todo', todo)"
                  title="Edit Todo"
                >
                  <Edit3 :size="14" />
                </button>
                <button
                  class="btn btn-danger btn-icon"
                  @click="$emit('delete-todo', todo)"
                  title="Hapus Todo"
                >
                  <Trash2 :size="14" />
                </button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Pagination Footer -->
    <div v-if="meta && meta.total_items > 0" class="pagination-footer">
      <div class="pagination-info">
        Menampilkan <strong>{{ rangeStart }}</strong> - <strong>{{ rangeEnd }}</strong> dari <strong>{{ meta.total_items.toLocaleString('id-ID') }}</strong> todo
      </div>

      <div class="pagination-nav">
        <!-- First Page -->
        <button
          class="btn btn-secondary btn-sm"
          :disabled="meta.page <= 1"
          @click="$emit('page-change', 1)"
          title="Halaman Pertama"
        >
          <ChevronsLeft :size="15" />
        </button>

        <!-- Prev Page -->
        <button
          class="btn btn-secondary btn-sm"
          :disabled="meta.page <= 1"
          @click="$emit('page-change', meta.page - 1)"
          title="Halaman Sebelumnya"
        >
          <ChevronLeft :size="15" />
        </button>

        <!-- Page Indicator Pill -->
        <div class="page-current-pill">
          Halaman <span>{{ meta.page }}</span> dari <span>{{ meta.total_pages || 1 }}</span>
        </div>

        <!-- Next Page -->
        <button
          class="btn btn-secondary btn-sm"
          :disabled="meta.page >= meta.total_pages"
          @click="$emit('page-change', meta.page + 1)"
          title="Halaman Berikutnya"
        >
          <ChevronRight :size="15" />
        </button>

        <!-- Last Page -->
        <button
          class="btn btn-secondary btn-sm"
          :disabled="meta.page >= meta.total_pages"
          @click="$emit('page-change', meta.total_pages)"
          title="Halaman Terakhir"
        >
          <ChevronsRight :size="15" />
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import {
  Inbox,
  Plus,
  Clock,
  Activity,
  CheckCircle2,
  Copy,
  Eye,
  Edit3,
  Trash2,
  ChevronLeft,
  ChevronRight,
  ChevronsLeft,
  ChevronsRight
} from 'lucide-vue-next'

const props = defineProps({
  todos: { type: Array, default: () => [] },
  meta: { type: Object, default: () => ({ page: 1, page_size: 20, total_items: 0, total_pages: 0 }) },
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

const rangeStart = computed(() => {
  if (!props.meta.total_items) return 0
  return (props.meta.page - 1) * props.meta.page_size + 1
})

const rangeEnd = computed(() => {
  if (!props.meta.total_items) return 0
  return Math.min(props.meta.page * props.meta.page_size, props.meta.total_items)
})

const truncate = (str, len) => {
  if (!str) return ''
  return str.length > len ? str.substring(0, len) + '...' : str
}

const formatDate = (isoStr) => {
  if (!isoStr) return '-'
  try {
    const d = new Date(isoStr)
    return d.toLocaleDateString('id-ID', {
      day: 'numeric',
      month: 'short',
      year: 'numeric'
    })
  } catch {
    return isoStr
  }
}

const formatRelative = (isoStr) => {
  if (!isoStr) return ''
  try {
    const d = new Date(isoStr)
    return d.toLocaleTimeString('id-ID', {
      hour: '2-digit',
      minute: '2-digit'
    })
  } catch {
    return ''
  }
}

const copyUuid = async (uuid) => {
  try {
    await navigator.clipboard.writeText(uuid)
    emit('copy-success', 'UUID v7 berhasil disalin ke clipboard!')
  } catch {
    // fallback
  }
}

const cycleStatus = (todo) => {
  const nextMap = {
    pending: 'progress',
    progress: 'done',
    done: 'pending'
  }
  const nextStatus = nextMap[todo.status] || 'pending'
  emit('cycle-status', { id: todo.id, status: nextStatus })
}
</script>

<style scoped>
.table-container {
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
}

.table-responsive {
  width: 100%;
  overflow-x: auto;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 14px;
}

.data-table thead {
  background: #0f1523;
  border-bottom: 1px solid var(--border-subtle);
}

.data-table th {
  padding: 14px 18px;
  font-size: 12px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--text-muted);
}

.table-row {
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  transition: background-color 0.15s ease;
}

.table-row:hover {
  background-color: var(--bg-card-hover);
}

.data-table td {
  padding: 14px 18px;
  vertical-align: middle;
}

.title-cell {
  cursor: pointer;
}

.todo-title {
  font-weight: 600;
  color: var(--text-primary);
  line-height: 1.4;
}

.title-done {
  text-decoration: line-through;
  color: var(--text-muted);
}

.todo-desc {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 3px;
}

.badge-btn {
  cursor: pointer;
  transition: all 0.15s;
  border: 1px solid transparent;
}
.badge-btn:hover {
  transform: scale(1.04);
}

.priority-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: currentColor;
}

.copy-icon {
  margin-left: 4px;
  opacity: 0.6;
}

.date-main {
  font-size: 13px;
  color: var(--text-primary);
  font-weight: 500;
}

.date-sub {
  font-size: 11px;
  color: var(--text-muted);
}

.action-btn-group {
  display: flex;
  align-items: center;
  gap: 6px;
}

/* Skeleton Loading */
.skeleton-wrapper {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.skeleton-row {
  display: flex;
  align-items: center;
  gap: 16px;
}

.skeleton-box {
  background: linear-gradient(90deg, #182235 25%, #222f47 50%, #182235 75%);
  background-size: 200% 100%;
  animation: skeletonPulse 1.5s infinite;
  border-radius: var(--radius-sm);
  height: 24px;
}

.skeleton-title { flex: 2; height: 32px; }
.skeleton-badge { width: 80px; }
.skeleton-date { width: 100px; }
.skeleton-actions { width: 90px; }

@keyframes skeletonPulse {
  0% { background-position: 200% 0; }
  100% { background-position: -200% 0; }
}

/* Empty State */
.empty-state {
  padding: 60px 24px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}

.empty-icon-wrap {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: rgba(148, 163, 184, 0.1);
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 16px;
}

.empty-title {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 6px;
}

.empty-desc {
  font-size: 14px;
  color: var(--text-secondary);
  max-width: 420px;
  margin-bottom: 20px;
}

.empty-actions {
  display: flex;
  gap: 12px;
}

/* Pagination Footer */
.pagination-footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 20px;
  background: #0f1523;
  border-top: 1px solid var(--border-subtle);
  flex-wrap: wrap;
  gap: 12px;
}

.pagination-info {
  font-size: 13px;
  color: var(--text-muted);
}

.pagination-info strong {
  color: var(--text-primary);
}

.pagination-nav {
  display: flex;
  align-items: center;
  gap: 6px;
}

.page-current-pill {
  font-size: 13px;
  font-weight: 600;
  padding: 6px 12px;
  background: var(--bg-card);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  color: var(--text-secondary);
}
.page-current-pill span {
  color: var(--text-primary);
}
</style>
