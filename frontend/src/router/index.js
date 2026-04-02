import { createRouter, createWebHistory } from 'vue-router'

import AuthPage from '@/views/AuthPage.vue'
import HomeView from '@/views/HomeView.vue'
import Marketplace from '@/views/Marketplace.vue'
import Dashboard from '@/views/Dashboard.vue'
import CartView from '@/views/CartView.vue'
import Profile from '@/views/Profile.vue'
import AddProduct from '@/views/AddProduct.vue'
import ProductDetails from '@/views/ProductDetails.vue'

const routes = [
  // 🔐 Auth
  { path: '/auth', name: 'Auth', component: AuthPage },

  // 🏠 Landing Page
  { path: '/', name: 'Home', component: HomeView },

  // 🛍️ Marketplace
  { path: '/products', name: 'Products', component: Marketplace },

  // 🔥 Product Details (dynamic)
  { path: '/products/:id', name: 'ProductDetails', component: ProductDetails, props: true },

  // 🛒 Cart
  { path: '/cart', name: 'Cart', component: CartView },

  // 👤 Profile
  { path: '/profile', name: 'Profile', component: Profile },

  // 🏪 Dashboard
  { path: '/dashboard', name: 'Dashboard', component: Dashboard },

  // ➕ Add Product
  { path: '/add-product', name: 'AddProduct', component: AddProduct },

  // ❗ Catch-all (fallback)
  { path: '/:pathMatch(.*)*', redirect: '/' }
]

const router = createRouter({
  history: createWebHistory(), // ✅ important for clean URLs
  routes
})

export default router