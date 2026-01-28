<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { fetchPrompts, type Prompt } from './services/api'
import AddPromptForm from "./components/AddPromptForm.vue"

const prompts = ref<Prompt[]>([])
const loading = ref(true)
const error = ref<string | null>(null)
const searchQuery = ref('')
const selectedPurpose = ref('')

const purposes = computed(() => {
  const uniquePurposes = new Set(prompts.value.map(p => p.purpose))
  return Array.from(uniquePurposes).sort()
})

const filteredPrompts = computed(() => {
  let filtered = prompts.value
  
  if (searchQuery.value.trim()) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(p => 
      p.title.toLowerCase().includes(query) ||
      p.prompt_text.toLowerCase().includes(query) ||
      p.purpose.toLowerCase().includes(query) ||
      p.tags?.some(t => t.toLowerCase().includes(query))
    )
  }
  
  if (selectedPurpose.value) {
    filtered = filtered.filter(p => p.purpose === selectedPurpose.value)
  }
  
  return filtered
})

async function loadPrompts() {
  loading.value = true
  error.value = null
  try {
    prompts.value = await fetchPrompts()
  } catch (e) {
    error.value = 'Failed to load prompts.'
  } finally {
    loading.value = false
  }
}

function handlePromptAdded() {
  loadPrompts()
}

onMounted(() => {
  loadPrompts()
})
</script>



<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <h1>🧪 LLM Prompt Repository</h1>
        <p class="subtitle">Anonymous repository for sharing scientific LLM prompts</p>
      </div>
    </header>

    <main class="container">
      <AddPromptForm @prompt-added="handlePromptAdded" />

      <section class="prompts-section">
        <div class="section-header">
          <h2>Browse Prompts ({{ filteredPrompts.length }})</h2>
          
          <div class="filters">
            <div class="search-box">
              <input 
                v-model="searchQuery" 
                type="search" 
                placeholder="🔍 Search prompts, tags, or purpose..."
                class="search-input"
              />
            </div>
            
            <select v-model="selectedPurpose" class="purpose-filter">
              <option value="">All Purposes</option>
              <option v-for="purpose in purposes" :key="purpose" :value="purpose">
                {{ purpose }}
              </option>
            </select>
          </div>
        </div>

        <div v-if="loading" class="loading">Loading prompts...</div>
        <div v-else-if="error" class="error-message">{{ error }}</div>
        
        <div v-else-if="filteredPrompts.length === 0" class="no-results">
          <p>No prompts found matching your criteria.</p>
        </div>
        
        <div v-else class="prompts-grid">
          <article v-for="prompt in filteredPrompts" :key="prompt.id" class="prompt-card">
            <div class="prompt-header">
              <h3 class="prompt-title">{{ prompt.title }}</h3>
              <span class="prompt-purpose">{{ prompt.purpose }}</span>
            </div>
            
            <p class="prompt-text">{{ prompt.prompt_text }}</p>
            
            <div class="prompt-footer">
              <div class="tags" v-if="prompt.tags && prompt.tags.length">
                <span v-for="tag in prompt.tags" :key="tag" class="tag">
                  #{{ tag }}
                </span>
              </div>
              
              <div class="prompt-meta">
                <a v-if="prompt.source" :href="prompt.source" target="_blank" class="source-link">
                  📄 Source
                </a>
                <span class="date">{{ new Date(prompt.created_at).toLocaleDateString() }}</span>
              </div>
            </div>
          </article>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
* {
  box-sizing: border-box;
}

.app {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
}

.header {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  padding: 2rem 0;
  box-shadow: 0 2px 20px rgba(0, 0, 0, 0.1);
  margin-bottom: 2rem;
}

.header h1 {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
  font-size: 2.5rem;
  font-weight: 700;
}

.subtitle {
  margin: 0;
  color: #718096;
  font-size: 1.1rem;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
}

.prompts-section {
  margin-top: 3rem;
}

.section-header {
  margin-bottom: 2rem;
}

.section-header h2 {
  color: white;
  font-size: 1.8rem;
  margin: 0 0 1rem 0;
}

.filters {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
}

.search-box {
  flex: 1;
  min-width: 250px;
}

.search-input {
  width: 100%;
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.95);
  color: #2d3748;
  transition: all 0.3s;
}

.search-input::placeholder {
  color: #a0aec0;
}

.search-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2);
}

.purpose-filter {
  padding: 0.75rem 1rem;
  font-size: 1rem;
  border: 2px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.95);
  color: #2d3748;
  cursor: pointer;
  min-width: 200px;
}

.loading,
.no-results {
  text-align: center;
  padding: 3rem;
  background: rgba(255, 255, 255, 0.95);
  border-radius: 12px;
  color: #4a5568;
}

.error-message {
  padding: 1rem;
  background: #fed7d7;
  color: #c53030;
  border-radius: 8px;
  border: 2px solid #fc8181;
}

.prompts-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.prompt-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
  display: flex;
  flex-direction: column;
}

.prompt-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 24px rgba(0, 0, 0, 0.15);
}

.prompt-header {
  margin-bottom: 1rem;
}

.prompt-title {
  margin: 0 0 0.5rem 0;
  color: #2d3748;
  font-size: 1.3rem;
  font-weight: 600;
}

.prompt-purpose {
  display: inline-block;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 0.25rem 0.75rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.prompt-text {
  color: #4a5568;
  line-height: 1.6;
  margin: 0 0 1rem 0;
  flex: 1;
}

.prompt-footer {
  border-top: 1px solid #e2e8f0;
  padding-top: 1rem;
  margin-top: auto;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  margin-bottom: 0.75rem;
}

.tag {
  background: #edf2f7;
  color: #4a5568;
  padding: 0.25rem 0.75rem;
  border-radius: 12px;
  font-size: 0.85rem;
  font-weight: 500;
}

.prompt-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.85rem;
  color: #718096;
}

.source-link {
  color: #667eea;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.source-link:hover {
  color: #764ba2;
  text-decoration: underline;
}

.date {
  color: #a0aec0;
}
</style>
