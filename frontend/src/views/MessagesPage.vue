<template>
  <div class="messages-page">
    <div class="messages-layout">

      <!-- Thread List -->
      <div class="thread-sidebar">
        <div class="sidebar-header">
          <h2>Messages</h2>
        </div>

        <div class="search-box">
          <input v-model="search" placeholder="Search conversations..." />
        </div>

        <div class="thread-list">
          <p v-if="filteredThreads.length === 0" class="empty-threads">No conversations yet.</p>

          <div
            v-for="thread in filteredThreads"
            :key="thread.seller_id"
            class="thread-item"
            :class="{ active: activeThread?.seller_id === thread.seller_id }"
            @click="openThread(thread)"
          >
            <div class="avatar">{{ thread.seller_name?.charAt(0) || '?' }}</div>
            <div class="thread-info">
              <div class="thread-top">
                <span class="thread-name">{{ thread.seller_name }}</span>
                <span class="thread-time">{{ formatTime(thread.last_time) }}</span>
              </div>
              <p class="thread-preview">{{ thread.last_message || 'Start a conversation' }}</p>
            </div>
            <span v-if="thread.unread" class="unread-dot"></span>
          </div>
        </div>
      </div>

      <!-- Chat Window -->
      <div class="chat-window" v-if="activeThread">
        <div class="chat-header">
          <div class="avatar">{{ activeThread.seller_name?.charAt(0) }}</div>
          <div>
            <p class="chat-partner-name">{{ activeThread.seller_name }}</p>
            <span class="chat-status">Active now</span>
          </div>
        </div>

        <!-- Product context if opened from a product page -->
        <div v-if="activeThread.product" class="product-context">
          <img :src="activeThread.product.image_url || '/images/placeholder.png'" class="product-thumb" />
          <div>
            <p class="product-context-title">{{ activeThread.product.title }}</p>
            <p class="product-context-price">₱{{ formatPrice(activeThread.product.price) }}</p>
          </div>
        </div>

        <div class="message-list" ref="messageListRef">
          <div
            v-for="(msg, i) in messages"
            :key="i"
            class="message-row"
            :class="msg.sender_id === user?.user_id ? 'mine' : 'theirs'"
          >
            <div class="bubble">{{ msg.content }}</div>
            <span class="msg-time">{{ formatTime(msg.created_at) }}</span>
          </div>
        </div>

        <div class="chat-input-row">
          <input
            v-model="newMessage"
            placeholder="Type a message..."
            @keyup.enter="sendMessage"
          />
          <button class="send-btn" @click="sendMessage">
            <i class="fa-solid fa-paper-plane"></i>
          </button>
        </div>
      </div>

      <!-- Empty State -->
      <div class="empty-chat" v-else>
        <i class="fa-regular fa-comment-dots empty-icon"></i>
        <p>Select a conversation to start messaging</p>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/services/api'

const route = useRoute()
const user = JSON.parse(localStorage.getItem('user'))

const threads = ref([])
const activeThread = ref(null)
const messages = ref([])
const newMessage = ref('')
const search = ref('')
const messageListRef = ref(null)

const filteredThreads = computed(() => {
  if (!search.value) return threads.value
  return threads.value.filter(t =>
    t.seller_name?.toLowerCase().includes(search.value.toLowerCase())
  )
})

const fetchThreads = async () => {
  try {
    const res = await api.getThreads(user.user_id)
    threads.value = res.data || []

    // If coming from product page via ?seller_id=...
    const sellerId = route.query.seller_id
    if (sellerId) {
      let thread = threads.value.find(t => t.seller_id == sellerId)
      if (!thread) {
        thread = {
          seller_id: sellerId,
          seller_name: route.query.seller_name || 'Seller',
          last_message: '',
          unread: false
        }
        threads.value.unshift(thread)
      }
      openThread(thread)
    }
  } catch (err) {
    console.error(err)
  }
}

const openThread = async (thread) => {
  activeThread.value = thread
  thread.unread = false
  try {
    const res = await api.getMessages(user.user_id, thread.seller_id)
    messages.value = res.data || []
    await scrollToBottom()
  } catch (err) {
    console.error(err)
  }
}

const sendMessage = async () => {
  if (!newMessage.value.trim()) return
  try {
    await api.sendMessage({
      sender_id: user.user_id,
      receiver_id: activeThread.value.seller_id,
      content: newMessage.value.trim()
    })
    messages.value.push({
      sender_id: user.user_id,
      content: newMessage.value.trim(),
      created_at: new Date().toISOString()
    })
    newMessage.value = ''
    await scrollToBottom()
  } catch (err) {
    console.error(err)
  }
}

const scrollToBottom = async () => {
  await nextTick()
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

const formatTime = (d) => {
  if (!d) return ''
  const date = new Date(d)
  const now = new Date()
  const diff = now - date
  if (diff < 3600000) return `${Math.floor(diff / 60000)}m ago`
  if (diff < 86400000) return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
  return date.toLocaleDateString()
}

const formatPrice = (v) =>
  parseFloat(v).toLocaleString(undefined, { minimumFractionDigits: 2 })

onMounted(fetchThreads)
</script>

<style scoped>
.messages-page {
  background: #f8fafc;
  min-height: 100vh;
  padding: 24px;
}

.messages-layout {
  max-width: 1000px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 280px 1fr;
  height: calc(100vh - 108px);
  background: white;
  border-radius: 12px;
  border: 1px solid #e5e7eb;
  overflow: hidden;
}

/* Sidebar */
.thread-sidebar {
  border-right: 1px solid #e5e7eb;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e5e7eb;
}

.sidebar-header h2 {
  font-size: 16px;
  font-weight: 600;
  color: #003366;
}

.search-box {
  padding: 10px 12px;
  border-bottom: 1px solid #e5e7eb;
}

.search-box input {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  font-size: 13px;
  outline: none;
  background: #f8fafc;
}

.thread-list { overflow-y: auto; flex: 1; }

.thread-item {
  display: flex;
  gap: 10px;
  padding: 12px 14px;
  cursor: pointer;
  border-bottom: 1px solid #f5f5f5;
  align-items: flex-start;
  transition: background 0.15s;
}

.thread-item:hover { background: #f0f4ff; }
.thread-item.active { background: #e8f0fe; }

.avatar {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  background: #003366;
  color: #FFD700;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  font-size: 14px;
  flex-shrink: 0;
}

.thread-info { flex: 1; min-width: 0; }

.thread-top {
  display: flex;
  justify-content: space-between;
  margin-bottom: 2px;
}

.thread-name { font-size: 13px; font-weight: 600; color: #1a1a1a; }
.thread-time { font-size: 11px; color: #999; }
.thread-preview { font-size: 12px; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }

.unread-dot {
  width: 8px;
  height: 8px;
  background: #003366;
  border-radius: 50%;
  flex-shrink: 0;
  margin-top: 6px;
}

.empty-threads { padding: 20px; text-align: center; color: #999; font-size: 13px; }

/* Chat Window */
.chat-window { display: flex; flex-direction: column; }

.chat-header {
  padding: 12px 16px;
  border-bottom: 1px solid #e5e7eb;
  display: flex;
  align-items: center;
  gap: 10px;
}

.chat-partner-name { font-size: 14px; font-weight: 600; color: #003366; }
.chat-status { font-size: 12px; color: #22c55e; }

.product-context {
  display: flex;
  gap: 10px;
  align-items: center;
  padding: 10px 16px;
  background: #f8fafc;
  border-bottom: 1px solid #e5e7eb;
}

.product-thumb {
  width: 40px;
  height: 40px;
  object-fit: cover;
  border-radius: 6px;
}

.product-context-title { font-size: 13px; font-weight: 500; color: #1a1a1a; }
.product-context-price { font-size: 12px; color: #ee4d2d; font-weight: 600; }

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  background: #f8fafc;
}

.message-row {
  display: flex;
  flex-direction: column;
  max-width: 65%;
}

.message-row.mine { align-self: flex-end; align-items: flex-end; }
.message-row.theirs { align-self: flex-start; }

.bubble {
  padding: 10px 14px;
  border-radius: 16px;
  font-size: 13px;
  line-height: 1.5;
}

.mine .bubble {
  background: #003366;
  color: white;
  border-bottom-right-radius: 4px;
}

.theirs .bubble {
  background: white;
  color: #1a1a1a;
  border: 1px solid #e5e7eb;
  border-bottom-left-radius: 4px;
}

.msg-time { font-size: 10px; color: #999; margin-top: 3px; }

.chat-input-row {
  padding: 12px 16px;
  border-top: 1px solid #e5e7eb;
  display: flex;
  gap: 10px;
  align-items: center;
}

.chat-input-row input {
  flex: 1;
  padding: 10px 16px;
  border: 1px solid #e5e7eb;
  border-radius: 24px;
  font-size: 13px;
  outline: none;
}

.send-btn {
  width: 38px;
  height: 38px;
  background: #003366;
  border: none;
  border-radius: 50%;
  color: #FFD700;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  flex-shrink: 0;
}

/* Empty State */
.empty-chat {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #aaa;
  font-size: 14px;
  gap: 12px;
  background: #f8fafc;
}

.empty-icon { font-size: 40px; }

@media (max-width: 768px) {
  .messages-layout { grid-template-columns: 1fr; }
  .thread-sidebar { display: none; }
}
</style>