<template>
  <div class="modal-overlay" @click.self="!generating && $emit('close')">
    <div class="modal-content bulk-modal" role="dialog" aria-labelledby="bulk-title">
      <div class="modal-header">
        <div class="bulk-header-icon">
          <Database :size="18" />
        </div>
        <div class="modal-header-text">
          <h2 id="bulk-title" class="modal-heading">Generate Data Massal</h2>
          <p class="modal-subheading">Injeksi data acak dengan UUID v7 dalam 1 transaksi atomik (UC-07)</p>
        </div>
        <button
          v-if="!generating"
          class="modal-close-btn"
          @click="$emit('close')"
          aria-label="Tutup modal bulk"
        >
          <X :size="16" />
        </button>
      </div>

      <div class="bulk-body">
        <div class="bulk-info-banner">
          <Info :size="15" class="info-icon" />
          <p>
            Fitur ini menghasilkan data todo dengan <strong>UUID v7</strong>, judul realistis, status, dan prioritas acak. Seluruh data disimpan langsung ke database MySQL.
          </p>
        </div>

        <!-- Slider & Count Input -->
        <div class="count-selector-group">
          <div class="count-label-row">
            <label for="bulk-count-input" class="form-label">Jumlah Todo Dihasilkan:</label>
            <span class="count-display">{{ count.toLocaleString('id-ID') }} item</span>
          </div>

          <div class="slider-row">
            <input
              type="range"
              min="10"
              max="1000"
              step="10"
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
              {{ p === 1000 ? '1.000 (SRS Max)' : `${p} item` }}
            </button>
          </div>
        </div>

        <!-- Generating Progress State -->
        <div v-if="generating" class="generating-progress-box">
          <Loader2 :size="20" class="spin progress-spinner" />
          <div class="progress-text-group">
            <div class="progress-title">Sedang Menghasilkan {{ count.toLocaleString('id-ID') }} Data...</div>
            <div class="progress-subtitle">Memproses UUIDv7 sequence dan commit transaksi MySQL</div>
          </div>
        </div>
      </div>

      <div class="modal-footer">
        <button
          class="btn btn-secondary btn-sm"
          @click="$emit('close')"
          :disabled="generating"
        >
          Batal
        </button>
        <button
          class="btn btn-primary btn-sm"
          @click="startGenerate"
          :disabled="generating || count < 1 || count > 1000"
        >
          <Loader2 v-if="generating" :size="13" class="spin" />
          <Database v-else :size="13" />
          <span>{{ generating ? 'Menyimpan...' : `Eksekusi ${count.toLocaleString('id-ID')} Data` }}</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { Database, X, Info, Loader2 } from 'lucide-vue-next'

const props = defineProps({
  generating: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['close', 'confirm'])
const count = ref(1000)

function startGenerate() {
  if (count.value >= 1 && count.value <= 1000) {
    emit('confirm', count.value)
  }
}
</script>

<style scoped>
.modal-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-subtle);
}

.bulk-header-icon {
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

.bulk-body {
  padding: 18px 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.bulk-info-banner {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-sm);
  padding: 10px 12px;
  display: flex;
  gap: 10px;
  font-size: 12px;
  color: var(--text-secondary);
  line-height: 1.45;
}

.info-icon {
  color: #38bdf8;
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
  align-items: baseline;
}

.form-label {
  font-size: 12px;
  font-weight: 600;
  color: var(--text-secondary);
}

.count-display {
  font-family: var(--font-mono);
  font-size: 14px;
  font-weight: 700;
  color: #ffffff;
}

.range-slider {
  width: 100%;
  accent-color: #ffffff;
  cursor: pointer;
}

.quick-preset-chips {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}

.preset-chip {
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border-subtle);
  border-radius: var(--radius-xs);
  padding: 4px 10px;
  color: var(--text-secondary);
  font-size: 11px;
  font-family: var(--font-mono);
  cursor: pointer;
  transition: all 0.12s;
}

.preset-chip:hover {
  background: rgba(255, 255, 255, 0.08);
  color: #ffffff;
}

.preset-chip.active {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
  color: #ffffff;
  font-weight: 600;
}

.generating-progress-box {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-sm);
  padding: 12px 14px;
  display: flex;
  align-items: center;
  gap: 12px;
}

.progress-spinner {
  color: #38bdf8;
}

.progress-title {
  font-size: 12px;
  font-weight: 600;
  color: #ffffff;
}

.progress-subtitle {
  font-size: 11px;
  color: var(--text-muted);
}

.modal-footer {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 8px;
  padding: 14px 20px;
  border-top: 1px solid var(--border-subtle);
}

.spin {
  animation: spin 1s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>
