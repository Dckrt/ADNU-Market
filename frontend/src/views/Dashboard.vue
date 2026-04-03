<template>
  <div class="dashboard-wrapper">
    <div class="container">

      <!-- Header -->
      <header class="dashboard-header">
        <div class="title-section">
          <h1>Seller <span>Dashboard</span></h1>
          <p>Manage your campus listings and sales status</p>
        </div>
        <button class="add-btn" @click="router.push('/add-product')">
          <i class="fa-solid fa-plus"></i> Add New Product
        </button>
      </header>

      <!-- Stats Bar -->
      <div class="stats-bar">
        <div class="stat-card">
          <div class="stat-icon">
            <i class="fa-solid fa-box"></i>
          </div>
          <div>
            <span class="stat-label">Total Listings</span>
            <span class="stat-value">{{ totalProducts }}</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon green">
            <i class="fa-solid fa-circle-check"></i>
          </div>
          <div>
            <span class="stat-label">Available</span>
            <span class="stat-value">{{ products.length }}</span>
          </div>
        </div>
        <div class="stat-card">
          <div class="stat-icon gold">
            <i class="fa-solid fa-file-lines"></i>
          </div>
          <div>
            <span class="stat-label">Current Page</span>
            <span class="stat-value">{{ page }} / {{ totalPages || 1 }}</span>
          </div>
        </div>
      </div>

      <!-- Section Title -->
      <div class="section-header">
        <h2>Your Listings</h2>
        <span class="item-count">{{ totalProducts }} item{{ totalProducts !== 1 ? 's' : '' }}</span>
      </div>

      <!-- Loading Skeletons -->
      <div v-if="loading" class="product-grid">
        <SkeletonCard v-for="n in 8" :key="n" />
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
        <div class="empty-icon">🏪</div>
        <h3>No listings yet</h3>
        <p>Start selling to ADNU students by posting your first item.</p>
        <button @click="router.push('/add-product')" class="add-btn">
          <i class="fa-solid fa-plus"></i> Post Your First Item
        </button>
      </div>

      <!-- Pagination -->
      <nav v-if="totalPages > 1" class="pagination-container">
        <button @click="prevPage" :disabled="page === 1" class="page-btn">
          <i class="fa-solid fa-chevron-left"></i> Prev
        </button>
        <div class="page-numbers">
          <button
            v-for="p in totalPages"
            :key="p"
            class="page-num"
            :class="{ active: p === page }"
            @click="page = p"
          >{{ p }}</button>
        </div>
        <button @click="nextPage" :disabled="page >= totalPages" class="page-btn">
          Next <i class="fa-solid fa-chevron-right"></i>
        </button>
      </nav>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import API from '../services/api'
import ProductCard from '../components/ProductCard.vue'
import SkeletonCard from '../components/SkeletonCard.vue'

const router = useRouter()
const products = ref([])
const loading = ref(true)
const page = ref(1)
const limit = 8
const totalProducts = ref(0)

const totalPages = computed(() => Math.max(1, Math.ceil(totalProducts.value / limit)))

const fetchProducts = async () => {
  loading.value = true
  try {
    const res = await API.getProducts({ page: page.value, limit })
    if (Array.isArray(res.data)) {
      products.value = res.data
      totalProducts.value = res.data.length
    } else {
      products.value = res.data.products || []
      totalProducts.value = res.data.total || 0
    }
  } catch (err) {
    console.error('Dashboard Fetch Error:', err)
  } finally {
    loading.value = false
  }
}

const nextPage = () => { if (page.value < totalPages.value) page.value++ }
const prevPage = () => { if (page.value > 1) page.value-- }

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
  padding: 2rem 1.5rem;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  border-left: 5px solid #FFD700;
  padding-left: 1.5rem;
  flex-wrap: wrap;
  gap: 1rem;
}

.title-section h1 {
  margin: 0;
  color: #003366;
  font-size: 1.8rem;
  font-weight: 800;
}

.title-section h1 span { color: #64748b; font-weight: 300; }
.title-section p { color: #888; margin: 4px 0 0; font-size: 0.875rem; }

.add-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  background-color: #003366;
  color: white;
  border: none;
  padding: 11px 22px;
  border-radius: 8px;
  font-weight: 700;
  font-size: 0.9rem;
  cursor: pointer;
  transition: 0.2s;
}

.add-btn:hover {
  background-color: #002244;
  transform: translateY(-2px);
}

.stats-bar {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
  gap: 12px;
  margin-bottom: 2rem;
}

.stat-card {
  background: white;
  border-radius: 12px;
  padding: 1rem 1.25rem;
  display: flex;
  align-items: center;
  gap: 14px;
  border: 0.5px solid #eee;
}

.stat-icon {
  width: 40px;
  height: 40px;
  background: #f0f4ff;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #003366;
  font-size: 1rem;
  flex-shrink: 0;
}

.stat-icon.green { color: #16a34a; background: #f0fdf4; }
.stat-icon.gold { color: #b45309; background: #fffbeb; }

.stat-card div { display: flex; flex-direction: column; }
.stat-label { font-size: 0.72rem; text-transform: uppercase; color: #888; letter-spacing: 0.5px; }
.stat-value { font-size: 1.3rem; font-weight: 800; color: #003366; }

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.25rem;
}

.section-header h2 {
  font-size: 1.1rem;
  font-weight: 700;
  color: #003366;
  margin: 0;
}

.item-count {
  font-size: 0.82rem;
  color: #888;
  background: #f1f5f9;
  padding: 3px 10px;
  border-radius: 20px;
}

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 1.5rem;
}

.empty-state {
  text-align: center;
  padding: 5rem 2rem;
  background: white;
  border-radius: 16px;
  border: 1px dashed #cbd5e1;
}

.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.empty-state h3 { color: #003366; font-size: 1.1rem; margin: 0 0 8px; }
.empty-state p { color: #888; font-size: 0.9rem; margin: 0 0 1.5rem; }

.pagination-container {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  margin-top: 3rem;
  padding-bottom: 2rem;
}

.page-btn {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border: 1px solid #e2e8f0;
  background: white;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  color: #003366;
  font-size: 0.875rem;
  transition: 0.2s;
}

.page-btn:hover:not(:disabled) { background-color: #003366; color: white; border-color: #003366; }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }

.page-numbers { display: flex; gap: 6px; }

.page-num {
  width: 36px;
  height: 36px;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
  background: white;
  color: #555;
  font-weight: 600;
  cursor: pointer;
  transition: 0.2s;
  font-size: 0.875rem;
}

.page-num:hover { border-color: #003366; color: #003366; }
.page-num.active { background: #003366; color: white; border-color: #003366; }
</style>