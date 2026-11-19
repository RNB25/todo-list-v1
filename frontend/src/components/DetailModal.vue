<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content" role="dialog" aria-labelledby="detail-title">
      <div class="modal-header">
        <div class="detail-header-icon">
          <FileText :size="20" />
        </div>
        <div class="modal-header-text">
          <h2 id="detail-title" class="modal-heading">Detail Todo</h2>
          <p class="modal-subheading">Informasi lengkap data pekerjaan terdaftar</p>
        </div>
        <button class="modal-close-btn" @click="$emit('close')" aria-label="Tutup detail">
          <X :size="18" />
        </button>
      </div>

      <div class="detail-body">
        <!-- UUID v7 Section -->
        <div class="detail-row">
          <div class="detail-label">ID (UUID v7 Kanonis):</div>
          <div class="detail-uuid-row">
            <span class="uuid-full-text">{{ todo.id }}</span>
            <button class="btn btn-secondary btn-sm" @click="copyUuid(todo.id)">
              <Copy :size="13" />
              <span>Salin</span>
            </button>
          </div>
        </div>

        <!-- Title Section -->
        <div class="detail-row">
          <div class="detail-label">Judul:</div>
          <div class="detail-title-val">{{ todo.title }}</div>
        </div>

        <!-- Badges Row -->
        <div class="detail-badges-row">
          <div class="badge-item">
            <div class="detail-label">Status:</div>
            <span class="badge" :class="`badge-${todo.status}`">
              {{ todo.status }}
            </span>
          </div>

          <div class="badge-item">
            <div class="detail-label">Prioritas:</div>
            <span class="badge" :class="`badge-${todo.priority}`">
              {{ todo.priority }}
            </span>
          </div>
        </div>

        <!-- Description Section -->
        <div class="detail-row">
          <div class="detail-label">Deskripsi:</div>
          <div class="detail-desc-box">
            <p v-if="todo.description" class="desc-text">{{ todo.description }}</p>
            <p v-else class="desc-empty">Tidak ada deskripsi tambahan.</p>
          </div>
        </div>

        <!-- Timestamps Section -->
        <div class="detail-timestamps">
          <div class="timestamp-col">
            <span class="ts-label">Waktu Dibuat (UTC):</span>
            <span class="ts-val">{{ todo.created_at }}</span>
          </div>
          <div class="timestamp-col">
            <span class="ts-label">Waktu Diperbarui (UTC):</span>
            <span class="ts-val">{{ todo.updated_at }}</span>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-danger btn-sm" @click="$emit('delete', todo)">
          <Trash2 :size="14" />
          <span>Hapus</span>
        </button>
        <button class="btn btn-secondary btn-sm" @click="$emit('edit', todo)">
          <Edit3 :size="14" />
          <span>Edit</span>
        </button>
        <button class="btn btn-primary btn-sm" @click="$emit('close')">
          Tutup
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { FileText, X, Copy, Edit3, Trash2 } from 'lucide-vue-next'

const props = defineProps({
  todo: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'edit', 'delete', 'copy-success'])

const copyUuid = async (uuid) => {
  try {
    await navigator.clipboard.writeText(uuid)
    emit('copy-success', 'UUID v7 berhasil disalin ke clipboard!')
  } catch {
    // fallback
  }
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

.detail-header-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-md);
  background: rgba(56, 189, 248, 0.15);
  color: #38bdf8;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.modal-header-text {
  flex: 1;
}

.modal-heading {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
}

.modal-subheading {
  font-size: 13px;
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
}
.modal-close-btn:hover {
  color: var(--text-primary);
}

.detail-body {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.detail-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-label {
  font-size: 12px;
  font-weight: 700;
  color: var(--text-muted);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.detail-uuid-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  background: var(--bg-input);
  padding: 8px 12px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
}

.uuid-full-text {
  font-family: var(--font-mono);
  font-size: 12px;
  color: #38bdf8;
  word-break: break-all;
}

.detail-title-val {
  font-size: 16px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.4;
}

.detail-badges-row {
  display: flex;
  gap: 24px;
  padding: 12px 16px;
  background: var(--bg-input);
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
}

.badge-item {
  display: flex;
  align-items: center;
  gap: 10px;
}

.detail-desc-box {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 14px;
  min-height: 80px;
  max-height: 220px;
  overflow-y: auto;
}

.desc-text {
  font-size: 14px;
  color: var(--text-primary);
  white-space: pre-wrap;
  line-height: 1.6;
}

.desc-empty {
  font-size: 13px;
  color: var(--text-muted);
  font-style: italic;
}

.detail-timestamps {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  background: #0f1523;
  padding: 12px 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--border-subtle);
}

.timestamp-col {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.ts-label {
  font-size: 11px;
  color: var(--text-muted);
  text-transform: uppercase;
}

.ts-val {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-secondary);
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-subtle);
  background: #0f1523;
}
</style>
