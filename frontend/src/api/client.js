const BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api/v1'

class ApiError extends Error {
  constructor(status, code, message, details = [], requestId = null) {
    super(message)
    this.name = 'ApiError'
    this.status = status
    this.code = code
    this.details = details
    this.requestId = requestId
  }
}

async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`
  const headers = {
    'Accept': 'application/json',
    ...(options.headers || {})
  }

  if (options.body && !(options.body instanceof FormData)) {
    headers['Content-Type'] = 'application/json'
  }

  try {
    const res = await fetch(url, {
      ...options,
      headers
    })

    if (res.status === 204) {
      return null
    }

    const data = await res.json().catch(() => ({}))

    if (!res.ok) {
      const err = data.error || {}
      throw new ApiError(
        res.status,
        err.code || 'HTTP_ERROR',
        err.message || `Terjadi kesalahan (HTTP ${res.status})`,
        err.details || [],
        err.request_id || null
      )
    }

    return data
  } catch (error) {
    if (error instanceof ApiError) {
      throw error
    }
    throw new ApiError(
      0,
      'NETWORK_ERROR',
      error.message || 'Gagal terhubung ke server backend.',
      [],
      null
    )
  }
}

export const api = {
  getTodos(params = {}) {
    const query = new URLSearchParams()
    Object.entries(params).forEach(([key, val]) => {
      if (val !== undefined && val !== null && val !== '') {
        query.append(key, val)
      }
    })
    const qs = query.toString() ? `?${query.toString()}` : ''
    return request(`/todos${qs}`, { method: 'GET' })
  },

  getTodo(id) {
    return request(`/todos/${id}`, { method: 'GET' })
  },

  createTodo(payload) {
    return request('/todos', {
      method: 'POST',
      body: JSON.stringify(payload)
    })
  },

  updateTodo(id, payload) {
    return request(`/todos/${id}`, {
      method: 'PATCH',
      body: JSON.stringify(payload)
    })
  },

  deleteTodo(id) {
    return request(`/todos/${id}`, {
      method: 'DELETE'
    })
  },

  bulkRandom(count = 1000) {
    return request('/todos/bulk-random', {
      method: 'POST',
      body: JSON.stringify({ count })
    })
  },

  getHealth() {
    return request('/health', { method: 'GET' })
  }
}
