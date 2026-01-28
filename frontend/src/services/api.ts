const API_BASE = (import.meta.env.VITE_API_BASE_URL || "").replace(/\/$/, "")

export interface Prompt {
  id: number
  title: string
  prompt_text: string
  purpose: string
  tags?: string[]
  source?: string
  created_at: string
}

export async function fetchPrompts(): Promise<Prompt[]> {
  const response = await fetch(`${API_BASE}/prompts`)
  if (!response.ok) {
    throw new Error("Failed to fetch prompts")
  }
  return response.json()
}
