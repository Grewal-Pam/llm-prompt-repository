
export interface Prompt {
  id: number
  title: string
  prompt_text: string
  purpose: string
  tags?: string[]
  source?: string
  created_at: string
}

export interface PromptCreate {
  title: string
  prompt_text: string
  purpose: string
  tags?: string[]
  source?: string
}

const API_BASE = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "")

export async function fetchPrompts(): Promise<Prompt[]> {
  const response = await fetch(`${API_BASE}/api/prompts`)
  if (!response.ok) {
    throw new Error("Failed to fetch prompts")
  }
  return response.json()
}

export async function createPrompt(prompt: PromptCreate): Promise<Prompt> {
  const response = await fetch(`${API_BASE}/api/prompts`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(prompt)
  })
  if (!response.ok) {
    const text = await response.text()
    throw new Error(text || "Failed to create prompt")
  }
  return response.json()
}
