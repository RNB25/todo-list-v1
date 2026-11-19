<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content" role="dialog" :aria-labelledby="isEdit ? 'edit-title' : 'create-title'">
      <div class="modal-header">
        <div class="modal-header-icon" :class="isEdit ? 'icon-edit' : 'icon-create'">
          <Edit3 v-if="isEdit" :size="20" />
          <Plus v-else :size="20" />
        </div>
        <div class="modal-header-text">
          <h2 :id="isEdit ? 'edit-title' : 'create-title'" class="modal-heading">
            {{ isEdit ? 'Edit Todo' : 'Tambah Todo Baru' }}
          </h2>
          <p class="modal-subheading">
            {{ isEdit ? 'Perbarui informasi todo yang tersimpan di sistem' : 'Tambahkan item pekerjaan baru dengan UUID v7 otomatis' }}
          </p>
        </div>
        <button class="modal-close-btn" @click="$emit('close')" aria-label="Tutup form">
          <X :size="18" />
        </button>
      </div>

      <!-- Server Error Alert -->
      <div v-if="serverError" class="modal-error-alert">
        <AlertTriangle :size="16" class="error-alert-icon" />
        <div>
          <div class="error-alert-title">{{ serverError.message || 'Validasi Gagal' }}</div>
          <ul v-if="serverError.details && serverError.details.length" class="error-detail-list">
            <li v-for="(d, idx) in serverError.details" :key="idx">
              <strong>{{ d.field }}:</strong> {{ d.reason }}
            </li>
          </ul>
        </div>
      </div>

      <form @submit.prevent="handleSubmit" class="modal-form">
        <!-- Title Input -->
        <div class="form-group">
          <div class="label-row">
            <label for="todo-title" class="form-label">
              Judul Todo <span class="required">*</span>
            </label>
            <span class="char-count" :class="{ 'char-warning': form.title.length > 240 }">
              {{ form.title.length }}/255
            </span>
          </div>
          <input
            id="todo-title"
            type="text"
            v-model="form.title"
            maxlength="255"
            placeholder="Contoh: Implementasi endpoint REST API dengan UUID v7"
            class="form-input"
            :class="{ 'input-error': clientErrors.title }"
            :disabled="submitting"
            required
            autofocus
          />
          <span v-if="clientErrors.title" class="field-error-msg">
            {{ clientErrors.title }}
          </span>
        </div>

        <!-- Status & Priority Row -->
        <div class="form-row">
          <div class="form-group flex-1">
            <label for="todo-status" class="form-label">Status</label>
            <select
              id="todo-status"
              v-model="form.status"
              class="form-select"
              :disabled="submitting"
            >
              <option value="pending">Pending (Menunggu)</option>
              <option value="progress">Progress (Sedang Dikerjakan)</option>
              <option value="done">Done (Selesai)</option>
            </select>
          </div>

          <div class="form-group flex-1">
            <label for="todo-priority" class="form-label">Prioritas</label>
            <select
              id="todo-priority"
              v-model="form.priority"
              class="form-select"
              :disabled="submitting"
            >
              <option value="low">Low (Rendah)</option>
              <option value="medium">Medium (Sedang)</option>
              <option value="high">High (Tinggi)</option>
            </select>
          </div>
        </div>

        <!-- Description Input -->
        <div class="form-group">
          <div class="label-row">
            <label for="todo-desc" class="form-label">Deskripsi (Opsional)</label>
            <span class="char-count">
              {{ form.description ? form.description.length : 0 }}/10.000
            </span>
          </div>
          <textarea
            id="todo-desc"
            v-model="form.description"
            rows="4"
            maxlength="10000"
            placeholder="Tambahkan rincian teknis, catatan implementasi, atau kriteria pengujian..."
            class="form-textarea"
            :disabled="submitting"
          ></textarea>
        </div>

        <!-- Form Actions -->
        <div class="modal-footer">
          <button
            type="button"
            class="btn btn-secondary"
            @click="$emit('close')"
            :disabled="submitting"
          >
            Batal
          </button>
          <button
            type="submit"
            class="btn btn-primary"
            :disabled="submitting"
          >
            <Loader2 v-if="submitting" :size="16" class="spin" />
            <span v-else>{{ isEdit ? 'Simpan Perubahan' : 'Simpan Todo' }}</span>
          </button>
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted } from 'vue'
import { Plus, Edit3, X, AlertTriangle, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  todo: {
    type: Object,
    default: null
  },
  submitting: {
    type: Boolean,
    default: false
  },
  serverError: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'submit'])

const isEdit = computed(() => !!props.todo && !!props.todo.id)

const form = reactive({
  title: '',
  status: 'pending',
  priority: 'medium',
  description: ''
})

const clientErrors = reactive({
  title: ''
})

onMounted(() => {
  if (props.todo) {
    form.title = props.todo.title || ''
    form.status = props.todo.status || 'pending'
    form.priority = props.todo.priority || 'medium'
    form.description = props.todo.description || ''
  }
})

const handleSubmit = () => {
  clientErrors.title = ''
  const trimmedTitle = form.title.trim()

  if (!trimmedTitle) {
    clientErrors.title = 'Judul todo tidak boleh kosong atau hanya berisi spasi.'
    return
  }
  if (trimmedTitle.length > 255) {
    clientErrors.title = 'Judul maksimal 255 karakter.'
    return
  }

  emit('submit', {
    title: trimmedTitle,
    status: form.status,
    priority: form.priority,
    description: form.description ? form.description.trim() : null
  })
}
</script>

<style scoped>
.modal-header {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 20px 24px 16px 24px;
  border-bottom: 1px solid var(--border-subtle);
}

.modal-header-icon {
  width: 36px;
  height: 36px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-default);
  color: #ffffff;
}

.icon-create {
  color: #ffffff;
}

.icon-edit {
  color: #ffffff;
}

.modal-header-text {
  flex: 1;
}

.modal-heading {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  letter-spacing: -0.015em;
}

.modal-subheading {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.modal-close-btn {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  border-radius: var(--radius-xs);
}
.modal-close-btn:hover {
  color: var(--text-primary);
  background: rgba(255, 255, 255, 0.06);
}

.modal-error-alert {
  margin: 16px 24px 0 24px;
  background: rgba(244, 63, 94, 0.1);
  border: 1px solid rgba(244, 63, 94, 0.25);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  display: flex;
  gap: 10px;
  color: #fecdd3;
  font-size: 12px;
}

.error-alert-title {
  font-weight: 600;
}

.error-detail-list {
  margin-top: 4px;
  padding-left: 18px;
  font-size: 12px;
}

.modal-form {
  padding: 18px 24px 24px 24px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
}

.required {
  color: #f43f5e;
}

.char-count {
  font-size: 11px;
  color: var(--text-muted);
  font-family: var(--font-mono);
}
.char-warning {
  color: #f59e0b;
}

.form-input, .form-select, .form-textarea {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 8px 12px;
  color: var(--text-primary);
  font-size: 13px;
  transition: all 0.12s;
}

.form-input:focus, .form-select:focus, .form-textarea:focus {
  outline: none;
  border-color: var(--border-strong);
  box-shadow: 0 0 0 1px var(--border-strong);
}

.input-error {
  border-color: #f43f5e;
}

.field-error-msg {
  font-size: 12px;
  color: var(--danger);
}

.form-row {
  display: flex;
  gap: 16px;
}

.flex-1 {
  flex: 1;
}

.form-textarea {
  resize: vertical;
  line-height: 1.5;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
