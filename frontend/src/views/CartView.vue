<template>
  <div class="cart-wrapper">
    <div class="container">
      <h2 class="title">
      <i class="fa-solid fa-cart-shopping"></i> My Cart
      </h2>

      <!-- Loading -->
      <div v-if="loading" class="loading">Loading cart...</div>

      <!-- Cart Items -->
      <div v-else-if="cartItems.length">
        <div v-for="item in cartItems" :key="item.cart_id" class="cart-card">
          <img :src="item.image_url || '/placeholder.png'" class="cart-img" />
          <div class="details">
            <h3>{{ item.title }}</h3>
            <p class="seller">Seller: {{ item.seller_name || 'Unknown' }}</p>
            <p class="price">₱{{ Number(item.price).toLocaleString() }}</p>
          </div>
          <button @click="removeItem(item.cart_id)" class="remove-btn" title="Remove">✕</button>
        </div>

        <!-- Checkout Section -->
        <div class="checkout-section">
          <h3>Order Summary</h3>

          <div class="summary-row">
            <span>Items ({{ cartItems.length }})</span>
            <span>₱{{ total.toLocaleString() }}</span>
          </div>
          <div class="summary-row total-row">
            <span>Total</span>
            <span class="total-price">₱{{ total.toLocaleString() }}</span>
          </div>

          <div class="input-group">
            <label>Pickup Location</label>
            <select v-model="checkout.location">
              <option>Richards Hall Lobby</option>
              <option>University Gazebo</option>
              <option>O'Brien Library Entrance</option>
              <option>Dormitory Gate A</option>
            </select>
          </div>

          <div class="input-group">
            <label>Payment Method</label>
            <select v-model="checkout.payment">
              <option>Cash on Delivery</option>
              <option>GCash</option>
              <option>Bank Transfer</option>
            </select>
          </div>

          <button @click="processOrder" class="checkout-btn" :disabled="checkingOut">
            {{ checkingOut ? 'Processing...' : 'Place Order' }}
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <p>🛍️</p>
        <p>Your cart is empty</p>
        <button @click="router.push('/products')" class="browse-btn">Browse Marketplace</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const router = useRouter()
const cartItems = ref([])
const loading = ref(true)
const checkingOut = ref(false)
const user = JSON.parse(localStorage.getItem('user'))

const checkout = ref({
  location: 'Richards Hall Lobby',
  payment: 'Cash on Delivery'
})

const fetchCart = async () => {
  if (!user) return router.push('/auth')
  try {
    loading.value = true
    const res = await api.getCart(user.user_id)
    cartItems.value = Array.isArray(res.data) ? res.data : []
  } catch (err) {
    console.error('Cart fetch error:', err)
    cartItems.value = []
  } finally {
    loading.value = false
  }
}

const total = computed(() =>
  cartItems.value.reduce((sum, item) => sum + Number(item.price), 0)
)

const removeItem = async (id) => {
  try {
    await api.removeFromCart(id)
    cartItems.value = cartItems.value.filter(i => i.cart_id !== id)
  } catch (err) {
    console.error('Remove error:', err)
    alert('Failed to remove item ❌')
  }
}

const processOrder = async () => {
  try {
    checkingOut.value = true
    await api.checkout({
      user_id: user.user_id,
      total: total.value,
      location: checkout.value.location,
      payment: checkout.value.payment
    })
    alert('Order placed successfully! 🎉')
    cartItems.value = []
    router.push('/')
  } catch (err) {
    console.error('Checkout error:', err)
    alert(err.response?.data?.message || 'Checkout failed ❌')
  } finally {
    checkingOut.value = false
  }
}

onMounted(fetchCart)
</script>

<style scoped>
.cart-wrapper {
  background: #f8fafc;
  min-height: 100vh;
  padding: 2rem 1rem;
}

.container {
  max-width: 700px;
  margin: auto;
}

.title {
  color: #003366;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  border-left: 4px solid #FFD700;
  padding-left: 12px;
}

.loading {
  text-align: center;
  color: #888;
  padding: 3rem;
}

/* Cart Card */
.cart-card {
  display: flex;
  align-items: center;
  gap: 15px;
  background: white;
  padding: 15px;
  border-radius: 12px;
  margin-bottom: 12px;
  border: 0.5px solid #eee;
}

.cart-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  background: #f0f0f0;
}

.details {
  flex: 1;
}

.details h3 {
  margin: 0 0 4px;
  font-size: 1rem;
  color: #003366;
}

.seller {
  font-size: 0.8rem;
  color: #888;
  margin: 0 0 4px;
}

.price {
  color: #e74c3c;
  font-weight: 800;
  font-size: 1rem;
  margin: 0;
}

.remove-btn {
  background: none;
  border: 1px solid #eee;
  border-radius: 6px;
  padding: 6px 10px;
  font-size: 14px;
  cursor: pointer;
  color: #999;
  transition: 0.2s;
}

.remove-btn:hover {
  background: #fee;
  color: #e74c3c;
  border-color: #e74c3c;
}

/* Checkout */
.checkout-section {
  background: white;
  padding: 1.5rem;
  border-radius: 12px;
  margin-top: 1.5rem;
  border: 0.5px solid #eee;
}

.checkout-section h3 {
  color: #003366;
  margin: 0 0 1rem;
  font-size: 1.1rem;
}

.summary-row {
  display: flex;
  justify-content: space-between;
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 8px;
}

.total-row {
  border-top: 1px solid #eee;
  padding-top: 10px;
  margin-top: 4px;
  font-weight: 700;
  color: #003366;
}

.total-price {
  color: #e74c3c;
  font-size: 1.1rem;
}

.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-top: 1rem;
}

.input-group label {
  font-size: 0.8rem;
  font-weight: 700;
  color: #003366;
  text-transform: uppercase;
}

select {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 0.95rem;
  width: 100%;
}

.checkout-btn {
  width: 100%;
  background: #003366;
  color: white;
  padding: 14px;
  border: none;
  border-radius: 8px;
  font-weight: 800;
  font-size: 1rem;
  cursor: pointer;
  margin-top: 1.5rem;
  transition: 0.3s;
}

.checkout-btn:hover:not(:disabled) {
  background: #002244;
  transform: translateY(-2px);
}

.checkout-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 4rem;
  background: white;
  border-radius: 12px;
  color: #888;
}

.empty-state p:first-child {
  font-size: 3rem;
  margin-bottom: 0.5rem;
}

.browse-btn {
  margin-top: 1rem;
  background: #003366;
  color: white;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-weight: 700;
  cursor: pointer;
  transition: 0.3s;
}

.browse-btn:hover {
  background: #002244;
}
</style>