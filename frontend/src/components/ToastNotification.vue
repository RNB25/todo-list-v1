<template>
  <div class="toast-container" aria-live="polite">
    <transition-group name="toast">
      <div
        v-for="toast in toasts"
        :key="toast.id"
        class="toast-item"
        :class="`toast-${toast.type}`"
      >
        <div class="toast-icon">
          <CheckCircle2 v-if="toast.type === 'success'" :size="18" />
          <AlertCircle v-else-if="toast.type === 'error'" :size="18" />
          <Info v-else :size="18" />
        </div>
        <div class="toast-content">
          <div class="toast-title">{{ toast.title }}</div>
          <div v-if="toast.message" class="toast-msg">{{ toast.message }}</div>
        </div>
        <button class="toast-close" @click="$emit('dismiss', toast.id)" aria-label="Tutup notifikasi">
          <X :size="14" />
        </button>
      </div>
    </transition-group>
  </div>
</template>

<script setup>
import { CheckCircle2, AlertCircle, Info, X } from 'lucide-vue-next'

defineProps({
  toasts: {
    type: Array,
    default: () => []
  }
})

defineEmits(['dismiss'])
</script>

<style scoped>
.toast-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 100;
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-width: 380px;
  pointer-events: none;
}

.toast-item {
  pointer-events: auto;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 14px 16px;
  border-radius: var(--radius-md);
  background: #182235;
  border: 1px solid var(--border-subtle);
  box-shadow: var(--shadow-lg);
  color: var(--text-primary);
  min-width: 280px;
}

.toast-success {
  border-left: 4px solid var(--success);
}
.toast-success .toast-icon {
  color: var(--success);
}

.toast-error {
  border-left: 4px solid var(--danger);
}
.toast-error .toast-icon {
  color: var(--danger);
}

.toast-info {
  border-left: 4px solid var(--primary);
}
.toast-info .toast-icon {
  color: var(--primary);
}

.toast-content {
  flex: 1;
}

.toast-title {
  font-weight: 600;
  font-size: 14px;
}

.toast-msg {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.toast-close {
  background: none;
  border: none;
  color: var(--text-muted);
  cursor: pointer;
  padding: 2px;
  display: flex;
  align-items: center;
}
.toast-close:hover {
  color: var(--text-primary);
}

.toast-enter-active,
.toast-leave-active {
  transition: all 0.25s ease;
}
.toast-enter-from {
  opacity: 0;
  transform: translateX(30px);
}
.toast-leave-to {
  opacity: 0;
  transform: scale(0.95);
}
</style>
