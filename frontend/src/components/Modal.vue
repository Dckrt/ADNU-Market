<template>
  <div class="modal">
    <div class="modal-content">
      <h3>Post New Product</h3>
      <input v-model="product.title" placeholder="Title (e.g., Math Textbook)" />
      <textarea v-model="product.description" placeholder="Description"></textarea>
      <input v-model.number="product.price" type="number" placeholder="Price (₱)" />
      <select v-model="product.category">
        <option value="Textbooks">Textbooks</option>
        <option value="Electronics">Electronics</option>
        <option value="Dorm Items">Dorm Items</option>
      </select>
      <button @click="submit">Post to Marketplace</button>
      <button @click="$emit('close')">Cancel</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';

const emit = defineEmits(['close', 'refresh']);
const user = JSON.parse(localStorage.getItem('user'));
const product = ref({ title: '', description: '', price: 0, category: 'Textbooks', seller_id: user.user_id });

const submit = async () => {
  await api.createProduct(product.value);
  emit('refresh');
  emit('close');
};
</script>
