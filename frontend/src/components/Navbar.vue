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

        <!-- Messages -->
        <router-link to="/messages" class="icon-btn" v-if="auth.user">
          <i class="fa-solid fa-message"></i>
          <span v-if="unreadCount > 0" class="badge">{{ unreadCount }}</span>
        </router-link>

        <!-- Notifications -->
        <div class="icon-btn notif" @click="toggleNotif" v-click-outside="() => showNotif = false">
          <i class="fa-solid fa-bell"></i>
          <span v-if="notifications.length" class="badge">{{ notifications.length }}</span>
          <div v-if="showNotif" class="dropdown notif-dropdown">
            <p class="dropdown-title">Notifications</p>
            <p v-if="notifications.length === 0" class="empty-notif">No notifications</p>
            <div v-for="(n, i) in notifications" :key="i" class="notif-item">{{ n }}</div>
          </div>
        </div>

        <!-- Cart -->
        <router-link to="/cart" class="icon-btn cart-btn">
          <i class="fa-solid fa-cart-shopping"></i>
          <span v-if="cartCount > 0" class="badge">{{ cartCount }}</span>
        </router-link>

        <!-- User Menu -->
        <div v-if="auth.user" class="user-wrapper" v-click-outside="() => showMenu = false">
          <div class="user-btn" @click="toggleMenu">
            <div class="avatar">{{ initials }}</div>
            <span class="user-name">{{ firstName }}</span>
            <i class="fa-solid fa-chevron-down chevron" :class="{ rotated: showMenu }"></i>
          </div>

          <div v-if="showMenu" class="dropdown user-dropdown">
            <div class="dropdown-header">
              <p class="dropdown-name">{{ auth.user.name }}</p>
              <p class="dropdown-email">{{ auth.user.email }}</p>
            </div>
            <div class="dropdown-divider"></div>
            <router-link to="/profile" @click="showMenu = false">
              <i class="fa-solid fa-user"></i> Profile
            </router-link>
            <router-link to="/dashboard" @click="showMenu = false">
              <i class="fa-solid fa-store"></i> My Shop
            </router-link>
            <router-link to="/messages" @click="showMenu = false">
              <i class="fa-solid fa-message"></i> Messages
            </router-link>
            <router-link to="/add-product" @click="showMenu = false">
              <i class="fa-solid fa-plus"></i> Sell Item
            </router-link>
            <div class="dropdown-divider"></div>
            <button @click="logout" class="logout-btn">
              <i class="fa-solid fa-right-from-bracket"></i> Logout
            </button>
          </div>
        </div>

        <!-- Login -->
        <router-link v-else to="/auth" class="login-btn">Login</router-link>

      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const auth = useAuthStore()
const router = useRouter()

const cartCount = ref(0)
const unreadCount = ref(0)
const showMenu = ref(false)
const showNotif = ref(false)
const notifications = ref([
  "New item added!",
  "Someone viewed your product"
])

const initials = computed(() => {
  if (!auth.user?.name) return '?'
  return auth.user.name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase()
})

const firstName = computed(() => {
  if (!auth.user?.name) return 'User'
  return auth.user.name.split(' ')[0]
})

const loadUser = () => {
  const saved = localStorage.getItem('user')
  if (saved) auth.user = JSON.parse(saved)
}

const fetchCart = async () => {
  if (!auth.user) return
  try {
    const res = await api.getCart(auth.user.user_id)
    cartCount.value = Array.isArray(res.data) ? res.data.length : 0
  } catch (err) {
    console.error(err)
  }
}

const fetchUnreadMessages = async () => {
  if (!auth.user) return
  try {
    const res = await api.getUnreadCount(auth.user.user_id)
    unreadCount.value = res.data?.count || 0
  } catch (err) {
    console.error(err)
  }
}

const toggleMenu = () => { showMenu.value = !showMenu.value }
const toggleNotif = () => { showNotif.value = !showNotif.value }

const logout = () => {
  localStorage.removeItem('user')
  auth.user = null
  cartCount.value = 0
  unreadCount.value = 0
  showMenu.value = false
  router.push('/auth')
}

const vClickOutside = {
  mounted(el, binding) {
    el._clickOutside = (e) => { if (!el.contains(e.target)) binding.value(e) }
    document.addEventListener('click', el._clickOutside)
  },
  unmounted(el) {
    document.removeEventListener('click', el._clickOutside)
  }
}

onMounted(async () => {
  loadUser()
  await fetchCart()
  await fetchUnreadMessages()
})
</script>

<style scoped>
.navbar {
  background: #003366;
  color: white;
  padding: 0 24px;
  height: 60px;
  position: sticky;
  top: 0;
  z-index: 999;
  box-shadow: 0 2px 12px rgba(0,0,0,0.15);
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  height: 100%;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

/* Brand */
.brand {
  font-weight: 800;
  font-size: 1.2rem;
  color: white;
  text-decoration: none;
  display: flex;
  align-items: center;
  gap: 6px;
}

.highlight { color: #FFD700; }

/* Links */
.links {
  display: flex;
  align-items: center;
  gap: 8px;
}

.nav-item {
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  font-size: 0.9rem;
  padding: 6px 12px;
  border-radius: 6px;
  transition: 0.2s;
}

.nav-item:hover,
.nav-item.router-link-active {
  color: white;
  background: rgba(255,255,255,0.12);
}

/* Icon Buttons */
.icon-btn {
  position: relative;
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 8px;
  color: rgba(255,255,255,0.85);
  cursor: pointer;
  transition: 0.2s;
  text-decoration: none;
}

.icon-btn:hover { background: rgba(255,255,255,0.12); color: white; }

/* Active state for messages icon */
.icon-btn.router-link-active {
  color: #FFD700;
  background: rgba(255,255,255,0.12);
}

.badge {
  position: absolute;
  top: -4px;
  right: -4px;
  background: #FFD700;
  color: #003366;
  font-size: 10px;
  font-weight: 800;
  min-width: 16px;
  height: 16px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0 3px;
}

/* User Button */
.user-wrapper { position: relative; }

.user-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  padding: 5px 10px;
  border-radius: 8px;
  transition: 0.2s;
}

.user-btn:hover { background: rgba(255,255,255,0.12); }

.avatar {
  width: 30px;
  height: 30px;
  background: #FFD700;
  color: #003366;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  font-weight: 800;
}

.user-name {
  font-size: 0.9rem;
  font-weight: 600;
  color: white;
}

.chevron {
  font-size: 10px;
  color: rgba(255,255,255,0.7);
  transition: transform 0.2s;
}

.chevron.rotated { transform: rotate(180deg); }

/* Dropdowns */
.dropdown {
  position: absolute;
  top: calc(100% + 10px);
  right: 0;
  background: white;
  color: #333;
  border-radius: 10px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.15);
  min-width: 200px;
  overflow: hidden;
  z-index: 1000;
}

.dropdown-header {
  padding: 12px 16px;
  background: #f8fafc;
}

.dropdown-name {
  font-weight: 700;
  font-size: 0.9rem;
  color: #003366;
  margin: 0 0 2px;
}

.dropdown-email {
  font-size: 0.75rem;
  color: #888;
  margin: 0;
}

.dropdown-divider {
  height: 1px;
  background: #eee;
}

.dropdown a,
.dropdown button {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 16px;
  font-size: 0.875rem;
  color: #333;
  text-decoration: none;
  border: none;
  background: none;
  width: 100%;
  text-align: left;
  cursor: pointer;
  transition: 0.15s;
}

.dropdown a:hover,
.dropdown button:hover {
  background: #f0f4ff;
  color: #003366;
}

.dropdown i { width: 14px; color: #888; }

.logout-btn { color: #e74c3c !important; }
.logout-btn i { color: #e74c3c !important; }
.logout-btn:hover { background: #fff5f5 !important; }

/* Notif Dropdown */
.notif-dropdown { min-width: 260px; }

.dropdown-title {
  font-weight: 700;
  font-size: 0.85rem;
  color: #003366;
  padding: 12px 16px 8px;
  margin: 0;
  border-bottom: 1px solid #eee;
}

.notif-item {
  padding: 10px 16px;
  font-size: 0.85rem;
  color: #444;
  border-bottom: 1px solid #f5f5f5;
}

.empty-notif {
  padding: 16px;
  text-align: center;
  color: #aaa;
  font-size: 0.85rem;
  margin: 0;
}

/* Login Button */
.login-btn {
  background: #FFD700;
  color: #003366;
  padding: 7px 16px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.875rem;
  text-decoration: none;
  transition: 0.2s;
}

.login-btn:hover { background: #e6c200; }
</style>