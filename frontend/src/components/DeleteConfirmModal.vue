<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content delete-modal" role="dialog" aria-labelledby="delete-title">
      <div class="delete-icon-wrapper">
        <AlertTriangle :size="22" />
      </div>

      <div class="delete-text-content">
        <h2 id="delete-title" class="delete-heading">Hapus Item Todo</h2>
        <p class="delete-desc">
          Apakah Anda yakin ingin menghapus todo ini secara permanen dari database MySQL? Tindakan ini tidak dapat dibatalkan.
        </p>

        <div class="item-preview-card">
          <div class="preview-title">{{ todo.title }}</div>
          <div class="preview-id">{{ todo.id }}</div>
        </div>
      </div>

      <div class="modal-footer">
        <button
          class="btn btn-secondary btn-sm"
          @click="$emit('close')"
          :disabled="deleting"
        >
          Batal
        </button>
        <button
          class="btn btn-danger btn-sm"
          @click="$emit('confirm', todo.id)"
          :disabled="deleting"
        >
          <Loader2 v-if="deleting" :size="13" class="spin" />
          <span v-else>Hapus Permanen</span>
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
  max-width: 420px;
  text-align: center;
  padding: 24px;
}

.delete-icon-wrapper {
  width: 44px;
  height: 44px;
  border-radius: var(--radius-sm);
  background: rgba(244, 63, 94, 0.1);
  border: 1px solid rgba(244, 63, 94, 0.25);
  color: #fb7185;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 16px auto;
}

.delete-heading {
  font-size: 16px;
  font-weight: 700;
  color: #ffffff;
  margin-bottom: 6px;
}

.delete-desc {
  font-size: 12px;
  color: var(--text-muted);
  line-height: 1.45;
  margin-bottom: 16px;
}

.item-preview-card {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 10px 14px;
  text-align: left;
  margin-bottom: 18px;
}

.preview-title {
  font-size: 13px;
  font-weight: 600;
  color: #ffffff;
  margin-bottom: 4px;
}

.preview-id {
  font-family: var(--font-mono);
  font-size: 11px;
  color: var(--text-muted);
  word-break: break-all;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
