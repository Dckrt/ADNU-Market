<template>
  <div class="details-wrapper" v-if="product">
    <div class="container py-8">

      <!-- Back -->
      <button @click="$router.push('/products')" class="back-link">
        ← Back to Market
      </button>

      <div class="details-grid">

        <!-- PRODUCT -->
        <div class="ateneo-card main-info shadow-md">
          <div class="image-container">
            <img 
              :src="product.image_url || '/images/placeholder.png'" 
              class="main-img" 
            />
          </div>
          
          <div class="content-header mt-6">
            <div class="flex-between">
              <span class="badge available">{{ product.category }}</span>
              <StatusBadge :status="product.status" />
            </div>

            <h1 class="title">{{ product.title }}</h1>
            <p class="price">₱{{ formatPrice(product.price) }}</p>
          </div>

          <div class="description-section">
            <h3 class="section-label">Product Description</h3>
            <p class="description-text">{{ product.description }}</p>
          </div>

          <div class="metadata mt-6 pt-6 border-t">
            <p><strong>📍 Meet-up:</strong> {{ product.pickup_location || 'Campus Center' }}</p>
            <p><strong>📅 Posted:</strong> {{ formatDate(product.created_at) }}</p>
          </div>
        </div>

        <!-- SIDEBAR -->
        <div class="sidebar">
          <div class="ateneo-card seller-card shadow-md">

            <h3>Seller Info</h3>

            <div class="seller-profile">
              <div class="avatar">
                {{ product.seller_name?.charAt(0) || 'S' }}
              </div>

              <div>
                <p class="seller-name">
                  {{ product.seller_name || 'Ateneo Student' }}
                </p>

                <StarRating :rating="product.seller_rating || 0" />
              </div>
            </div>

            <!-- ACTIONS -->
            <div class="action-group">
              <button @click="handleBuyNow" class="btn-ateneo buy-now">
                Buy Now
              </button>

              <button @click="handleAddToCart" class="btn-outline add-cart">
                🛒 Add to Cart
              </button>
            </div>

            <p class="note">
              Meet only in safe campus areas like Richards Hall.
            </p>

          </div>
        </div>

      </div>
    </div>
  </div>

  <!-- LOADING -->
  <div v-else class="container py-20 text-center">
    <p>Loading product...</p>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/services/api'
import StatusBadge from '@/components/StatusBadge.vue'
import StarRating from '@/components/RatingStars.vue'

const route = useRoute()
const router = useRouter()

const product = ref(null)

// 🔥 LOAD PRODUCT
const loadDetails = async () => {
  try {
    const res = await api.getProduct(route.params.id)
    product.value = res.data

    window.scrollTo(0, 0)
  } catch (err) {
    console.error("Fetch error:", err)
  }
}

onMounted(loadDetails)
watch(() => route.params.id, loadDetails)

// 🔥 ADD TO CART
const handleAddToCart = async () => {
  const user = JSON.parse(localStorage.getItem('user'))

  if (!user) return router.push('/auth')

  try {
    await api.addToCart({
      user_id: user.user_id,
      product_id: product.value.id
    })

    alert("Added to cart!")
  } catch (err) {
    console.error(err)
    alert("Failed to add to cart")
  }
}

// 🔥 BUY NOW
const handleBuyNow = async () => {
  await handleAddToCart()
  router.push('/cart')
}

// HELPERS
const formatPrice = (v) =>
  parseFloat(v).toLocaleString(undefined, {
    minimumFractionDigits: 2
  })

const formatDate = (d) =>
  d ? new Date(d).toLocaleDateString() : 'N/A'
</script>

<style scoped>
.details-wrapper {
  background: #f8fafc;
  min-height: 100vh;
  padding: 30px;
}

.back-link {
  background: none;
  border: none;
  color: #003366;
  font-weight: bold;
  cursor: pointer;
  margin-bottom: 20px;
}

.details-grid {
  display: grid;
  grid-template-columns: 1.5fr 1fr;
  gap: 20px;
}

.main-img {
  width: 100%;
  height: 350px;
  object-fit: cover;
  border-radius: 10px;
}

.title {
  font-size: 2rem;
  font-weight: bold;
}

.price {
  font-size: 1.5rem;
  color: #ee4d2d;
  font-weight: bold;
}

.description-text {
  color: #555;
  line-height: 1.6;
}

.sidebar {
  position: sticky;
  top: 80px;
}

.seller-profile {
  display: flex;
  gap: 10px;
  margin: 20px 0;
}

.avatar {
  width: 40px;
  height: 40px;
  background: #003366;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-group {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.buy-now {
  background: #003366;
  color: white;
  padding: 10px;
  border-radius: 6px;
}

.add-cart {
  border: 2px solid #003366;
  background: white;
  padding: 10px;
  border-radius: 6px;
  cursor: pointer;
}

@media (max-width: 768px) {
  .details-grid {
    grid-template-columns: 1fr;
  }
}
</style>