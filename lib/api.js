const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

// Adds a timeout to fetch so the UI doesn't hang indefinitely
async function fetchWithTimeout(input, init = {}, timeoutMs = 20000) {
  const controller = new AbortController()
  const id = setTimeout(() => controller.abort(), timeoutMs)
  try {
    return await fetch(input, { ...init, signal: controller.signal })
  } finally {
    clearTimeout(id)
  }
}

export async function scoreResume(resumeFile, jobDescription, useBert = false) {
  const formData = new FormData()
  formData.append("resume", resumeFile)
  formData.append("job_description", jobDescription)

  const url = new URL("/score", API_BASE_URL)
  if (useBert) {
    url.searchParams.append("use_bert", "true")
  }

  let response
  try {
    response = await fetchWithTimeout(url.toString(), {
      method: "POST",
      body: formData,
    })
  } catch (e) {
    const base = typeof window !== "undefined" ? window.location.origin : "http://localhost:3000"
    const backend = API_BASE_URL
    const hint = `Could not reach backend at ${backend}. Make sure it's running and accessible from ${base}.`
    throw new Error(hint)
  }

  if (!response.ok) {
    try {
      const error = await response.json()
      throw new Error(error.detail || `Request failed (${response.status})`)
    } catch {
      throw new Error(`Request failed (${response.status})`)
    }
  }

  return response.json()
}

export async function checkHealth() {
  try {
    const response = await fetchWithTimeout(`${API_BASE_URL}/health`)
    return response.ok
  } catch {
    return false
  }
}

export async function getConfig() {
  const response = await fetchWithTimeout(`${API_BASE_URL}/config`)
  if (!response.ok) {
    throw new Error("Failed to fetch config")
  }
  return response.json()
}
