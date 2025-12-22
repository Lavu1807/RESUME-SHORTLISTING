// API configuration and helper functions

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Small helper to add a timeout to fetch so the UI doesn't hang forever
async function fetchWithTimeout(input: RequestInfo | URL, init: RequestInit = {}, timeoutMs = 20000) {
  const controller = new AbortController()
  const id = setTimeout(() => controller.abort(), timeoutMs)
  try {
    return await fetch(input, { ...init, signal: controller.signal })
  } finally {
    clearTimeout(id)
  }
}

export interface ScoreResponse {
  score: number
  top_keywords: string[]
  skills_matched: string[]
  years_experience: number
  resume_char_count: number
  job_char_count: number
  method_used: string
  explanation?: string
}

export interface ScoreError {
  detail: string
}

/**
 * Send resume and job description to backend for scoring
 * @param resumeFile - The resume file (PDF or DOCX)
 * @param jobDescription - The job description text
 * @param useBert - Whether to use BERT for semantic matching (slower but more accurate)
 * @returns Promise with score response
 */
export async function scoreResume(
  resumeFile: File,
  jobDescription: string,
  useBert: boolean = false,
): Promise<ScoreResponse> {
  const formData = new FormData()
  formData.append("resume", resumeFile)
  formData.append("job_description", jobDescription)

  const url = new URL("/score", API_BASE_URL)
  if (useBert) {
    url.searchParams.append("use_bert", "true")
  }

  let response: Response
  try {
    response = await fetchWithTimeout(url.toString(), {
      method: "POST",
      body: formData,
    })
  } catch (e) {
    // Network/CORS/timeout errors surface here as TypeError / AbortError
    const base = typeof window !== "undefined" ? window.location.origin : "http://localhost:3000"
    const backend = API_BASE_URL
    const hint = `Could not reach backend at ${backend}. Make sure it's running and accessible from ${base}.`
    throw new Error(hint)
  }

  if (!response.ok) {
    // Try parsing JSON error, but fall back gracefully
    try {
      const error = (await response.json()) as ScoreError
      throw new Error(error.detail || `Request failed (${response.status})`)
    } catch {
      throw new Error(`Request failed (${response.status})`)
    }
  }

  return response.json() as Promise<ScoreResponse>
}

/**
 * Check backend health status
 */
export async function checkHealth(): Promise<boolean> {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/health`)
    return response.ok
  } catch {
    return false
  }
}

/**
 * Get config from backend (e.g., feature flags)
 */
export async function getConfig(): Promise<{ enable_gpt5: boolean }> {
  const response = await fetchWithTimeout(`${API_BASE_URL}/config`)
  if (!response.ok) {
    throw new Error("Failed to fetch config")
  }
  return response.json()
}
