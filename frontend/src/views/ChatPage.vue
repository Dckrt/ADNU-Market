<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const messages = ref([])
const newMessage = ref("")

const user = JSON.parse(localStorage.getItem('user'))
const receiver_id = route.query.seller_id

const loadMessages = async () => {
  const res = await api.getMessages(user.user_id, receiver_id)
  messages.value = res.data
}

const sendMessage = async () => {
  if (!newMessage.value) return

  await api.sendMessage({
    sender_id: user.user_id,
    receiver_id,
    message_text: newMessage.value
  })

  newMessage.value = ""
  loadMessages()
}

onMounted(loadMessages)
</script>

<template>
  <div class="chat-container">
    <h2>Chat</h2>

    <div class="messages">
      <div 
        v-for="(msg, i) in messages" 
        :key="i"
        :class="msg.sender_id == user.user_id ? 'mine' : 'theirs'"
      >
        {{ msg.message_text }}
      </div>
    </div>

    <div class="input-box">
      <input v-model="newMessage" placeholder="Type message..." />
      <button @click="sendMessage">Send</button>
    </div>
  </div>
</template>

<style scoped>
.chat-container {
  padding: 20px;
}

.messages {
  height: 300px;
  overflow-y: auto;
  margin-bottom: 10px;
}

.mine {
  text-align: right;
  background: #003366;
  color: white;
  margin: 5px;
  padding: 8px;
  border-radius: 6px;
}

.theirs {
  text-align: left;
  background: #eee;
  margin: 5px;
  padding: 8px;
  border-radius: 6px;
}

.input-box {
  display: flex;
  gap: 10px;
}
</style>