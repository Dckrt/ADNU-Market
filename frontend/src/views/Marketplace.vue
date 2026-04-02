<template>
  <div class="marketplace-wrapper">
    <div class="container">
      <header class="marketplace-header">
        <div class="title-section">
          <h1>University <span>Market</span></h1>
          <p>Verified essentials for Ateneo de Naga Students</p>
        </div>
        
        <div class="search-bar shadow-sm">
          <input v-model="searchQuery" type="text" placeholder="Search items..." @input="resetPage" />
          <select v-model="selectedCategory">
            <option value="All">All Categories</option>
            <option value="Textbooks">Textbooks</option>
            <option value="Electronics">Electronics</option>
            <option value="Dorm Items">Dorm Items</option>
          </select>
        </div>
      </header>

      <!-- 1. LOADING STATE (Always show this first) -->
      <div v-if="loading" class="product-grid">
        <SkeletonCard v-for="n in 8" :key="n" />
      </div>

      <!-- 2. DATA LOADED & ITEMS EXIST -->
      <div v-else-if="products && products.length > 0" class="product-grid">
        <ProductCard v-for="p in products" :key="p.id" :product="p" />
      </div>

      <!-- 3. DATA LOADED BUT NO ITEMS (Search/Category returned 0) -->
      <div v-else class="empty-state">
        <div class="empty-icon">🔎</div>
        <h3>No items found</h3>
        <p v-if="searchQuery || selectedCategory !== 'All'">
          No matches for "{{ searchQuery }}" in {{ selectedCategory }}.
        </p>
        <p v-else>The marketplace is currently empty. Check back later!</p>
        <button @click="clearSearch" class="link-btn">Show all items</button>
      </div>

      <!-- 4. PAGINATION -->
      <div class="pagination-footer" v-if="products.length > 0">
        <button @click="prevPage" :disabled="page === 1" class="page-btn">Previous</button>
        <span class="page-info">Page {{ page }}</span>
        <button @click="nextPage" :disabled="page >= 5" class="page-btn">Next</button>
      </div>
    </div>
  </div>
</template>


<script>
import API from '../services/api'
import ProductCard from '../components/ProductCard.vue'
import SkeletonCard from '../components/SkeletonCard.vue'

export default {
  components: { ProductCard, SkeletonCard },

  data() {
    return {
      products: [],
      loading: true,
      page: 1,
      limit: 12,
      searchQuery: '',
      selectedCategory: 'All',
      timer: null
    }
  },

  mounted() {
    this.fetchProducts()
  },

  watch: {
    page() { 
      this.fetchProducts() 
    },
    searchQuery() { 
      this.debouncedFetch() 
    },
    selectedCategory() { 
      this.page = 1; 
      this.fetchProducts(); 
    }
  },

  methods: {
    async fetchProducts() {
      this.loading = true
      try {
        const res = await API.getProducts({ 
          page: this.page, 
          limit: this.limit,
          search: this.searchQuery,
          category: this.selectedCategory !== 'All' ? this.selectedCategory : null
        })
        
        // Debugging: This helps you see what Oracle is actually sending back
        console.log("Data from Oracle:", res.data);

        // Ensure we capture the list correctly regardless of backend format
        this.products = Array.isArray(res.data) ? res.data : (res.data.products || []);
        
      } catch (err) {
        console.error("Marketplace Fetch Error:", err)
      } finally {
        this.loading = false
      }
    },
    resetPage() { 
      this.page = 1 
    },
    clearSearch() {
      this.searchQuery = '';
      this.selectedCategory = 'All';
      this.resetPage();
      this.fetchProducts();
    },
    nextPage() { 
      if (this.page < 5) this.page++ 
    },
    prevPage() { 
      if (this.page > 1) this.page-- 
    },
    debouncedFetch() {
      clearTimeout(this.timer)
      this.timer = setTimeout(() => {
        this.resetPage()
        this.fetchProducts()
      }, 500)
    }
  }
}
</script>

<style scoped>
.marketplace-wrapper {
  background-color: #f8fafc;
  min-height: 100vh;
}
.container { max-width: 1200px; margin: 0 auto; padding: 2rem; }
.marketplace-header { margin-bottom: 2.5rem; border-left: 5px solid #FFD700; padding-left: 1.5rem; }
.title-section h1 { color: #003366; font-size: 2rem; font-weight: 800; margin: 0; }
.title-section span { color: #64748b; font-weight: 300; }
.search-bar { display: flex; gap: 10px; background: white; padding: 10px; border-radius: 12px; max-width: 600px; margin-top: 1.5rem; border: 1px solid #e2e8f0; }
.search-bar input { flex-grow: 1; border: none; padding: 10px; font-size: 1rem; outline: none; }
.search-bar select { border: none; background: #f1f5f9; padding: 0 15px; border-radius: 8px; font-weight: 600; color: #003366; }
.product-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 2rem; }
.empty-state { text-align: center; padding: 5rem; background: white; border-radius: 15px; border: 1px dashed #cbd5e1; }
.empty-icon { font-size: 3rem; margin-bottom: 1rem; }
.pagination-footer { margin-top: 4rem; display: flex; justify-content: center; align-items: center; gap: 20px; padding-bottom: 3rem; }
.page-btn { padding: 10px 20px; background: white; border: 1px solid #e2e8f0; border-radius: 8px; color: #003366; font-weight: 700; cursor: pointer; transition: 0.3s; }
.page-btn:hover:not(:disabled) { background: #003366; color: white; }
.page-btn:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
