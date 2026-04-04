<template>
  <div class="admin-wrapper">

    <!-- Login Gate -->
    <div v-if="!authenticated" class="admin-login">
      <div class="login-box">
        <h2>🔐 Admin Panel</h2>
        <p>ADNU Market — Staff Only</p>
        <input v-model="adminPassword" type="password" placeholder="Admin password" @keyup.enter="adminLogin" />
        <button @click="adminLogin">Access Dashboard</button>
        <p v-if="loginError" class="error-msg">{{ loginError }}</p>
      </div>
    </div>

    <!-- Dashboard -->
    <div v-else class="admin-dashboard">

      <!-- Header -->
      <div class="admin-header">
        <div class="admin-brand">
          <span>🛍️</span>
          <span>ADNU Market <strong>Admin</strong></span>
        </div>
        <div class="admin-nav">
          <button :class="{ active: tab === 'overview' }" @click="tab = 'overview'">Overview</button>
          <button :class="{ active: tab === 'products' }" @click="tab = 'products'; fetchProducts()">Products</button>
          <button :class="{ active: tab === 'users' }" @click="tab = 'users'; fetchUsers()">Users</button>
        </div>
        <button class="logout-admin" @click="authenticated = false">Logout</button>
      </div>

      <!-- OVERVIEW TAB -->
      <div v-if="tab === 'overview'" class="tab-content">
        <h2 class="tab-title">Overview</h2>
        <div class="stats-grid">
          <div class="stat-box">
            <i class="fa-solid fa-users"></i>
            <span class="stat-num">{{ stats.users ?? '...' }}</span>
            <span class="stat-label">Registered Users</span>
          </div>
          <div class="stat-box">
            <i class="fa-solid fa-box"></i>
            <span class="stat-num">{{ stats.products ?? '...' }}</span>
            <span class="stat-label">Total Listings</span>
          </div>
          <div class="stat-box">
            <i class="fa-solid fa-message"></i>
            <span class="stat-num">{{ stats.messages ?? '...' }}</span>
            <span class="stat-label">Messages Sent</span>
          </div>
          <div class="stat-box">
            <i class="fa-solid fa-cart-shopping"></i>
            <span class="stat-num">{{ stats.cart_items ?? '...' }}</span>
            <span class="stat-label">Cart Items</span>
          </div>
        </div>
      </div>

      <!-- PRODUCTS TAB -->
      <div v-if="tab === 'products'" class="tab-content">
        <div class="tab-header">
          <h2 class="tab-title">All Listings</h2>
          <input v-model="productSearch" class="search-input" placeholder="Search products..." />
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Title</th>
                <th>Category</th>
                <th>Price</th>
                <th>Status</th>
                <th>Seller</th>
                <th>Posted</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="p in filteredProducts" :key="p.id">
                <td>{{ p.id }}</td>
                <td class="title-cell">{{ p.title }}</td>
                <td><span class="cat-tag">{{ p.category }}</span></td>
                <td>₱{{ p.price.toLocaleString() }}</td>
                <td><span class="status-tag" :class="p.status.toLowerCase()">{{ p.status }}</span></td>
                <td>{{ p.seller_name }}</td>
                <td>{{ formatDate(p.created_at) }}</td>
                <td>
                  <button class="del-btn" @click="deleteProduct(p.id, p.title)">
                    <i class="fa-solid fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredProducts.length === 0">
                <td colspan="8" class="empty-row">No products found</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <!-- USERS TAB -->
      <div v-if="tab === 'users'" class="tab-content">
        <div class="tab-header">
          <h2 class="tab-title">All Users</h2>
          <input v-model="userSearch" class="search-input" placeholder="Search users..." />
        </div>
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Name</th>
                <th>Email</th>
                <th>Student ID</th>
                <th>Course</th>
                <th>Year</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="u in filteredUsers" :key="u.id">
                <td>{{ u.id }}</td>
                <td class="title-cell">{{ u.name }}</td>
                <td class="email-cell">{{ u.email }}</td>
                <td>{{ u.student_id }}</td>
                <td>{{ u.course }}</td>
                <td>{{ u.year_level }}</td>
                <td>
                  <button class="del-btn" @click="deleteUser(u.id, u.name)">
                    <i class="fa-solid fa-trash"></i>
                  </button>
                </td>
              </tr>
              <tr v-if="filteredUsers.length === 0">
                <td colspan="7" class="empty-row">No users found</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/services/api'
import axios from 'axios'

const BASE = 'http://127.0.0.1:5000/api'

const authenticated = ref(false)
const adminPassword = ref('')
const loginError = ref('')
const tab = ref('overview')

const stats = ref({})
const products = ref([])
const users = ref([])
const productSearch = ref('')
const userSearch = ref('')

const filteredProducts = computed(() =>
  products.value.filter(p =>
    p.title?.toLowerCase().includes(productSearch.value.toLowerCase()) ||
    p.seller_name?.toLowerCase().includes(productSearch.value.toLowerCase()) ||
    p.category?.toLowerCase().includes(productSearch.value.toLowerCase())
  )
)

const filteredUsers = computed(() =>
  users.value.filter(u =>
    u.name?.toLowerCase().includes(userSearch.value.toLowerCase()) ||
    u.email?.toLowerCase().includes(userSearch.value.toLowerCase()) ||
    u.student_id?.toLowerCase().includes(userSearch.value.toLowerCase())
  )
)

const adminLogin = async () => {
  try {
    await axios.post(`${BASE}/admin/login`, { password: adminPassword.value })
    authenticated.value = true
    loginError.value = ''
    fetchStats()
  } catch {
    loginError.value = 'Wrong password'
  }
}

const fetchStats = async () => {
  try {
    const res = await axios.get(`${BASE}/admin/stats`)
    stats.value = res.data
  } catch (e) {
    console.error(e)
  }
}

const fetchProducts = async () => {
  try {
    const res = await axios.get(`${BASE}/admin/products`)
    products.value = res.data
  } catch (e) {
    console.error(e)
  }
}

const fetchUsers = async () => {
  try {
    const res = await axios.get(`${BASE}/admin/users`)
    users.value = res.data
  } catch (e) {
    console.error(e)
  }
}

const deleteProduct = async (id, title) => {
  if (!confirm(`Delete "${title}"? This cannot be undone.`)) return
  try {
    await axios.delete(`${BASE}/admin/products/${id}`)
    products.value = products.value.filter(p => p.id !== id)
    stats.value.products = (stats.value.products || 1) - 1
  } catch {
    alert('Failed to delete product')
  }
}

const deleteUser = async (id, name) => {
  if (!confirm(`Delete user "${name}"? This will also delete their products, cart, and messages.`)) return
  try {
    await axios.delete(`${BASE}/admin/users/${id}`)
    users.value = users.value.filter(u => u.id !== id)
    stats.value.users = (stats.value.users || 1) - 1
  } catch {
    alert('Failed to delete user')
  }
}

const formatDate = (d) => d ? new Date(d).toLocaleDateString('en-PH', { month: 'short', day: 'numeric', year: 'numeric' }) : 'N/A'
</script>

<style scoped>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

* { box-sizing: border-box; }

.admin-wrapper {
  min-height: 100vh;
  background: #f1f5f9;
  font-family: 'Plus Jakarta Sans', sans-serif;
}

/* Login */
.admin-login {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #003366;
}

.login-box {
  background: white;
  border-radius: 16px;
  padding: 2.5rem;
  width: 340px;
  display: flex;
  flex-direction: column;
  gap: 1rem;
  text-align: center;
}

.login-box h2 { margin: 0; font-size: 1.4rem; color: #003366; }
.login-box p { margin: 0; color: #888; font-size: 0.875rem; }

.login-box input {
  padding: 11px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 9px;
  font-size: 0.9rem;
  outline: none;
  font-family: 'Plus Jakarta Sans', sans-serif;
}
.login-box input:focus { border-color: #003366; }

.login-box button {
  padding: 12px;
  background: #003366;
  color: white;
  border: none;
  border-radius: 9px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  font-family: 'Plus Jakarta Sans', sans-serif;
  transition: 0.2s;
}
.login-box button:hover { background: #002244; }

.error-msg { color: #e74c3c; font-size: 0.82rem; margin: 0; }

/* Header */
.admin-header {
  background: #003366;
  padding: 0 2rem;
  height: 58px;
  display: flex;
  align-items: center;
  gap: 2rem;
}

.admin-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  white-space: nowrap;
}
.admin-brand strong { color: #FFD700; }

.admin-nav { display: flex; gap: 4px; flex: 1; }

.admin-nav button {
  padding: 6px 16px;
  background: none;
  border: none;
  color: rgba(255,255,255,0.7);
  font-size: 0.875rem;
  font-weight: 600;
  cursor: pointer;
  border-radius: 6px;
  font-family: 'Plus Jakarta Sans', sans-serif;
  transition: 0.2s;
}
.admin-nav button:hover { background: rgba(255,255,255,0.1); color: white; }
.admin-nav button.active { background: rgba(255,255,255,0.15); color: white; }

.logout-admin {
  padding: 6px 14px;
  background: rgba(255,255,255,0.1);
  border: 1px solid rgba(255,255,255,0.2);
  color: rgba(255,255,255,0.8);
  border-radius: 6px;
  font-size: 0.8rem;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Plus Jakarta Sans', sans-serif;
  transition: 0.2s;
  white-space: nowrap;
}
.logout-admin:hover { background: rgba(255,255,255,0.2); }

/* Content */
.tab-content { max-width: 1200px; margin: 0 auto; padding: 2rem; }

.tab-title { font-size: 1.2rem; font-weight: 700; color: #003366; margin: 0 0 1.5rem; }

.tab-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
  gap: 1rem;
}

.search-input {
  padding: 8px 14px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 0.875rem;
  outline: none;
  width: 240px;
  font-family: 'Plus Jakarta Sans', sans-serif;
}
.search-input:focus { border-color: #003366; }

/* Stats */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
  gap: 16px;
}

.stat-box {
  background: white;
  border-radius: 14px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  border: 0.5px solid #e5e7eb;
  text-align: center;
}

.stat-box i { font-size: 1.5rem; color: #003366; }
.stat-num { font-size: 2rem; font-weight: 800; color: #003366; }
.stat-label { font-size: 0.8rem; color: #888; font-weight: 500; }

/* Table */
.table-wrap {
  background: white;
  border-radius: 14px;
  border: 0.5px solid #e5e7eb;
  overflow: hidden;
}

table { width: 100%; border-collapse: collapse; }

thead { background: #f8fafc; }

th {
  padding: 12px 14px;
  text-align: left;
  font-size: 0.72rem;
  font-weight: 700;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  border-bottom: 1px solid #e5e7eb;
}

td {
  padding: 11px 14px;
  font-size: 0.85rem;
  color: #333;
  border-bottom: 0.5px solid #f1f5f9;
}

tr:last-child td { border-bottom: none; }
tr:hover td { background: #fafafa; }

.title-cell { font-weight: 600; color: #003366; max-width: 200px; }
.email-cell { color: #555; max-width: 200px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

.cat-tag {
  background: #f0f4f8;
  color: #555;
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
}

.status-tag {
  font-size: 0.72rem;
  font-weight: 700;
  padding: 3px 8px;
  border-radius: 4px;
}
.status-tag.available { background: #f0fdf4; color: #16a34a; }
.status-tag.sold { background: #fff5f5; color: #e74c3c; }

.del-btn {
  background: #fff5f5;
  color: #e74c3c;
  border: none;
  padding: 6px 10px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: 0.2s;
}
.del-btn:hover { background: #e74c3c; color: white; }

.empty-row { text-align: center; color: #aaa; padding: 2rem; }
</style>