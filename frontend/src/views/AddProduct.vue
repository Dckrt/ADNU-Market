<template>
  <div class="form">
    <h2>Sell Item</h2>

    <input v-model="title" placeholder="Title" />

    <input 
      v-model.number="price" 
      type="number" 
      placeholder="Price" 
    />

    <input v-model="category" placeholder="Category" />

    <textarea 
      v-model="description" 
      placeholder="Description">
    </textarea>

    <button @click="submit" :disabled="loading">
      {{ loading ? "Posting..." : "Post Product" }}
    </button>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'
import { useRouter } from 'vue-router'

const router = useRouter()

const title = ref('')
const price = ref('')
const category = ref('')
const description = ref('')
const loading = ref(false)

const submit = async () => {

  // 🔥 validation
  if (!title.value || !price.value || !category.value) {
    alert("Please fill all required fields")
    return
  }

  const user = JSON.parse(localStorage.getItem('user'))

  if (!user) {
    alert("Please login first")
    return router.push('/auth')
  }

  try {
    loading.value = true

    await api.createProduct({
      title: title.value,
      description: description.value,
      price: price.value,
      category: category.value,
      user_id: user.user_id
    })

    alert("Product added successfully! 🎉")

    // 🔥 reset form
    title.value = ''
    price.value = ''
    category.value = ''
    description.value = ''

    // 🔥 redirect to marketplace
    router.push('/products')

  } catch (err) {
    console.error(err)
    alert("Failed to add product")
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.form {
  max-width: 400px;
  margin: 40px auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

input, textarea {
  padding: 10px;
  border-radius: 6px;
  border: 1px solid #ccc;
}

button {
  background: #003366;
  color: white;
  padding: 10px;
  border-radius: 6px;
  border: none;
  cursor: pointer;
}

button:disabled {
  background: #999;
}
</style>