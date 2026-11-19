<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content delete-modal" role="dialog" aria-labelledby="delete-title">
      <div class="delete-icon-wrapper">
        <AlertTriangle :size="28" />
      </div>

      <div class="delete-text-content">
        <h2 id="delete-title" class="delete-heading">Konfirmasi Hapus Todo</h2>
        <p class="delete-desc">
          Apakah Anda yakin ingin menghapus todo ini secara permanen? Tindakan ini tidak dapat dibatalkan.
        </p>

        <div class="item-preview-card">
          <div class="preview-title">{{ todo.title }}</div>
          <div class="preview-id">{{ todo.id }}</div>
        </div>
      </div>

      <div class="modal-footer">
        <button
          class="btn btn-secondary"
          @click="$emit('close')"
          :disabled="deleting"
        >
          Batal
        </button>
        <button
          class="btn btn-danger"
          @click="$emit('confirm', todo.id)"
          :disabled="deleting"
        >
          <Loader2 v-if="deleting" :size="15" class="spin" />
          <span v-else>Ya, Hapus Permanen</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { AlertTriangle, Loader2 } from 'lucide-vue-next'

defineProps({
  todo: {
    type: Object,
    required: true
  },
  deleting: {
    type: Boolean,
    default: false
  }
})

defineEmits(['close', 'confirm'])
</script>

<style scoped>
.delete-modal {
  max-width: 440px;
  text-align: center;
  padding: 24px;
}

.delete-icon-wrapper {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--danger-subtle);
  color: var(--danger);
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px auto;
}

.delete-heading {
  font-size: 18px;
  font-weight: 700;
  color: var(--text-primary);
  margin-bottom: 8px;
}

.delete-desc {
  font-size: 14px;
  color: var(--text-secondary);
  line-height: 1.5;
  margin-bottom: 16px;
}

.item-preview-card {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 12px 14px;
  text-align: left;
  margin-bottom: 20px;
}

.preview-title {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
}

.preview-id {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  margin-top: 4px;
}

.modal-footer {
  display: flex;
  justify-content: center;
  gap: 12px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
