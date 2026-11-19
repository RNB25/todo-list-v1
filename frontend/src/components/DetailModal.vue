<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content" role="dialog" aria-labelledby="detail-title">
      <div class="modal-header">
        <div class="detail-header-icon">
          <Terminal :size="18" />
        </div>
        <div class="modal-header-text">
          <h2 id="detail-title" class="modal-heading">Detail Pekerjaan</h2>
          <p class="modal-subheading">Entitas database MySQL & representasi objek UUID v7</p>
        </div>
        <button class="modal-close-btn" @click="$emit('close')" aria-label="Tutup detail">
          <X :size="16" />
        </button>
      </div>

      <div class="detail-body">
        <!-- UUID v7 Inspector -->
        <div class="detail-row">
          <div class="detail-label">UUID v7 (Canonical 36-char string):</div>
          <div class="uuid-inspector-box">
            <span class="uuid-text">{{ todo.id }}</span>
            <button class="btn btn-secondary btn-sm" @click="copyUuid(todo.id)">
              <Check v-if="copied" :size="12" class="copy-check" />
              <Copy v-else :size="12" />
              <span>{{ copied ? 'Tersalin' : 'Salin' }}</span>
            </button>
          </div>
          <div v-if="uuidTimestamp" class="uuid-decoded-hint">
            <span class="hint-tag">UUIDv7 Decoded Time</span>
            <span>{{ uuidTimestamp }}</span>
          </div>
        </div>

        <!-- Title Section -->
        <div class="detail-row">
          <div class="detail-label">Judul Todo:</div>
          <div class="detail-title-val">{{ todo.title }}</div>
        </div>

        <!-- Badges Row -->
        <div class="detail-meta-grid">
          <div class="meta-card">
            <div class="meta-label">Status</div>
            <span class="badge" :class="`badge-${todo.status}`">
              {{ todo.status }}
            </span>
          </div>

          <div class="meta-card">
            <div class="meta-label">Prioritas</div>
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
            <p v-else class="desc-empty">Tidak ada deskripsi tambahan untuk todo ini.</p>
          </div>
        </div>

        <!-- Timestamps Section -->
        <div class="detail-timestamps-box">
          <div class="ts-row">
            <span class="ts-label">Waktu Dibuat:</span>
            <span class="ts-val">{{ todo.created_at }}</span>
          </div>
          <div class="ts-row">
            <span class="ts-label">Waktu Diperbarui:</span>
            <span class="ts-val">{{ todo.updated_at }}</span>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button class="btn btn-danger btn-sm" @click="$emit('delete', todo)">
          <Trash2 :size="13" />
          <span>Hapus</span>
        </button>
        <button class="btn btn-secondary btn-sm" @click="$emit('edit', todo)">
          <Pencil :size="13" />
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
import { ref, computed } from 'vue'
import { Terminal, X, Copy, Check, Pencil, Trash2 } from 'lucide-vue-next'

const props = defineProps({
  todo: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close', 'edit', 'delete', 'copy-success'])
const copied = ref(false)

function copyUuid(id) {
  navigator.clipboard.writeText(id).then(() => {
    copied.value = true
    emit('copy-success', `UUID tersalin: ${id}`)
    setTimeout(() => {
      copied.value = false
    }, 2000)
  })
}

const uuidTimestamp = computed(() => {
  if (!props.todo?.id) return null
  try {
    const raw = props.todo.id.replace(/-/g, '')
    if (raw.length >= 12) {
      const msHex = raw.substring(0, 12)
      const ms = parseInt(msHex, 16)
      if (!isNaN(ms) && ms > 1500000000000 && ms < 2500000000000) {
        return new Date(ms).toLocaleString('id-ID', {
          dateStyle: 'medium',
          timeStyle: 'medium'
        })
      }
    }
  } catch {}
  return null
})
</script>

<style scoped>
.modal-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-subtle);
}

.detail-header-icon {
  width: 32px;
  height: 32px;
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-default);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
}

.modal-header-text {
  flex: 1;
}

.modal-heading {
  font-size: 15px;
  font-weight: 700;
  color: var(--text-primary);
}

.modal-subheading {
  font-size: 11px;
  color: var(--text-muted);
}

.modal-close-btn {
  background: transparent;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 4px;
  border-radius: var(--radius-xs);
  display: flex;
}
.modal-close-btn:hover {
  color: #ffffff;
  background: rgba(255, 255, 255, 0.06);
}

.detail-body {
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.detail-row {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.detail-label {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: var(--text-muted);
}

.uuid-inspector-box {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  padding: 8px 12px;
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
}

.uuid-text {
  font-family: var(--font-mono);
  font-size: 12px;
  color: #38bdf8;
  word-break: break-all;
}

.copy-check {
  color: #10b981;
}

.uuid-decoded-hint {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 11px;
  color: var(--text-secondary);
  font-family: var(--font-mono);
  padding: 0 4px;
}

.hint-tag {
  background: rgba(255, 255, 255, 0.06);
  padding: 1px 6px;
  border-radius: var(--radius-xs);
  font-size: 10px;
  color: var(--text-muted);
}

.detail-title-val {
  font-size: 15px;
  font-weight: 600;
  color: #ffffff;
  line-height: 1.4;
}

.detail-meta-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
}

.meta-card {
  padding: 10px 12px;
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.meta-label {
  font-size: 11px;
  font-weight: 500;
  color: var(--text-muted);
}

.detail-desc-box {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 12px;
  min-height: 70px;
}

.desc-text {
  font-size: 13px;
  color: var(--text-primary);
  line-height: 1.5;
  white-space: pre-wrap;
}

.desc-empty {
  font-size: 12px;
  color: var(--text-muted);
  font-style: italic;
}

.detail-timestamps-box {
  padding: 10px 12px;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.ts-row {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  font-family: var(--font-mono);
}

.ts-label {
  color: var(--text-muted);
}

.ts-val {
  color: var(--text-secondary);
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  padding: 14px 20px;
  border-top: 1px solid var(--border-subtle);
}
</style>
