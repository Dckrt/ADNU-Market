<template>
  <div v-if="product" class="details-wrapper">
    <div class="container">

      <!-- Breadcrumb -->
      <div class="breadcrumb">
        <button @click="$router.push('/')" class="crumb">Home</button>
        <span class="crumb-sep">/</span>
        <button @click="$router.push('/products')" class="crumb">Market</button>
        <span class="crumb-sep">/</span>
        <span class="crumb active">{{ product.title }}</span>
      </div>

      <div class="details-grid">

        <!-- LEFT -->
        <div class="left-col">

          <!-- Image -->
          <div class="image-box">
            <img :src="product.image_url || '/placeholder.png'" class="main-img" :alt="product.title" />
            <span class="cat-badge">{{ product.category }}</span>
          </div>

          <!-- Description Card -->
          <div class="desc-card">
            <h3 class="section-label">
              <i class="fa-solid fa-align-left"></i> Product Description
            </h3>
            <p class="product-desc">{{ product.description || 'No description provided.' }}</p>

            <div class="meta-row">
              <div class="meta-item">
                <i class="fa-solid fa-tag"></i>
                <span>{{ product.category }}</span>
              </div>
              <div class="meta-item">
                <i class="fa-solid fa-calendar-days"></i>
                <span>Posted {{ formatDate(product.created_at) }}</span>
              </div>
              <div class="meta-item">
                <i class="fa-solid fa-circle-check" style="color:#16a34a"></i>
                <span style="color:#16a34a">Available</span>
              </div>
            </div>
          </div>

        </div>

        <!-- RIGHT -->
        <div class="right-col">

          <!-- Product Header -->
          <div class="product-header-card">
            <h1 class="product-title">{{ product.title }}</h1>
            <p class="product-price">₱{{ formatPrice(product.price) }}</p>
          </div>

          <!-- Seller Card -->
          <div class="seller-card">
            <p class="card-label"><i class="fa-solid fa-store"></i> Sold by</p>
            <div class="seller-row">
              <div class="seller-avatar">
                {{ product.seller_name?.charAt(0)?.toUpperCase() || 'S' }}
              </div>
              <div>
                <p class="seller-name">{{ product.seller_name || 'ADNU Student' }}</p>
                <p class="seller-sub">
                  <i class="fa-solid fa-circle-check"></i> ADNU Verified Student
                </p>
              </div>
              <button
                v-if="!isOwnProduct"
                @click="handleChat"
                class="chat-quick-btn"
                title="Message Seller"
              >
                <i class="fa-solid fa-comment-dots"></i>
              </button>
            </div>
          </div>

          <!-- Action Card -->
          <div class="action-card">

            <div v-if="isOwnProduct" class="own-listing-banner">
              <i class="fa-solid fa-store"></i>
              This is your listing
            </div>

            <template v-else>
              <button @click="handleAddToCart" class="btn-cart" :disabled="addingToCart">
                <i class="fa-solid fa-cart-shopping"></i>
                {{ addingToCart ? 'Adding...' : 'Add to Cart' }}
              </button>

              <button @click="handleChat" class="btn-chat">
                <i class="fa-solid fa-comment-dots"></i>
                Chat with Seller
              </button>
            </template>

            <p class="safety-note">
              <i class="fa-solid fa-shield-halved"></i>
              Arrange meetup details through chat
            </p>
          </div>

        </div>
      </div>
    </div>
  </div>

  <!-- Loading -->
  <div v-else class="loading-wrapper">
    <div class="container">
      <div class="loading-grid">
        <div class="skeleton img-sk"></div>
        <div class="loading-right">
          <div class="skeleton title-sk"></div>
          <div class="skeleton price-sk"></div>
          <div class="skeleton btn-sk"></div>
          <div class="skeleton btn-sk"></div>
        </div>
      </div>
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
  try {
    addingToCart.value = true
    await api.addToCart({ user_id: currentUser.user_id, product_id: product.value.id })
    alert(`"${product.value.title}" added to cart! ✅`)
  } catch (err) {
    alert((err.response?.data?.message || 'Failed to add to cart') + ' ❌')
  } finally {
    addingToCart.value = false
  }
}

const handleChat = () => {
  if (!currentUser) return router.push('/auth')
  router.push({
    path: '/messages',
    query: { seller_id: product.value.seller_id, seller_name: product.value.seller_name }
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
  padding: 1.5rem;
}

.container { max-width: 1100px; margin: 0 auto; }

/* Breadcrumb */
.breadcrumb {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 1.5rem;
  font-size: 0.82rem;
}

.crumb {
  background: none;
  border: none;
  color: #003366;
  cursor: pointer;
  font-weight: 600;
  padding: 0;
  font-size: 0.82rem;
}

.crumb:hover { text-decoration: underline; }
.crumb.active { color: #888; cursor: default; font-weight: 400; }
.crumb.active:hover { text-decoration: none; }
.crumb-sep { color: #ccc; }

/* Grid */
.details-grid {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 1.5rem;
  align-items: start;
}

/* LEFT */
.left-col { display: flex; flex-direction: column; gap: 16px; }

.image-box {
  position: relative;
  height: 380px;
  background: #f1f5f9;
  border-radius: 16px;
  overflow: hidden;
  border: 0.5px solid #eee;
}

.main-img { width: 100%; height: 100%; object-fit: cover; }

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

.desc-card {
  background: white;
  border-radius: 14px;
  border: 0.5px solid #eee;
  padding: 1.25rem;
}

.section-label {
  font-size: 0.85rem;
  font-weight: 700;
  color: #003366;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  margin: 0 0 0.75rem;
  display: flex;
  align-items: center;
  gap: 7px;
}

.product-desc {
  color: #555;
  line-height: 1.7;
  font-size: 0.9rem;
  margin: 0 0 1rem;
}

.meta-row {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  padding-top: 0.75rem;
  border-top: 1px solid #f1f5f9;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8rem;
  color: #666;
}

.meta-item i { color: #003366; font-size: 0.75rem; }

/* RIGHT */
.right-col {
  display: flex;
  flex-direction: column;
  gap: 12px;
  position: sticky;
  top: 80px;
}

.product-header-card {
  background: white;
  border-radius: 14px;
  border: 0.5px solid #eee;
  padding: 1.25rem;
}

.product-title {
  font-size: 1.4rem;
  font-weight: 800;
  color: #003366;
  margin: 0 0 8px;
  line-height: 1.3;
}

.product-price {
  font-size: 1.6rem;
  font-weight: 800;
  color: #e74c3c;
  margin: 0;
}

/* Seller */
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
  display: flex;
  align-items: center;
  gap: 6px;
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
  margin: 0 0 3px;
}

.seller-sub {
  font-size: 0.75rem;
  color: #16a34a;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 4px;
}

.chat-quick-btn {
  margin-left: auto;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #f0f4ff;
  color: #003366;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  transition: 0.2s;
  flex-shrink: 0;
}
.chat-quick-btn:hover { background: #003366; color: white; }

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

.own-listing-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  background: #f0f4ff;
  color: #003366;
  font-size: 0.875rem;
  font-weight: 700;
  padding: 12px 16px;
  border-radius: 10px;
  border: 1px solid #d0ddf5;
}

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
  background: #003366;
  color: white;
  border: none;
  padding: 13px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: 0.2s;
}
.btn-chat:hover { background: #002244; transform: translateY(-1px); }

.safety-note {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.75rem;
  color: #aaa;
  margin: 2px 0 0;
}
.safety-note i { color: #16a34a; }

/* Loading */
.loading-wrapper {
  background: #f8fafc;
  min-height: 100vh;
  padding: 1.5rem;
}

.loading-grid {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 1.5rem;
}

.loading-right {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.skeleton {
  background: #e8ecef;
  border-radius: 10px;
  animation: pulse 1.5s infinite;
}

.img-sk { height: 380px; }
.title-sk { height: 28px; width: 80%; }
.price-sk { height: 32px; width: 40%; }
.btn-sk { height: 48px; border-radius: 10px; }

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

@media (max-width: 768px) {
  .details-grid, .loading-grid { grid-template-columns: 1fr; }
  .right-col { position: static; }
}
</style>