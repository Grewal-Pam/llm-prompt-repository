<script setup lang="ts">
import { ref } from "vue"
import { createPrompt } from "../services/api"

const emit = defineEmits<{
  promptAdded: []
}>()

const title = ref("")
const promptText = ref("")
const purpose = ref("")
const tags = ref("")
const source = ref("")
const error = ref("")
const success = ref("")
const loading = ref(false)

async function submitPrompt() {
  error.value = ""
  
  // Validate required fields
  if (!title.value.trim()) {
    error.value = "Title is required"
    return
  }
  if (!promptText.value.trim()) {
    error.value = "Prompt text is required"
    return
  }
  if (!purpose.value.trim()) {
    error.value = "Purpose is required"
    return
  }
  
  loading.value = true

  try {
    const payload: any = {
      title: title.value,
      prompt_text: promptText.value,
      purpose: purpose.value
    }

    if (tags.value.trim() !== "") {
      payload.tags = tags.value.split(",").map(t => t.trim())
    }

    if (source.value.trim() !== "") {
      payload.source = source.value
    }

    await createPrompt(payload)

    // Clear form
    title.value = ""
    promptText.value = ""
    purpose.value = ""
    tags.value = ""
    source.value = ""

    success.value = "✅ Prompt added successfully!"
    emit('promptAdded')
    
    // Clear success message after 4 seconds
    setTimeout(() => {
      success.value = ""
    }, 4000)

  } catch (e) {
    error.value = e instanceof Error ? e.message : "Could not submit prompt"
    console.error("Submit error:", e)
  } finally {
    loading.value = false
  }
}

</script>

<template>
  <section class="add-prompt-form">
    <div class="form-header">
      <h2>➕ Add New Prompt</h2>
      <p>Share your LLM prompt with the scientific community</p>
    </div>

    <div v-if="error" class="message error">{{ error }}</div>
    <div v-if="success" class="message success">{{ success }}</div>

    <form @submit.prevent="submitPrompt" class="form">
      <div class="form-row">
        <div class="form-group">
          <label for="title">Title <span class="required">*</span></label>
          <input 
            id="title"
            v-model="title" 
            placeholder="e.g. ClickBaitTitle"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="purpose">Purpose <span class="required">*</span></label>
          <input 
            id="purpose"
            v-model="purpose" 
            placeholder="e.g. Text rewriting, Code documentation"
            :disabled="loading"
          />
        </div>
      </div>

      <div class="form-group">
        <label for="promptText">Prompt Text <span class="required">*</span></label>
        <textarea 
          id="promptText"
          v-model="promptText" 
          placeholder="Enter the complete prompt text here..."
          rows="4"
          :disabled="loading"
        ></textarea>
      </div>

      <div class="form-row">
        <div class="form-group">
          <label for="tags">Tags (comma separated)</label>
          <input 
            id="tags"
            v-model="tags" 
            placeholder="e.g. headline, rewriting, documentation"
            :disabled="loading"
          />
        </div>

        <div class="form-group">
          <label for="source">Source</label>
          <input 
            id="source"
            v-model="source" 
            placeholder="e.g. Manual, Dr. Smith, https://..."
            :disabled="loading"
          />
        </div>
      </div>

      <button type="submit" class="submit-btn" :disabled="loading">
        {{ loading ? "⏳ Saving..." : "📤 Add Prompt" }}
      </button>
    </form>
  </section>
</template>

<style scoped>
.add-prompt-form {
  background: white;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.form-header {
  margin-bottom: 1.5rem;
}

.form-header h2 {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
  font-size: 1.8rem;
}

.form-header p {
  margin: 0;
  color: #718096;
  font-size: 1rem;
}

.message {
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1.5rem;
  font-weight: 500;
}

.message.error {
  background: #fed7d7;
  color: #c53030;
  border: 2px solid #fc8181;
}

.message.success {
  background: #c6f6d5;
  color: #22543d;
  border: 2px solid #68d391;
}

.form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 1.5rem;
}

@media (max-width: 768px) {
  .form-row {
    grid-template-columns: 1fr;
  }
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  margin-bottom: 0.5rem;
  color: #2d3748;
  font-weight: 600;
  font-size: 0.95rem;
}

.required {
  color: #e53e3e;
}

.form-group input,
.form-group textarea {
  padding: 0.75rem 1rem;
  border: 2px solid #e2e8f0;
  border-radius: 8px;
  font-size: 1rem;
  font-family: inherit;
  background: white;
  color: #2d3748;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: #a0aec0;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}

.form-group input:disabled,
.form-group textarea:disabled {
  background-color: #f7fafc;
  cursor: not-allowed;
  opacity: 0.6;
}

.form-group textarea {
  resize: vertical;
  min-height: 100px;
}

.submit-btn {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 600;
  border-radius: 8px;
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  align-self: flex-start;
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
}

.submit-btn:disabled {
  background: #cbd5e0;
  cursor: not-allowed;
  transform: none;
}
</style>
