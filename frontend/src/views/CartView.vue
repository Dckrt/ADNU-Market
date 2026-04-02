<template>
  <div class="cart-container">
    <div class="container">

      <h2 class="title">
        <i class="fa-solid fa-cart-shopping"></i> My Cart
      </h2>

      <!-- CART ITEMS -->
      <div v-if="cartItems.length">

        <div 
          v-for="item in cartItems" 
          :key="item.cart_id" 
          class="cart-card"
        >
          <img :src="item.image_url || '/placeholder.png'" class="cart-img" />

          <div class="details">
            <h3>{{ item.title }}</h3>
            <p class="price">₱{{ item.price }}</p>
          </div>

          <!-- REMOVE -->
          <button @click="removeItem(item.cart_id)" class="remove-btn">
            ❌
          </button>
        </div>

      </div>

      <!-- EMPTY -->
      <p v-else class="empty">Your cart is empty</p>

      <!-- CHECKOUT -->
      <div class="checkout-section" v-if="cartItems.length">

        <h3>Checkout</h3>

        <p class="total">Total: ₱{{ total }}</p>

        <label>Pickup Location</label>
        <select v-model="checkout.location" class="input">
          <option>Richards Hall Lobby</option>
          <option>University Gazebo</option>
          <option>O'Brien Library Entrance</option>
          <option>Dormitory Gate A</option>
        </select>

        <label>Payment Method</label>
        <select v-model="checkout.payment" class="input">
          <option>Cash on Delivery</option>
          <option>GCash</option>
          <option>Bank Transfer</option>
        </select>

        <button @click="processOrder" class="checkout-btn">
          Place Order
        </button>

      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'

const cartItems = ref([])
const user = JSON.parse(localStorage.getItem('user'))

const checkout = ref({
  location: 'Richards Hall Lobby',
  payment: 'Cash on Delivery'
})

// 🔥 fetch cart
const fetchCart = async () => {
  if (!user) return

  try {
    const res = await api.getCart(user.user_id)
    cartItems.value = res.data
  } catch (err) {
    console.error(err)
  }
}

// 🔥 total price
const total = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.price, 0)
})

// 🔥 remove item
const removeItem = async (id) => {
  try {
    await api.removeFromCart(id)
    cartItems.value = cartItems.value.filter(i => i.cart_id !== id)
  } catch (err) {
    console.error(err)
  }
}

// 🔥 checkout
const processOrder = async () => {
  try {
    await api.checkout({
      user_id: user.user_id,
      total: total.value
    })

    alert("Order placed successfully! 🎉")
    cartItems.value = []

  } catch (err) {
    console.error(err)
    alert("Checkout failed")
  }
}

onMounted(fetchCart)
</script>

<style scoped>
.cart-container {
  background: #f5f5f5;
  min-height: 100vh;
  padding: 20px;
}

.container {
  max-width: 800px;
  margin: auto;
}

/* ITEM */
.cart-card {
  display: flex;
  align-items: center;
  gap: 15px;
  background: white;
  padding: 15px;
  border-radius: 10px;
  margin-bottom: 10px;
}

.cart-img {
  width: 80px;
  height: 80px;
  object-fit: cover;
}

.details {
  flex: 1;
}

.price {
  color: #ee4d2d;
  font-weight: bold;
}

.remove-btn {
  background: none;
  border: none;
  font-size: 18px;
  cursor: pointer;
}

/* EMPTY */
.empty {
  text-align: center;
  color: gray;
  margin-top: 20px;
}

/* CHECKOUT */
.checkout-section {
  margin-top: 20px;
  background: white;
  padding: 20px;
  border-radius: 10px;
}

.total {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.input {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
}

.checkout-btn {
  width: 100%;
  background: #ee4d2d;
  color: white;
  padding: 12px;
  border: none;
  border-radius: 6px;
  font-weight: bold;
  cursor: pointer;
}
</style>