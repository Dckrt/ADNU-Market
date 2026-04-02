<template>
  <div class="home">

    <!-- 🔥 HERO SECTION -->
    <section class="hero">
      <h1>Welcome to AdnuMarket</h1>
      <p>Buy and sell within your campus community</p>

      <div class="hero-actions">
        <router-link to="/products" class="btn-primary">
          Browse Products
        </router-link>
        <router-link to="/dashboard" class="btn-secondary">
          Sell Item
        </router-link>
      </div>
    </section>

    <!-- 🔥 CATEGORIES -->
    <section class="categories">
      <h2>Categories</h2>
      <div class="category-grid">
        <div class="category-card">📱 Electronics</div>
        <div class="category-card">📚 Books</div>
        <div class="category-card">👕 Clothes</div>
        <div class="category-card">🎒 School Items</div>
      </div>
    </section>

    <!-- 🔥 FEATURED PRODUCTS -->
    <section class="products">
      <h2>Latest Products</h2>

      <div v-if="loading">Loading...</div>

      <div v-else class="product-grid">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
        />
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import ProductCard from '@/components/ProductCard.vue'
import api from '@/services/api'

const products = ref([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await api.get('/products')
    products.value = res.data.slice(0, 8) // limit to 8 items
  } catch (err) {
    console.error("Error fetching products", err)
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
.home {
  padding: 20px;
}

/* 🔥 HERO */
.hero {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #003366, #0055aa);
  color: white;
  border-radius: 12px;
  margin-bottom: 40px;
}

.hero h1 {
  font-size: 2.5rem;
  font-weight: 800;
}

.hero p {
  margin: 10px 0 20px;
  font-size: 1.1rem;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: 15px;
}

.btn-primary {
  background: #FFD700;
  color: #003366;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: bold;
  text-decoration: none;
}

.btn-secondary {
  background: transparent;
  border: 2px solid white;
  color: white;
  padding: 10px 20px;
  border-radius: 8px;
  text-decoration: none;
}

/* 🔥 CATEGORIES */
.categories {
  margin-bottom: 40px;
}

.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 15px;
}

.category-card {
  background: #f1f5f9;
  padding: 20px;
  text-align: center;
  border-radius: 10px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.2s;
}

.category-card:hover {
  background: #e2e8f0;
}

/* 🔥 PRODUCTS */
.products {
  margin-bottom: 40px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
  gap: 20px;
}
</style>