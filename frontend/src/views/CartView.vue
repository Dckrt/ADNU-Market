<template>
  <div class="cart-wrapper">
    <div class="cart-container">

      <!-- Header -->
      <div class="page-header">
        <div class="header-left">
          <i class="fa-solid fa-cart-shopping header-icon"></i>
          <div>
            <h1 class="page-title">My Cart</h1>
            <p class="page-sub" v-if="cartItems.length">{{ cartItems.length }} item{{ cartItems.length > 1 ? 's' : '' }} ready for pickup</p>
          </div>
        </div>
        <router-link to="/products" class="continue-link">
          <i class="fa-solid fa-arrow-left"></i> Continue Shopping
        </router-link>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="loading-state">
        <div class="spinner"></div>
        <p>Loading your cart...</p>
      </div>

      <!-- Cart Layout -->
      <div v-else-if="cartItems.length" class="cart-layout">

        <!-- Items -->
        <div class="items-col">
          <TransitionGroup name="cart-item" tag="div">
            <div v-for="item in cartItems" :key="item.cart_id" class="cart-card">
              <div class="card-img-wrap">
                <img :src="item.image_url || '/placeholder.png'" class="cart-img" />
                <span class="category-badge" v-if="item.category">{{ item.category }}</span>
              </div>

              <div class="card-body">
                <div class="card-top">
                  <h3 class="item-title">{{ item.title }}</h3>
                  <button @click="removeItem(item.cart_id)" class="remove-btn" title="Remove item">
                    <i class="fa-solid fa-xmark"></i>
                  </button>
                </div>

                <p class="item-seller">
                  <i class="fa-solid fa-store"></i>
                  {{ item.seller_name || 'Ateneo Student' }}
                </p>

                <div class="card-bottom">
                  <span class="item-price">₱{{ Number(item.price).toLocaleString('en-PH', { minimumFractionDigits: 2 }) }}</span>
                  <span class="item-status">
                    <i class="fa-solid fa-circle-check"></i> Available
                  </span>
                </div>
              </div>
            </div>
          </TransitionGroup>
        </div>

        <!-- Order Summary -->
        <div class="summary-col">
          <div class="summary-card">
            <h3 class="summary-title">Order Summary</h3>

            <div class="summary-lines">
              <div class="summary-line" v-for="item in cartItems" :key="'s-' + item.cart_id">
                <span class="summary-item-name">{{ item.title }}</span>
                <span>₱{{ Number(item.price).toLocaleString('en-PH', { minimumFractionDigits: 2 }) }}</span>
              </div>
            </div>

            <div class="summary-divider"></div>

            <div class="summary-total">
              <span>Total</span>
              <span class="total-amount">₱{{ total.toLocaleString('en-PH', { minimumFractionDigits: 2 }) }}</span>
            </div>

            <!-- Pickup Location -->
            <div class="input-group">
              <label><i class="fa-solid fa-location-dot"></i> Pickup Location</label>
              <div class="select-wrap">
                <select v-model="checkout.location">
                  <option>Richards Hall Lobby</option>
                  <option>University Gazebo</option>
                  <option>O'Brien Library Entrance</option>
                  <option>Dormitory Gate A</option>
                </select>
                <i class="fa-solid fa-chevron-down select-arrow"></i>
              </div>
            </div>

            <!-- Payment Method -->
            <div class="input-group">
              <label><i class="fa-solid fa-wallet"></i> Payment Method</label>
              <div class="select-wrap">
                <select v-model="checkout.payment">
                  <option>Cash on Delivery</option>
                  <option>GCash</option>
                  <option>Bank Transfer</option>
                </select>
                <i class="fa-solid fa-chevron-down select-arrow"></i>
              </div>
            </div>

            <!-- Payment badge -->
            <div class="payment-badge" v-if="checkout.payment === 'GCash'">
              <i class="fa-solid fa-mobile-screen-button"></i> GCash number will be shared after order
            </div>
            <div class="payment-badge cod" v-else-if="checkout.payment === 'Cash on Delivery'">
              <i class="fa-solid fa-money-bill-wave"></i> Pay in cash upon meetup
            </div>

            <button @click="processOrder" class="checkout-btn" :disabled="checkingOut">
              <span v-if="checkingOut">
                <i class="fa-solid fa-circle-notch fa-spin"></i> Processing...
              </span>
              <span v-else>
                <i class="fa-solid fa-bag-shopping"></i> Place Order
              </span>
            </button>

            <p class="safety-note">
              <i class="fa-solid fa-shield-halved"></i>
              Meet only in safe, public campus areas.
            </p>
          </div>
        </div>

      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <div class="empty-icon-wrap">
          <i class="fa-solid fa-cart-shopping empty-icon"></i>
        </div>
        <h3>Your cart is empty</h3>
        <p>Looks like you haven't added anything yet.</p>
        <button @click="router.push('/products')" class="browse-btn">
          <i class="fa-solid fa-store"></i> Browse Marketplace
        </button>
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
    alert('Failed to remove item.')
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
    alert(err.response?.data?.message || 'Checkout failed. Please try again.')
  } finally {
    checkingOut.value = false
  }
}

onMounted(fetchCart)
</script>

<style scoped>
.cart-wrapper {
  background: #f0f4f8;
  min-height: 100vh;
  padding: 2rem 1.5rem 4rem;
}

.cart-container {
  max-width: 1000px;
  margin: 0 auto;
}

/* Header */
.page-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 2rem;
  flex-wrap: wrap;
  gap: 12px;
}

.header-left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.header-icon {
  font-size: 1.6rem;
  color: #003366;
  background: #FFD700;
  width: 52px;
  height: 52px;
  border-radius: 14px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.page-title {
  font-size: 1.5rem;
  font-weight: 800;
  color: #003366;
  margin: 0;
  line-height: 1.2;
}

.page-sub {
  font-size: 0.82rem;
  color: #888;
  margin: 2px 0 0;
}

.continue-link {
  font-size: 0.85rem;
  color: #003366;
  text-decoration: none;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 14px;
  border: 1.5px solid #d0dbe8;
  border-radius: 8px;
  transition: 0.2s;
  background: white;
}

.continue-link:hover {
  background: #003366;
  color: white;
  border-color: #003366;
}

/* Loading */
.loading-state {
  text-align: center;
  padding: 5rem;
  color: #888;
}

.spinner {
  width: 36px;
  height: 36px;
  border: 3px solid #e0e0e0;
  border-top-color: #003366;
  border-radius: 50%;
  animation: spin 0.7s linear infinite;
  margin: 0 auto 1rem;
}

@keyframes spin { to { transform: rotate(360deg); } }

/* Layout */
.cart-layout {
  display: grid;
  grid-template-columns: 1fr 360px;
  gap: 24px;
  align-items: start;
}

/* Cart Card */
.cart-card {
  display: flex;
  gap: 16px;
  background: white;
  padding: 16px;
  border-radius: 14px;
  margin-bottom: 12px;
  border: 1px solid #e8eef4;
  transition: box-shadow 0.2s, transform 0.2s;
}

.cart-card:hover {
  box-shadow: 0 4px 20px rgba(0, 51, 102, 0.08);
  transform: translateY(-1px);
}

.card-img-wrap {
  position: relative;
  flex-shrink: 0;
}

.cart-img {
  width: 90px;
  height: 90px;
  object-fit: cover;
  border-radius: 10px;
  background: #f0f4f8;
  display: block;
}

.category-badge {
  position: absolute;
  bottom: 4px;
  left: 4px;
  background: rgba(0, 51, 102, 0.82);
  color: white;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 6px;
  border-radius: 4px;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.card-body {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 6px;
  min-width: 0;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 8px;
}

.item-title {
  font-size: 0.97rem;
  font-weight: 700;
  color: #003366;
  margin: 0;
  line-height: 1.3;
}

.remove-btn {
  background: none;
  border: 1px solid #e8eef4;
  border-radius: 6px;
  width: 28px;
  height: 28px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  color: #bbb;
  flex-shrink: 0;
  transition: 0.2s;
  font-size: 13px;
}

.remove-btn:hover {
  background: #fff0f0;
  color: #e74c3c;
  border-color: #e74c3c;
}

.item-seller {
  font-size: 0.8rem;
  color: #999;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 5px;
}

.card-bottom {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: auto;
}

.item-price {
  font-size: 1.05rem;
  font-weight: 800;
  color: #e74c3c;
}

.item-status {
  font-size: 0.75rem;
  color: #22c55e;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 4px;
}

/* Summary Card */
.summary-col {
  position: sticky;
  top: 80px;
}

.summary-card {
  background: white;
  border-radius: 16px;
  padding: 1.5rem;
  border: 1px solid #e8eef4;
}

.summary-title {
  font-size: 1rem;
  font-weight: 800;
  color: #003366;
  margin: 0 0 1rem;
  padding-bottom: 10px;
  border-bottom: 2px solid #FFD700;
  display: inline-block;
}

.summary-lines {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 12px;
  max-height: 160px;
  overflow-y: auto;
}

.summary-line {
  display: flex;
  justify-content: space-between;
  font-size: 0.82rem;
  color: #666;
  gap: 8px;
}

.summary-item-name {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  max-width: 170px;
}

.summary-divider {
  height: 1px;
  background: #eee;
  margin: 10px 0;
}

.summary-total {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-weight: 800;
  color: #003366;
  font-size: 0.95rem;
  margin-bottom: 1.25rem;
}

.total-amount {
  color: #e74c3c;
  font-size: 1.15rem;
}

/* Inputs */
.input-group {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin-bottom: 12px;
}

.input-group label {
  font-size: 0.75rem;
  font-weight: 700;
  color: #003366;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.select-wrap {
  position: relative;
}

select {
  width: 100%;
  padding: 10px 36px 10px 12px;
  border: 1.5px solid #dce4ee;
  border-radius: 8px;
  font-size: 0.875rem;
  color: #333;
  background: #f8fafc;
  appearance: none;
  cursor: pointer;
  transition: border-color 0.2s;
  outline: none;
}

select:focus { border-color: #003366; }

.select-arrow {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  font-size: 10px;
  color: #999;
  pointer-events: none;
}

/* Payment badge */
.payment-badge {
  background: #e8f0fe;
  color: #185FA5;
  font-size: 0.78rem;
  font-weight: 600;
  padding: 8px 12px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  gap: 7px;
  margin-bottom: 12px;
}

.payment-badge.cod {
  background: #e8f8ee;
  color: #1a7a40;
}

/* Checkout Button */
.checkout-btn {
  width: 100%;
  background: #003366;
  color: white;
  padding: 14px;
  border: none;
  border-radius: 10px;
  font-weight: 800;
  font-size: 0.95rem;
  cursor: pointer;
  margin-top: 4px;
  transition: 0.25s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
}

.checkout-btn:hover:not(:disabled) {
  background: #002244;
  transform: translateY(-2px);
  box-shadow: 0 6px 18px rgba(0, 51, 102, 0.25);
}

.checkout-btn:disabled {
  opacity: 0.65;
  cursor: not-allowed;
}

.safety-note {
  text-align: center;
  font-size: 0.75rem;
  color: #aaa;
  margin: 12px 0 0;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 5rem 2rem;
  background: white;
  border-radius: 16px;
  border: 1px solid #e8eef4;
}

.empty-icon-wrap {
  width: 80px;
  height: 80px;
  background: #f0f4f8;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 1.25rem;
}

.empty-icon {
  font-size: 2rem;
  color: #c0cdd8;
}

.empty-state h3 {
  font-size: 1.2rem;
  font-weight: 800;
  color: #003366;
  margin: 0 0 6px;
}

.empty-state p {
  color: #aaa;
  font-size: 0.9rem;
  margin: 0 0 1.5rem;
}

.browse-btn {
  background: #003366;
  color: white;
  border: none;
  padding: 12px 28px;
  border-radius: 10px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: 0.2s;
}

.browse-btn:hover {
  background: #002244;
  transform: translateY(-1px);
}

/* Transitions */
.cart-item-enter-active,
.cart-item-leave-active {
  transition: all 0.3s ease;
}

.cart-item-enter-from {
  opacity: 0;
  transform: translateY(-10px);
}

.cart-item-leave-to {
  opacity: 0;
  transform: translateX(20px);
}

/* Responsive */
@media (max-width: 768px) {
  .cart-layout {
    grid-template-columns: 1fr;
  }

  .summary-col {
    position: static;
  }

  .cart-card {
    flex-direction: column;
  }

  .cart-img {
    width: 100%;
    height: 180px;
  }

  .card-img-wrap {
    width: 100%;
  }
}
</style>