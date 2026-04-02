<template>
  <div class="dashboard-wrapper">
    

    <div class="container">
      <!-- Header with "Add Product" Action -->
      <header class="dashboard-header">
        <div class="title-section">
          <h1>Seller <span>Dashboard</span></h1>
          <p>Manage your campus listings and sales status</p>
        </div>
        <button class="add-btn" @click="openModal">+ Add New Product</button>
      </header>

      <!-- Seller Stats Bar (Optional but looks professional) -->
      <div class="stats-bar shadow-sm">
        <div class="stat-item">
          <span class="stat-label">Total Listings</span>
          <span class="stat-value">{{ totalProducts }}</span>
        </div>
        <div class="stat-item">
          <span class="stat-label">Current Page</span>
          <span class="stat-value">{{ page }} / {{ totalPages || 1 }}</span>
        </div>
      </div>

      <!-- Loading Skeletons -->
      <div v-if="loading" class="product-grid">
        <SkeletonCard v-for="n in 4" :key="n" />
      </div>

      <!-- Products Grid -->
      <div v-else-if="products.length > 0" class="product-grid">
        <ProductCard
          v-for="product in products"
          :key="product.id"
          :product="product"
        />
      </div>

      <!-- Empty State -->
      <div v-else class="empty-state">
        <p>You haven't posted any items yet.</p>
        <button @click="openModal" class="link-btn">Post your first item now</button>
      </div>

      <!-- Pagination -->
      <nav v-if="totalPages > 1" class="pagination-container">
        <button @click="prevPage" :disabled="page === 1" class="page-btn">
          &laquo; Prev
        </button>
        <span class="page-info">Page {{ page }} of {{ totalPages }}</span>
        <button @click="nextPage" :disabled="page >= totalPages" class="page-btn">
          Next &raquo;
        </button>
      </nav>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import API from '../services/api'
import Navbar from '../components/Navbar.vue'
import ProductCard from '../components/ProductCard.vue'
import SkeletonCard from '../components/SkeletonCard.vue'

const products = ref([])
const loading = ref(true)
const page = ref(1)
const limit = 8 // Reduced to fit the dashboard better
const totalProducts = ref(0)

const totalPages = computed(() => Math.ceil(totalProducts.value / limit))

const fetchProducts = async () => {
  loading.value = true
  try {
    // Note: API.get uses your services/api.js config
    const res = await API.getProducts({ page: page.value, limit })
    products.value = res.data.products
    totalProducts.value = res.data.total
  } catch (err) {
    console.error("Dashboard Fetch Error:", err)
  } finally {
    loading.value = false
  }
}

const nextPage = () => { if (page.value < totalPages.value) page.value++ }
const prevPage = () => { if (page.value > 1) page.value-- }
const openModal = () => { alert("Add Product Modal logic goes here!") }

onMounted(fetchProducts)
watch(page, fetchProducts)
</script>

<style scoped>
.dashboard-wrapper {
  background-color: #f8fafc;
  min-height: 100vh;
}

.container {
  max-width: 1100px;
  margin: 0 auto;
  padding: 2rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-left: 5px solid #FFD700; /* Gold accent */
  padding-left: 1.5rem;
}

.title-section h1 {
  margin: 0;
  color: #003366; /* Ateneo Blue */
  font-size: 1.8rem;
}

.title-section h1 span { color: #555; font-weight: 300; }
.title-section p { color: #666; margin: 5px 0 0 0; }

.add-btn {
  background-color: #003366;
  color: white;
  border: none;
  padding: 12px 24px;
  border-radius: 8px;
  font-weight: bold;
  cursor: pointer;
  transition: 0.3s;
}

.add-btn:hover {
  background-color: #002244;
  transform: translateY(-2px);
}

.stats-bar {
  background: white;
  display: flex;
  gap: 40px;
  padding: 1.2rem 2rem;
  border-radius: 12px;
  margin-bottom: 2rem;
}

.stat-item { display: flex; flex-direction: column; }
.stat-label { font-size: 0.75rem; text-transform: uppercase; color: #888; letter-spacing: 1px; }
.stat-value { font-size: 1.3rem; font-weight: 800; color: #003366; }

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 4rem;
  background: white;
  border-radius: 12px;
  color: #888;
}

.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 20px;
  margin-top: 3rem;
}

.page-btn {
  padding: 10px 20px;
  border: 1px solid #ddd;
  background: white;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 600;
  color: #003366;
  transition: 0.2s;
}

.page-btn:hover:not(:disabled) {
  background-color: #003366;
  color: white;
}

.page-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.page-info { font-weight: bold; color: #555; }
</style>
