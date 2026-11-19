<template>
  <div class="app-layout">
    <!-- Header Navigation -->
    <HeaderBar
      :healthStatus="healthStatus"
      :loading="loading || generatingBulk"
      @open-create="openCreateModal"
      @open-bulk="openBulkModal"
    />

    <!-- Main Content Container -->
    <main class="main-content">
      <div class="content-wrapper">
        <!-- Dashboard Statistics Overview -->
        <StatsOverview
          :totalItems="stats.total"
          :pendingCount="stats.pending"
          :progressCount="stats.progress"
          :doneCount="stats.done"
          :currentStatus="filters.status"
          @filter-status="quickFilterStatus"
        />

        <!-- Error State Banner if API connection fails -->
        <div v-if="apiError" class="api-error-banner" role="alert">
          <AlertCircle :size="20" class="api-error-icon" />
          <div class="api-error-content">
            <h4 class="api-error-title">{{ apiError.code }}: {{ apiError.message }}</h4>
            <p class="api-error-hint">Pastikan backend FastAPI sedang berjalan di port 8000.</p>
          </div>
          <button class="btn btn-secondary btn-sm" @click="loadData">
            <RefreshCw :size="14" />
            <span>Coba Lagi</span>
          </button>
        </div>

        <!-- Filter & Sorting Toolbar -->
        <FilterSortBar
          :currentStatus="filters.status"
          :currentPriority="filters.priority"
          :currentQ="filters.q"
          :currentSortBy="filters.sortBy"
          :currentSortOrder="filters.sortOrder"
          :currentPageSize="filters.pageSize"
          @update:status="val => updateFilter('status', val)"
          @update:priority="val => updateFilter('priority', val)"
          @update:q="val => updateFilter('q', val)"
          @update:sortBy="val => updateFilter('sortBy', val)"
          @update:sortOrder="val => updateFilter('sortOrder', val)"
          @update:pageSize="val => updateFilter('pageSize', val)"
          @reset-filters="resetFilters"
        />

        <!-- Todo List Table & Pagination -->
        <TodoTable
          :todos="todos"
          :meta="meta"
          :loading="loading"
          :hasFilters="hasActiveFilters"
          @view-detail="openDetailModal"
          @edit-todo="openEditModal"
          @delete-todo="openDeleteModal"
          @cycle-status="handleCycleStatus"
          @open-create="openCreateModal"
          @reset-filters="resetFilters"
          @page-change="handlePageChange"
          @copy-success="msg => addToast('Salin Berhasil', msg, 'info')"
        />
      </div>
    </main>

    <!-- Modals -->
    <TodoModal
      v-if="isTodoModalOpen"
      :todo="selectedTodo"
      :submitting="submittingTodo"
      :serverError="todoServerError"
      @close="closeTodoModal"
      @submit="handleSaveTodo"
    />

    <DetailModal
      v-if="isDetailModalOpen && selectedTodo"
      :todo="selectedTodo"
      @close="isDetailModalOpen = false"
      @edit="todo => { isDetailModalOpen = false; openEditModal(todo); }"
      @delete="todo => { isDetailModalOpen = false; openDeleteModal(todo); }"
      @copy-success="msg => addToast('Salin Berhasil', msg, 'info')"
    />

    <DeleteConfirmModal
      v-if="isDeleteModalOpen && selectedTodo"
      :todo="selectedTodo"
      :deleting="deletingTodo"
      @close="isDeleteModalOpen = false"
      @confirm="handleConfirmDelete"
    />

    <BulkModal
      v-if="isBulkModalOpen"
      :generating="generatingBulk"
      @close="isBulkModalOpen = false"
      @confirm="handleConfirmBulk"
    />

    <!-- Toast Notifications -->
    <ToastNotification
      :toasts="toasts"
      @dismiss="removeToast"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, onUnmounted } from 'vue'
import { AlertCircle, RefreshCw } from 'lucide-vue-next'
import { api } from './api/client.js'

import HeaderBar from './components/HeaderBar.vue'
import StatsOverview from './components/StatsOverview.vue'
import FilterSortBar from './components/FilterSortBar.vue'
import TodoTable from './components/TodoTable.vue'
import TodoModal from './components/TodoModal.vue'
import DetailModal from './components/DetailModal.vue'
import DeleteConfirmModal from './components/DeleteConfirmModal.vue'
import BulkModal from './components/BulkModal.vue'
import ToastNotification from './components/ToastNotification.vue'

// State
const todos = ref([])
const meta = ref({
  page: 1,
  page_size: 20,
  total_items: 0,
  total_pages: 0
})
const loading = ref(false)
const apiError = ref(null)
const healthStatus = ref('healthy')

const stats = reactive({
  total: 0,
  pending: 0,
  progress: 0,
  done: 0
})

const filters = reactive({
  status: '',
  priority: '',
  q: '',
  sortBy: 'created_at',
  sortOrder: 'desc',
  page: 1,
  pageSize: 20
})

const hasActiveFilters = computed(() => {
  return (
    filters.status !== '' ||
    filters.priority !== '' ||
    filters.q !== '' ||
    filters.sortBy !== 'created_at' ||
    filters.sortOrder !== 'desc' ||
    filters.pageSize !== 20
  )
})

// Modals state
const isTodoModalOpen = ref(false)
const selectedTodo = ref(null)
const submittingTodo = ref(false)
const todoServerError = ref(null)

const isDetailModalOpen = ref(false)
const isDeleteModalOpen = ref(false)
const deletingTodo = ref(false)

const isBulkModalOpen = ref(false)
const generatingBulk = ref(false)

// Toast System
const toasts = ref([])
let toastIdCounter = 0

const addToast = (title, message = '', type = 'success', duration = 3500) => {
  const id = ++toastIdCounter
  toasts.value.push({ id, title, message, type })
  if (duration > 0) {
    setTimeout(() => {
      removeToast(id)
    }, duration)
  }
}

const removeToast = (id) => {
  toasts.value = toasts.value.filter(t => t.id !== id)
}

// Data Fetching
const loadData = async () => {
  loading.value = true
  apiError.value = null

  try {
    const params = {
      page: filters.page,
      page_size: filters.pageSize,
      sort_by: filters.sortBy,
      sort_order: filters.sortOrder
    }
    if (filters.status) params.status = filters.status
    if (filters.priority) params.priority = filters.priority
    if (filters.q) params.q = filters.q

    const res = await api.getTodos(params)
    todos.value = res.data || []
    meta.value = res.meta || { page: 1, page_size: filters.pageSize, total_items: 0, total_pages: 0 }
    stats.total = meta.value.total_items

    // Update count stats
    updateCounts()
  } catch (err) {
    console.error('Failed to load todos:', err)
    apiError.value = err
  } finally {
    loading.value = false
  }
}

const updateCounts = async () => {
  try {
    // Quick parallel count queries
    const [pRes, progRes, dRes] = await Promise.all([
      api.getTodos({ status: 'pending', page: 1, page_size: 1 }),
      api.getTodos({ status: 'progress', page: 1, page_size: 1 }),
      api.getTodos({ status: 'done', page: 1, page_size: 1 })
    ])
    stats.pending = pRes.meta.total_items
    stats.progress = progRes.meta.total_items
    stats.done = dRes.meta.total_items
  } catch {
    // Silently continue if stats probe fails
  }
}

const checkHealth = async () => {
  try {
    const res = await api.getHealth()
    healthStatus.value = res.status === 'healthy' ? 'healthy' : 'degraded'
  } catch {
    healthStatus.value = 'degraded'
  }
}

// Filters & Pagination Handlers
const updateFilter = (key, val) => {
  filters[key] = val
  // Per SRS BR-010 & Section 10.3: reset page to 1 whenever filter or sort changes
  if (key !== 'page') {
    filters.page = 1
  }
  loadData()
}

const quickFilterStatus = (statusVal) => {
  filters.status = filters.status === statusVal ? '' : statusVal
  filters.page = 1
  loadData()
}

const resetFilters = () => {
  filters.status = ''
  filters.priority = ''
  filters.q = ''
  filters.sortBy = 'created_at'
  filters.sortOrder = 'desc'
  filters.page = 1
  filters.pageSize = 20
  loadData()
}

const handlePageChange = (newPage) => {
  filters.page = newPage
  loadData()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

// Modal Handlers
const openCreateModal = () => {
  selectedTodo.value = null
  todoServerError.value = null
  isTodoModalOpen.value = true
}

const openEditModal = (todo) => {
  selectedTodo.value = { ...todo }
  todoServerError.value = null
  isTodoModalOpen.value = true
}

const closeTodoModal = () => {
  isTodoModalOpen.value = false
  selectedTodo.value = null
  todoServerError.value = null
}

const openDetailModal = (todo) => {
  selectedTodo.value = todo
  isDetailModalOpen.value = true
}

const openDeleteModal = (todo) => {
  selectedTodo.value = todo
  isDeleteModalOpen.value = true
}

const openBulkModal = () => {
  isBulkModalOpen.value = true
}

// Action Handlers
const handleSaveTodo = async (formData) => {
  submittingTodo.value = true
  todoServerError.value = null

  try {
    if (selectedTodo.value && selectedTodo.value.id) {
      // PATCH update
      await api.updateTodo(selectedTodo.value.id, formData)
      addToast('Todo Diperbarui', `Todo "${formData.title}" berhasil diubah.`, 'success')
    } else {
      // POST create
      await api.createTodo(formData)
      addToast('Todo Dibuat', `Todo "${formData.title}" berhasil disimpan dengan UUID v7.`, 'success')
    }
    closeTodoModal()
    loadData()
  } catch (err) {
    todoServerError.value = err
  } finally {
    submittingTodo.value = false
  }
}

const handleCycleStatus = async ({ id, status }) => {
  try {
    await api.updateTodo(id, { status })
    addToast('Status Diperbarui', `Status todo diubah menjadi ${status}.`, 'info', 2000)
    loadData()
  } catch (err) {
    addToast('Gagal Mengubah Status', err.message, 'error')
  }
}

const handleConfirmDelete = async (id) => {
  deletingTodo.value = true
  try {
    await api.deleteTodo(id)
    addToast('Todo Dihapus', 'Item todo telah dihapus dari database.', 'success')
    isDeleteModalOpen.value = false
    selectedTodo.value = null
    loadData()
  } catch (err) {
    addToast('Gagal Menghapus Todo', err.message, 'error')
  } finally {
    deletingTodo.value = false
  }
}

const handleConfirmBulk = async (count) => {
  generatingBulk.value = true
  try {
    const res = await api.bulkRandom(count)
    addToast(
      'Bulk Todo Berhasil Dibuat!',
      `${res.data.created_count.toLocaleString('id-ID')} data acak baru tersimpan secara atomik.`,
      'success',
      5000
    )
    isBulkModalOpen.value = false
    filters.page = 1
    loadData()
  } catch (err) {
    addToast('Gagal Menghasilkan Bulk Todo', err.message, 'error')
  } finally {
    generatingBulk.value = false
  }
}

const handleKeyDown = (e) => {
  const isInput = ['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)
  if (e.key === 'Escape') {
    isTodoModalOpen.value = false
    isDetailModalOpen.value = false
    isDeleteModalOpen.value = false
    isBulkModalOpen.value = false
    return
  }

  if (isInput) return

  if ((e.key === 'n' || e.key === 'N') && !isAnyModalOpen()) {
    e.preventDefault()
    openCreateModal()
  } else if ((e.key === 'b' || e.key === 'B') && !isAnyModalOpen()) {
    e.preventDefault()
    openBulkModal()
  }
}

const isAnyModalOpen = () => {
  return isTodoModalOpen.value || isDetailModalOpen.value || isDeleteModalOpen.value || isBulkModalOpen.value
}

onMounted(() => {
  checkHealth()
  loadData()
  window.addEventListener('keydown', handleKeyDown)
  // Periodic health ping
  const timer = setInterval(checkHealth, 30000)
  onUnmounted(() => {
    window.removeEventListener('keydown', handleKeyDown)
    clearInterval(timer)
  })
})
</script>

<style scoped>
.app-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 28px 20px 48px 20px;
}

.content-wrapper {
  max-width: var(--max-w);
  margin: 0 auto;
}

.api-error-banner {
  background: var(--danger-subtle);
  border: 1px solid rgba(239, 68, 68, 0.35);
  border-radius: var(--radius-lg);
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  margin-bottom: 24px;
}

.api-error-icon {
  color: var(--danger);
  flex-shrink: 0;
}

.api-error-content {
  flex: 1;
}

.api-error-title {
  font-size: 14px;
  font-weight: 700;
  color: #fca5a5;
}

.api-error-hint {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 2px;
}
</style>
