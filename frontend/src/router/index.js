import { createRouter, createWebHistory } from 'vue-router';

import AuthPage from '@/views/AuthPage.vue';
import HomeView from '@/views/HomeView.vue';
import Marketplace from '@/views/Marketplace.vue';
import Dashboard from '@/views/Dashboard.vue';
import CartView from '@/views/CartView.vue';
import Profile from '@/views/Profile.vue';
import AddProduct from '@/views/AddProduct.vue';
import ProductDetails from '@/views/ProductDetails.vue'; // 🔥 ADD THIS

const routes = [
  // 🔐 Auth
  { path: '/auth', component: AuthPage },

  // 🏠 Landing Page
  { path: '/', component: HomeView },

  // 🛍️ Marketplace
  { path: '/products', component: Marketplace },

  // 🔥 PRODUCT DETAILS (IMPORTANT)
  { path: '/products/:id', component: ProductDetails },

  // 🛒 Cart
  { path: '/cart', component: CartView },

  // 👤 Profile
  { path: '/profile', component: Profile },

  // 🏪 Seller Dashboard
  { path: '/dashboard', component: Dashboard },

  // ➕ Add Product
  { path: '/add-product', component: AddProduct },

  // ❗ Catch-all
  { path: '/:pathMatch(.*)*', redirect: '/' }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;