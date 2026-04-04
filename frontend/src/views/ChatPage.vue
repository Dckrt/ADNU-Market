<template>
  <div class="chat-wrapper">
    <div class="chat-layout">

      <!-- Sidebar: Conversations -->
      <div class="chat-sidebar">
        <div class="sidebar-header">
          <h2>Messages</h2>
        </div>
        <div class="conversations">
          <div class="empty-convos" v-if="!receiver_id">
            <i class="fa-solid fa-comment-dots"></i>
            <p>No conversation selected</p>
          </div>
          <div v-else class="convo-item active">
            <div class="convo-avatar">{{ receiverInitial }}</div>
            <div class="convo-info">
              <p class="convo-name">{{ receiverName || 'Seller' }}</p>
              <p class="convo-preview">{{ messages[messages.length - 1]?.message_text || 'No messages yet' }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Chat Area -->
      <div class="chat-main">

        <!-- Chat Header -->
        <div class="chat-header" v-if="receiver_id">
          <div class="chat-avatar">{{ receiverInitial }}</div>
          <div>
            <p class="chat-name">{{ receiverName || 'Seller' }}</p>
            <p class="chat-status">ADNU Student</p>
          </div>
        </div>

        <div class="no-chat" v-else>
          <i class="fa-solid fa-comments"></i>
          <p>Select a conversation to start chatting</p>
        </div>

        <!-- Messages -->
        <div class="messages-area" ref="messagesArea" v-if="receiver_id">
          <div v-if="messages.length === 0" class="no-messages">
            <p>No messages yet. Say hello! 👋</p>
          </div>
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="msg-row"
            :class="msg.sender_id == user.user_id ? 'mine' : 'theirs'"
          >
            <div class="bubble">
              {{ msg.message_text }}
              <span class="msg-time">{{ formatTime(msg.sent_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Input -->
        <div class="input-area" v-if="receiver_id">
          <input
            v-model="newMessage"
            placeholder="Type a message..."
            @keydown.enter="sendMessage"
          />
          <button @click="sendMessage" :disabled="!newMessage.trim() || sending" class="send-btn">
            <i class="fa-solid fa-paper-plane"></i>
          </button>
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const messages = ref([])
const newMessage = ref('')
const sending = ref(false)
const messagesArea = ref(null)
const receiverName = ref('')

const user = JSON.parse(localStorage.getItem('user'))
const receiver_id = route.query.seller_id

const receiverInitial = computed(() => {
  return receiverName.value ? receiverName.value[0].toUpperCase() : 'S'
})

const scrollToBottom = async () => {
  await nextTick()
  if (messagesArea.value) {
    messagesArea.value.scrollTop = messagesArea.value.scrollHeight
  }
}

const loadMessages = async () => {
  if (!receiver_id) return
  try {
    const res = await api.getMessages(user.user_id, receiver_id)
    messages.value = res.data
    scrollToBottom()
  } catch (err) {
    console.error('Load messages error:', err)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim() || sending.value) return
  try {
    sending.value = true
    await api.sendMessage({
      sender_id: user.user_id,
      receiver_id,
      message_text: newMessage.value.trim()
    })
    newMessage.value = ''
    await loadMessages()
  } catch (err) {
    console.error('Send error:', err)
    alert('Failed to send message ❌')
  } finally {
    sending.value = false
  }
}

const formatTime = (dateStr) => {
  if (!dateStr) return ''
  const d = new Date(dateStr)
  return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

onMounted(async () => {
  // Get seller name from query param if passed
  if (route.query.seller_name) {
    receiverName.value = route.query.seller_name
  }
  await loadMessages()

  // Auto-refresh every 10 seconds
  setInterval(loadMessages, 10000)
})
</script>

<style scoped>
.chat-wrapper {
  background: #f8fafc;
  min-height: 100vh;
  padding: 1.5rem;
}

.chat-layout {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 280px 1fr;
  height: calc(100vh - 100px);
  background: white;
  border-radius: 16px;
  border: 0.5px solid #eee;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
}

/* Sidebar */
.chat-sidebar {
  border-right: 1px solid #f1f5f9;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 1.25rem 1rem;
  border-bottom: 1px solid #f1f5f9;
}

.sidebar-header h2 {
  font-size: 1rem;
  font-weight: 700;
  color: #003366;
  margin: 0;
}

.conversations { flex: 1; overflow-y: auto; }

.empty-convos {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: #ccc;
  gap: 8px;
  font-size: 0.85rem;
}

.empty-convos i { font-size: 2rem; }

.convo-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  cursor: pointer;
  transition: 0.15s;
  border-bottom: 1px solid #f8fafc;
}

.convo-item:hover, .convo-item.active {
  background: #f0f4ff;
}

.convo-avatar {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: #003366;
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 1rem;
  flex-shrink: 0;
}

.convo-info { flex: 1; min-width: 0; }
.convo-name { font-size: 0.875rem; font-weight: 700; color: #003366; margin: 0 0 2px; }
.convo-preview { font-size: 0.78rem; color: #888; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

/* Chat Main */
.chat-main {
  display: flex;
  flex-direction: column;
}

.chat-header {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 1rem 1.25rem;
  border-bottom: 1px solid #f1f5f9;
  background: white;
}

.chat-avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #FFD700;
  color: #003366;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 800;
  font-size: 1rem;
}

.chat-name { font-size: 0.9rem; font-weight: 700; color: #003366; margin: 0 0 2px; }
.chat-status { font-size: 0.75rem; color: #16a34a; margin: 0; }

.no-chat {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #ccc;
  gap: 12px;
  font-size: 0.9rem;
}

.no-chat i { font-size: 3rem; }

/* Messages */
.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 8px;
  background: #f8fafc;
}

.no-messages {
  text-align: center;
  color: #aaa;
  font-size: 0.85rem;
  margin-top: 2rem;
}

.msg-row {
  display: flex;
}

.msg-row.mine { justify-content: flex-end; }
.msg-row.theirs { justify-content: flex-start; }

.bubble {
  max-width: 65%;
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 0.875rem;
  line-height: 1.5;
  position: relative;
}

.mine .bubble {
  background: #003366;
  color: white;
  border-bottom-right-radius: 4px;
}

.theirs .bubble {
  background: white;
  color: #333;
  border: 0.5px solid #eee;
  border-bottom-left-radius: 4px;
}

.msg-time {
  display: block;
  font-size: 0.65rem;
  margin-top: 4px;
  opacity: 0.6;
  text-align: right;
}

/* Input */
.input-area {
  display: flex;
  gap: 10px;
  padding: 1rem 1.25rem;
  border-top: 1px solid #f1f5f9;
  background: white;
}

.input-area input {
  flex: 1;
  padding: 10px 14px;
  border: 1px solid #e2e8f0;
  border-radius: 24px;
  font-size: 0.9rem;
  outline: none;
  transition: 0.2s;
}

.input-area input:focus { border-color: #003366; }

.send-btn {
  width: 42px;
  height: 42px;
  border-radius: 50%;
  background: #003366;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: 0.2s;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) { background: #002244; transform: scale(1.05); }
.send-btn:disabled { opacity: 0.5; cursor: not-allowed; }

@media (max-width: 640px) {
  .chat-layout { grid-template-columns: 1fr; }
  .chat-sidebar { display: none; }
}
</style>