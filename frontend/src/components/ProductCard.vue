<template>
  <div class="card">
    
    <!-- Category & Status -->
    <div class="category-header">
      <span class="category-tag">{{ product.category }}</span>
      <StatusBadge :status="product.status" />
    </div>

    <!-- Product Image -->
    <div class="image-container">
      <img 
        :src="getImage(product.image_url)" 
        :alt="product.title"
        class="product-image"
      />
    </div>

    <!-- Content -->
    <div class="card-body">
      <h3 class="product-title">{{ product.title }}</h3>
      <p class="product-desc">{{ product.description }}</p>
      <p class="price">₱{{ formatPrice(product.price) }}</p>
      
      <!-- Buttons -->
      <div class="button-group">
        <button 
          @click="handleAddToCart" 
          class="cart-btn"
          :disabled="product.status !== 'Available'"
        >
          <i class="fa-solid fa-cart-shopping"></i>
        </button>

        <button 
          @click="handleBuyNow" 
          class="buy-btn"
          :disabled="product.status !== 'Available'"
        >
          Buy Now
        </button>
      </div>

      <router-link :to="'/products/' + product.id" class="details-link">
        View Details
      </router-link>
    </div>
  </div>
</template>

<script setup>
import StatusBadge from './StatusBadge.vue'
import api from '@/services/api'
import { useRouter } from 'vue-router'

const props = defineProps(['product'])
const router = useRouter()

const formatPrice = (value) => {
  return parseFloat(value).toLocaleString(undefined, { minimumFractionDigits: 2 })
}

// 🔥 IMAGE HANDLER (PNG support)
const getImage = (url) => {
  if (!url) return '/placeholder-image.png'

  // if local image (like /images/item.png)
  if (url.startsWith('/')) return url

  // if base64 or external
  return url
}

// 🔥 ADD TO CART FIX
const handleAddToCart = async () => {
  const user = JSON.parse(localStorage.getItem('user'))
  if (!user) return router.push('/auth')

  try {
    await api.addToCart({
      user_id: user.user_id,
      product_id: props.product.id
    })

    alert(`${props.product.title} added to cart!`)
  } catch (err) {
    alert("Failed to add to cart")
  }
}

const handleBuyNow = () => {
  router.push('/products/' + props.product.id)
}
</script>

<style scoped>
.card {
  background: white;
  border-radius: 12px;
  padding: 1rem;
  transition: 0.2s;
}

.card:hover {
  transform: translateY(-5px);
}

/* HEADER */
.category-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 8px;
}

.category-tag {
  font-size: 0.65rem;
  font-weight: bold;
  background: #f0f4f8;
  padding: 4px 8px;
  border-radius: 4px;
}

/* IMAGE */
.image-container {
  height: 160px;
  overflow: hidden;
  border-radius: 8px;
}

.product-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* TEXT */
.product-title {
  font-size: 1rem;
  font-weight: bold;
}

.product-desc {
  font-size: 0.85rem;
  color: #666;
  margin-bottom: 10px;
}

.price {
  color: #ee4d2d;
  font-weight: bold;
}

/* BUTTONS */
.button-group {
  display: flex;
  gap: 8px;
}

.cart-btn {
  width: 40px;
  height: 40px;
  border-radius: 6px;
  border: none;
  background: #f1f5f9;
  cursor: pointer;
}

.cart-btn i {
  font-size: 16px;
}

.buy-btn {
  flex: 1;
  background: #003366;
  color: white;
  border-radius: 6px;
}

.buy-btn:hover {
  background: #002244;
}

/* LINK */
.details-link {
  font-size: 0.8rem;
  text-align: center;
  display: block;
  margin-top: 8px;
}
</style>