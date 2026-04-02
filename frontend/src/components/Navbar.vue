<template>
  <nav class="navbar">
    <div class="nav-container">

      <!-- Logo -->
      <router-link to="/" class="brand">
        <span class="logo">🛍️</span>
        ADNU <span class="highlight">Market</span>
      </router-link>

      <!-- Links -->
      <div class="links">

        <router-link to="/products" class="nav-item">Market</router-link>
        <router-link to="/dashboard" class="nav-item">My Shop</router-link>

        <!-- Notifications -->
        <div class="notif" @click="toggleNotif">
          🔔
          <span v-if="notifications.length" class="badge">
            {{ notifications.length }}
          </span>

          <div v-if="showNotif" class="dropdown notif-dropdown">
            <p v-if="notifications.length === 0">No notifications</p>
            <p v-for="(n, i) in notifications" :key="i">{{ n }}</p>
          </div>
        </div>

        <!-- Cart -->
        <router-link to="/cart" class="cart-btn">
        <i class="fa-solid fa-cart-shopping"></i>
        <span v-if="cartCount > 0" class="cart-badge">
          {{ cartCount }}
        </span>
      </router-link>

        <!-- USER -->
        <div v-if="auth.user" class="user-wrapper">

          <div class="user-btn" @click="toggleMenu">
            👤 {{ auth.user.name || 'User' }}
          </div>

          <!-- DROPDOWN -->
          <div v-if="showMenu" class="dropdown">
            <router-link to="/profile">Profile</router-link>
            <router-link to="/add-product">Sell Item</router-link>
            <button @click="logout">Logout</button>
          </div>

        </div>

        <!-- LOGIN -->
        <router-link v-else to="/auth" class="login-btn">
          Login
        </router-link>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/services/api'

const auth = useAuthStore()

const cartCount = ref(0)
const showMenu = ref(false)
const showNotif = ref(false)

const notifications = ref([
  "New item added!",
  "Someone viewed your product"
])

// 🔥 load user
const loadUser = () => {
  const saved = localStorage.getItem('user')
  if (saved) auth.user = JSON.parse(saved)
}

// 🔥 fetch cart
const fetchCart = async () => {
  if (!auth.user) return

  try {
    const res = await api.getCart(auth.user.user_id)
    cartCount.value = res.data.length
  } catch (err) {
    console.error(err)
  }
}

// 🔥 toggle menu
const toggleMenu = () => {
  showMenu.value = !showMenu.value
}

// 🔥 toggle notif
const toggleNotif = () => {
  showNotif.value = !showNotif.value
}

// 🔥 logout
const logout = () => {
  localStorage.removeItem('user')
  auth.user = null
  cartCount.value = 0
}

// lifecycle
onMounted(async () => {
  loadUser()
  await fetchCart()
})
</script>

<style scoped>
.navbar {
  background: linear-gradient(90deg, #003366, #0055aa);
  color: white;
  padding: 10px 20px;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.brand {
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.highlight {
  color: #FFD700;
}

.links {
  display: flex;
  align-items: center;
  gap: 20px;
}

.nav-item {
  color: white;
  text-decoration: none;
}

.cart-btn, .notif {
  position: relative;
  cursor: pointer;
}

.badge {
  position: absolute;
  top: -5px;
  right: -10px;
  background: #FFD700;
  color: #003366;
  padding: 2px 6px;
  border-radius: 10px;
  font-size: 10px;
}

.user-wrapper {
  position: relative;
}

.user-btn {
  cursor: pointer;
  font-weight: bold;
}

.dropdown {
  position: absolute;
  top: 30px;
  right: 0;
  background: white;
  color: black;
  border-radius: 8px;
  padding: 10px;
  display: flex;
  flex-direction: column;
  min-width: 150px;
}

.dropdown a, .dropdown button {
  padding: 5px;
  text-align: left;
  border: none;
  background: none;
  cursor: pointer;
}

.dropdown a:hover, .dropdown button:hover {
  background: #f0f0f0;
}

.login-btn {
  background: #FFD700;
  color: #003366;
  padding: 5px 10px;
  border-radius: 5px;
  text-decoration: none;
}
</style>