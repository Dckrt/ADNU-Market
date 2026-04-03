import axios from 'axios'

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
})

// 🔐 Attach user_id safely
apiClient.interceptors.request.use((config) => {
  try {
    const user = JSON.parse(localStorage.getItem('user'))
    if (user && user.user_id) {
      config.headers['X-User-ID'] = user.user_id
    }
  } catch (e) {
    console.warn('Invalid user in localStorage')
  }
  return config
})

// 🔥 Global error handler
apiClient.interceptors.response.use(
  (res) => res,
  (err) => {
    console.error('API Error:', err.response?.data || err.message)
    return Promise.reject(err)
  }
)

export default {
  // ================= AUTH ================= //
  register(userData) {
    return apiClient.post('/register', userData)
  },
  login(credentials) {
    return apiClient.post('/login', credentials)
  },
  // ================= PRODUCTS ================= //
  getProducts(params = {}) {
    return apiClient.get('/products', { params })
  },
  createProduct(productData) {
    return apiClient.post('/products', productData)
  },
  getProduct(id) {
    return apiClient.get(`/products/${id}`)
  },
  // ================= CART ================= //
  addToCart(data) {
    return apiClient.post('/cart', data)
  },
  getCart(userId) {
    return apiClient.get('/cart', {
      params: { user_id: userId }
    })
  },
  removeFromCart(id) {
    return apiClient.delete(`/cart/${id}`)
  },
  // ================= CHECKOUT ================= //
  checkout(data) {
    return apiClient.post('/checkout', data)
  },
  // ================= CHAT ================= //
  sendMessage(data) {
    return apiClient.post('/messages', data)
  },
  getMessages(sender_id, receiver_id) {
    return apiClient.get('/messages', {
      params: { sender_id, receiver_id }
    })
  },
  // ================= NOTIFICATIONS ================= //
  getNotifications(userId) {
    return apiClient.get('/notifications', {
      params: { user_id: userId }
    })
  },
  // ================= REVIEWS ================= //
  addReview(data) {
    return apiClient.post('/reviews', data)
  }
}