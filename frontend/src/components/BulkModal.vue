<template>
  <div class="modal-overlay" @click.self="!generating && $emit('close')">
    <div class="modal-content bulk-modal" role="dialog" aria-labelledby="bulk-title">
      <div class="modal-header">
        <div class="bulk-header-icon">
          <Sparkles :size="22" />
        </div>
        <div class="modal-header-text">
          <h2 id="bulk-title" class="modal-heading">Generate Data Acak Massal</h2>
          <p class="modal-subheading">Pembuatan data acak otomatis secara atomik (SRS UC-07)</p>
        </div>
        <button
          v-if="!generating"
          class="modal-close-btn"
          @click="$emit('close')"
          aria-label="Tutup modal bulk"
        >
          <X :size="18" />
        </button>
      </div>

      <div class="bulk-body">
        <div class="bulk-info-banner">
          <Info :size="16" class="info-icon" />
          <p>
            Fitur ini menghasilkan data todo dengan <strong>UUID v7</strong>, judul realistis, status, dan prioritas acak. Seluruh data disimpan dalam satu transaksi atomik.
          </p>
        </div>

        <!-- Slider & Count Input -->
        <div class="count-selector-group">
          <div class="count-label-row">
            <label for="bulk-count-input" class="form-label">Jumlah Todo yang Dibuat:</label>
            <span class="count-display">{{ count }} item</span>
          </div>

          <div class="slider-row">
            <input
              type="range"
              min="1"
              max="1000"
              step="50"
              v-model.number="count"
              :disabled="generating"
              class="range-slider"
            />
          </div>

          <div class="quick-preset-chips">
            <button
              v-for="p in [10, 100, 500, 1000]"
              :key="p"
              type="button"
              class="preset-chip"
              :class="{ active: count === p }"
              :disabled="generating"
              @click="count = p"
            >
              {{ p === 1000 ? '1.000 (Default)' : p }}
            </button>
          </div>
        </div>

        <!-- Generating Progress State -->
        <div v-if="generating" class="generating-progress-box">
          <Loader2 :size="24" class="spin progress-spinner" />
          <div class="progress-text-group">
            <div class="progress-title">Sedang Membuat {{ count.toLocaleString('id-ID') }} Todo...</div>
            <div class="progress-subtitle">Menghasilkan UUID v7 dan memproses transaksi database MySQL</div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button
          class="btn btn-secondary"
          @click="$emit('close')"
          :disabled="generating"
        >
          Batal
        </button>
        <button
          class="btn btn-bulk"
          @click="startGenerate"
          :disabled="generating || count < 1 || count > 1000"
        >
          <Loader2 v-if="generating" :size="16" class="spin" />
          <Sparkles v-else :size="16" />
          <span>{{ generating ? 'Memproses...' : `Generate ${count.toLocaleString('id-ID')} Data` }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Sparkles, X, Info, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  generating: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'confirm'])

const count = ref(1000)

const startGenerate = () => {
  emit('confirm', count.value)
}
</script>

<style scoped>
.bulk-modal {
  max-width: 500px;
}

.modal-header {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 20px 24px 16px 24px;
  border-bottom: 1px solid var(--border-subtle);
}

.bulk-header-icon {
  width: 42px;
  height: 42px;
  border-radius: var(--radius-md);
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2), rgba(139, 92, 246, 0.2));
  color: #a78bfa;
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

.bulk-body {
  padding: 20px 24px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.bulk-info-banner {
  background: rgba(99, 102, 241, 0.1);
  border: 1px solid rgba(99, 102, 241, 0.25);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  font-size: 13px;
  color: #c7d2fe;
  line-height: 1.5;
}

.info-icon {
  color: #a5b4fc;
  flex-shrink: 0;
  margin-top: 2px;
}

.count-selector-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.count-label-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.form-label {
  font-size: 13px;
  font-weight: 600;
  color: var(--text-secondary);
}

.count-display {
  font-size: 16px;
  font-weight: 700;
  color: #a78bfa;
  font-family: var(--font-mono);
}

.range-slider {
  width: 100%;
  accent-color: #6366f1;
  cursor: pointer;
}

.quick-preset-chips {
  display: flex;
  gap: 8px;
  margin-top: 4px;
}

.preset-chip {
  background: var(--bg-input);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-full);
  padding: 5px 12px;
  font-size: 12px;
  font-weight: 500;
  color: var(--text-secondary);
  cursor: pointer;
  transition: all 0.15s;
}

.preset-chip:hover {
  border-color: #6366f1;
  color: var(--text-primary);
}

.preset-chip.active {
  background: rgba(99, 102, 241, 0.2);
  border-color: #6366f1;
  color: #c7d2fe;
  font-weight: 600;
}

.generating-progress-box {
  background: #0f1523;
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-md);
  padding: 16px;
  display: flex;
  align-items: center;
  gap: 14px;
}

.progress-spinner {
  color: #a78bfa;
}

.progress-title {
  font-weight: 600;
  font-size: 14px;
  color: var(--text-primary);
}

.progress-subtitle {
  font-size: 12px;
  color: var(--text-muted);
  margin-top: 2px;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
  padding: 16px 24px;
  border-top: 1px solid var(--border-subtle);
  background: #0f1523;
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
