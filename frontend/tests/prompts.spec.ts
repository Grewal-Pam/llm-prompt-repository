import { expect, test, type Page } from '@playwright/test'

type Prompt = {
  id: number
  title: string
  prompt_text: string
  purpose: string
  tags?: string[]
  source?: string
  created_at: string
}

const initialPrompts: Prompt[] = [
  {
    id: 1,
    title: 'ClickBaitTitle',
    prompt_text: 'Rewrite the given text as a clickbait-style headline.',
    purpose: 'Text rewriting',
    tags: ['headline', 'rewriting'],
    source: 'https://resources.wolframcloud.com/PromptRepository/',
    created_at: '2026-06-25T00:00:00.000Z',
  },
  {
    id: 2,
    title: 'SurveySummary',
    prompt_text: 'Summarize the survey response into concise research notes.',
    purpose: 'Summarization',
    tags: ['survey', 'research'],
    created_at: '2026-06-25T00:01:00.000Z',
  },
]

test.describe('LLM Prompt Repository', () => {
  test('shows MCP capabilities after clicking the button', async ({ page }) => {
    await mockPromptsApi(page, [...initialPrompts])
    await page.route('**/mcp/capabilities', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          protocol: 'mcp-lite',
          capabilities: ['prompt_catalog', 'prompt_creation'],
          prompt_count: 2,
          latest_prompt: 'SurveySummary',
        }),
      })
    })

    await page.goto('/')

    await page.getByRole('button', { name: 'Check MCP capabilities' }).click()

    await expect(page.getByText('MCP: mcp-lite')).toBeVisible()
    await expect(page.getByText('Tools: prompt_catalog, prompt_creation')).toBeVisible()
    await expect(page.getByText('Prompts: 2')).toBeVisible()
    await expect(page.getByText('Latest: SurveySummary')).toBeVisible()
  })

  test('renders prompts and filters them', async ({ page }) => {
    await mockPromptsApi(page, [...initialPrompts])

    await page.goto('/')

    await expect(page.getByRole('heading', { name: 'LLM Prompt Repository' })).toBeVisible()
    await expect(page.getByRole('heading', { name: /Browse Prompts \(2\)/ })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'ClickBaitTitle' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'SurveySummary' })).toBeVisible()

    await page.getByPlaceholder('🔍 Search prompts, tags, or purpose...').fill('survey')
    await expect(page.getByRole('heading', { name: /Browse Prompts \(1\)/ })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'SurveySummary' })).toBeVisible()
    await expect(page.getByRole('heading', { name: 'ClickBaitTitle' })).toHaveCount(0)

    await page.getByPlaceholder('🔍 Search prompts, tags, or purpose...').fill('')
    await expect(page.getByRole('heading', { name: /Browse Prompts \(2\)/ })).toBeVisible()
  })

  test('adds a prompt through the form', async ({ page }) => {
    const prompts = [...initialPrompts]
    await mockPromptsApi(page, prompts)

    await page.goto('/')

    await page.getByLabel('Title *').fill('PaperOutline')
    await page.getByLabel('Purpose *').fill('Outline generation')
    await page.getByLabel('Prompt Text *').fill('Create a paper outline from the abstract.')
    await page.getByLabel('Tags (comma separated)').fill('outline, paper')
    await page.getByLabel('Source').fill('Manual entry')
    await page.getByRole('button', { name: '📤 Add Prompt' }).click()

    await expect(page.getByText('✅ Prompt added successfully!')).toBeVisible()
    await expect(page.getByRole('heading', { name: 'PaperOutline' })).toBeVisible()
    await expect(page.getByRole('heading', { name: /Browse Prompts \(3\)/ })).toBeVisible()
  })
})

async function mockPromptsApi(page: Page, prompts: Prompt[]) {
  let nextId = prompts.reduce((max, prompt) => Math.max(max, prompt.id), 0) + 1

  await page.route('**/api/prompts', async route => {
    const request = route.request()

    if (request.method() === 'GET') {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify(prompts),
      })
      return
    }

    if (request.method() === 'POST') {
      const body = request.postDataJSON() as Omit<Prompt, 'id' | 'created_at'>
      const created: Prompt = {
        id: nextId,
        created_at: new Date().toISOString(),
        ...body,
      }
      nextId += 1
      prompts.unshift(created)

      await route.fulfill({
        status: 201,
        contentType: 'application/json',
        body: JSON.stringify(created),
      })
      return
    }

    await route.continue()
  })
}