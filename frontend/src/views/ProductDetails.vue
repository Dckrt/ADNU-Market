<template>
  <div v-if="product" class="details-wrapper">
    <div class="container">

      <!-- Back -->
      <button @click="$router.push('/products')" class="back-link">
        <i class="fa-solid fa-arrow-left"></i> Back to Market
      </button>

      <div class="details-grid">

        <!-- LEFT: Product Info -->
        <div class="product-main">

          <!-- Image -->
          <div class="image-box">
            <img :src="product.image_url || '/placeholder.png'" class="main-img" :alt="product.title" />
            <span class="cat-badge">{{ product.category }}</span>
          </div>

          <!-- Info -->
          <div class="product-info">
            <div class="status-row">
              <span class="status-dot">● Available</span>
              <span class="posted-date">Posted {{ formatDate(product.created_at) }}</span>
            </div>

            <h1 class="product-title">{{ product.title }}</h1>
            <p class="product-price">₱{{ formatPrice(product.price) }}</p>

            <div class="divider"></div>

            <h3 class="section-label">Description</h3>
            <p class="product-desc">{{ product.description || 'No description provided.' }}</p>
          </div>
        </div>

        <!-- RIGHT: Seller + Actions -->
        <div class="sidebar">

          <!-- Seller Card -->
          <div class="seller-card">
            <p class="card-label">Sold by</p>
            <div class="seller-row">
              <div class="seller-avatar">{{ product.seller_name?.charAt(0)?.toUpperCase() || 'S' }}</div>
              <div>
                <p class="seller-name">{{ product.seller_name || 'ADNU Student' }}</p>
                <p class="seller-sub">ADNU Verified Student</p>
              </div>
            </div>
          </div>

          <!-- Action Card -->
          <div class="action-card">
            <p class="price-display">₱{{ formatPrice(product.price) }}</p>

            <button
              @click="handleBuyNow"
              class="btn-buy"
              :disabled="isOwnProduct"
            >
              <i class="fa-solid fa-bolt"></i>
              {{ isOwnProduct ? 'Your Listing' : 'Buy Now' }}
            </button>

            <button
              @click="handleAddToCart"
              class="btn-cart"
              :disabled="isOwnProduct || addingToCart"
            >
              <i class="fa-solid fa-cart-shopping"></i>
              {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
            </button>

            <button @click="handleChat" class="btn-chat">
              <i class="fa-solid fa-comment-dots"></i>
              Chat with Seller
            </button>

            <p class="safety-note">
              <i class="fa-solid fa-shield-halved"></i>
              Meet in safe campus areas only
            </p>
          </div>

        </div>
      </div>
    </div>
  </div>

  <!-- Loading -->
  <div v-else class="loading-wrapper">
    <div class="loading-card">
      <div class="skeleton img-skeleton"></div>
      <div class="skeleton title-skeleton"></div>
      <div class="skeleton price-skeleton"></div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const router = useRouter()

const product = ref(null)
const addingToCart = ref(false)
const currentUser = JSON.parse(localStorage.getItem('user'))

const isOwnProduct = computed(() =>
  currentUser && product.value && product.value.seller_id === currentUser.user_id
)

const loadDetails = async () => {
  product.value = null
  try {
    const res = await api.getProduct(route.params.id)
    product.value = res.data
    window.scrollTo(0, 0)
  } catch (err) {
    console.error('Fetch error:', err)
  }
}

onMounted(loadDetails)
watch(() => route.params.id, loadDetails)

const handleAddToCart = async () => {
  if (!currentUser) return router.push('/auth')
  if (isOwnProduct.value) return alert('You cannot add your own product to cart.')
  try {
    addingToCart.value = true
    await api.addToCart({ user_id: currentUser.user_id, product_id: product.value.id })
    alert(`"${product.value.title}" added to cart! ✅`)
  } catch (err) {
    const msg = err.response?.data?.message || 'Failed to add to cart'
    alert(msg + ' ❌')
  } finally {
    addingToCart.value = false
  }
}

const handleBuyNow = async () => {
  if (!currentUser) return router.push('/auth')
  if (isOwnProduct.value) return
  await handleAddToCart()
  router.push('/cart')
}

const handleChat = () => {
  if (!currentUser) return router.push('/auth')
  if (isOwnProduct.value) return alert('This is your own listing.')
  router.push({
    path: '/chat',
    query: {
      seller_id: product.value.seller_id,
      seller_name: product.value.seller_name
    }
  })
}

const formatPrice = (v) =>
  parseFloat(v).toLocaleString(undefined, { minimumFractionDigits: 2 })

const formatDate = (d) =>
  d ? new Date(d).toLocaleDateString('en-PH', { month: 'short', day: 'numeric', year: 'numeric' }) : 'N/A'
</script>

<style scoped>
.details-wrapper {
  background: #f8fafc;
  min-height: 100vh;
  padding: 2rem 1.5rem;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
}

.back-link {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: #003366;
  font-weight: 700;
  font-size: 0.875rem;
  cursor: pointer;
  margin-bottom: 1.5rem;
  padding: 0;
  transition: 0.2s;
}
.back-link:hover { opacity: 0.7; }

.details-grid {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 1.5rem;
  align-items: start;
}

/* LEFT */
.product-main {
  background: white;
  border-radius: 16px;
  border: 0.5px solid #eee;
  overflow: hidden;
}

.image-box {
  position: relative;
  height: 340px;
  background: #f1f5f9;
}

.main-img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.cat-badge {
  position: absolute;
  top: 14px;
  left: 14px;
  background: white;
  color: #003366;
  font-size: 0.75rem;
  font-weight: 700;
  padding: 5px 12px;
  border-radius: 20px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}

.product-info { padding: 1.5rem; }

.status-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.75rem;
}

.status-dot {
  font-size: 0.78rem;
  font-weight: 700;
  color: #16a34a;
}

.posted-date {
  font-size: 0.78rem;
  color: #888;
}

.product-title {
  font-size: 1.6rem;
  font-weight: 800;
  color: #003366;
  margin: 0 0 0.5rem;
  line-height: 1.3;
}

.product-price {
  font-size: 1.5rem;
  font-weight: 800;
  color: #e74c3c;
  margin: 0 0 1rem;
}

.divider {
  height: 1px;
  background: #f1f5f9;
  margin: 1rem 0;
}

.section-label {
  font-size: 0.82rem;
  font-weight: 700;
  color: #003366;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 0.5rem;
}

.product-desc {
  color: #555;
  line-height: 1.7;
  font-size: 0.9rem;
  margin: 0;
}

/* RIGHT SIDEBAR */
.sidebar {
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: sticky;
  top: 80px;
}

.seller-card {
  background: white;
  border-radius: 14px;
  border: 0.5px solid #eee;
  padding: 1.25rem;
}

.card-label {
  font-size: 0.72rem;
  font-weight: 700;
  color: #888;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 0.75rem;
}

.seller-row {
  display: flex;
  align-items: center;
  gap: 12px;
}

.seller-avatar {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #003366;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1rem;
  flex-shrink: 0;
}

.seller-name {
  font-size: 0.95rem;
  font-weight: 700;
  color: #003366;
  margin: 0 0 2px;
}

.seller-sub {
  font-size: 0.75rem;
  color: #16a34a;
  margin: 0;
}

/* Action Card */
.action-card {
  background: white;
  border-radius: 14px;
  border: 0.5px solid #eee;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.price-display {
  font-size: 1.4rem;
  font-weight: 800;
  color: #e74c3c;
  margin: 0 0 4px;
}

.btn-buy {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  background: #003366;
  color: white;
  border: none;
  padding: 13px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 0.95rem;
  cursor: pointer;
  transition: 0.2s;
}
.btn-buy:hover:not(:disabled) { background: #002244; transform: translateY(-1px); }
.btn-buy:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-cart {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  background: #FFD700;
  color: #003366;
  border: none;
  padding: 13px;
  border-radius: 10px;
  font-weight: 800;
  font-size: 0.95rem;
  cursor: pointer;
  transition: 0.2s;
}
.btn-cart:hover:not(:disabled) { background: #e6c200; transform: translateY(-1px); }
.btn-cart:disabled { opacity: 0.5; cursor: not-allowed; }

.btn-chat {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  width: 100%;
  background: white;
  color: #003366;
  border: 1.5px solid #003366;
  padding: 12px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: 0.2s;
}
.btn-chat:hover { background: #f0f4ff; }

.safety-note {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: #888;
  margin: 4px 0 0;
}

.safety-note i { color: #16a34a; }

/* Loading */
.loading-wrapper {
  background: #f8fafc;
  min-height: 100vh;
  padding: 2rem;
  display: flex;
  justify-content: center;
}

.loading-card {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  width: 100%;
  max-width: 600px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton {
  background: #e8ecef;
  border-radius: 6px;
  animation: pulse 1.5s infinite;
}

.img-skeleton { height: 280px; border-radius: 12px; }
.title-skeleton { height: 24px; width: 70%; }
.price-skeleton { height: 20px; width: 30%; }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@media (max-width: 768px) {
  .details-grid { grid-template-columns: 1fr; }
  .sidebar { position: static; }
}
</style>