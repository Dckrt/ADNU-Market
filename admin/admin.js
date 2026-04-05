const BASE = 'http://127.0.0.1:5000/api'
const ADMIN_PASSWORD = 'adnu_admin_2024'

let allProducts = []
let allUsers = []
let allMessages = []

// ── AUTH ──────────────────────────────────────────

async function adminLogin() {
  const pw = document.getElementById('admin-password').value
  const errEl = document.getElementById('login-error')
  errEl.textContent = ''

  try {
    const res = await fetch(`${BASE}/admin/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ password: pw })
    })
    const data = await res.json()

    if (res.ok && data.success) {
      sessionStorage.setItem('admin_auth', '1')
      document.getElementById('login-screen').style.display = 'none'
      document.getElementById('dashboard').style.display = 'block'
      loadOverview()
    } else {
      errEl.textContent = data.message || 'Wrong password'
    }
  } catch (e) {
    errEl.textContent = 'Cannot connect to backend. Make sure Flask is running.'
  }
}

function logout() {
  sessionStorage.removeItem('admin_auth')
  document.getElementById('dashboard').style.display = 'none'
  document.getElementById('login-screen').style.display = 'flex'
  document.getElementById('admin-password').value = ''
}

// Allow Enter key on password field
document.getElementById('admin-password').addEventListener('keyup', (e) => {
  if (e.key === 'Enter') adminLogin()
})

// Auto-restore session
if (sessionStorage.getItem('admin_auth')) {
  document.getElementById('login-screen').style.display = 'none'
  document.getElementById('dashboard').style.display = 'block'
  loadOverview()
}

// ── TABS ──────────────────────────────────────────

function showTab(name) {
  document.querySelectorAll('.tab-content').forEach(el => el.style.display = 'none')
  document.querySelectorAll('.nav-tab').forEach(el => el.classList.remove('active'))

  document.getElementById(`tab-${name}`).style.display = 'block'
  document.querySelectorAll('.nav-tab').forEach(el => {
    if (el.getAttribute('onclick').includes(name)) el.classList.add('active')
  })

  if (name === 'products') loadProducts()
  if (name === 'users')    loadUsers()
  if (name === 'messages') loadMessages()
}

// ── OVERVIEW ──────────────────────────────────────

async function loadOverview() {
  try {
    const res = await fetch(`${BASE}/admin/stats`)
    const data = await res.json()
    document.getElementById('stat-users').textContent    = data.users ?? '—'
    document.getElementById('stat-products').textContent = data.products ?? '—'
    document.getElementById('stat-messages').textContent = data.messages ?? '—'
    document.getElementById('stat-cart').textContent     = data.cart_items ?? '—'
  } catch (e) {
    console.error('Stats error:', e)
  }

  // Recent products
  try {
    const res = await fetch(`${BASE}/admin/products`)
    const products = await res.json()
    const recent = products.slice(0, 8)
    const container = document.getElementById('recent-products')

    if (recent.length === 0) {
      container.innerHTML = '<p style="padding:1rem;color:#aaa;text-align:center">No listings yet</p>'
      return
    }

    container.innerHTML = recent.map(p => `
      <div class="recent-item">
        <img class="recent-thumb" src="${p.image_url || ''}" onerror="this.style.display='none'" />
        <div class="recent-info">
          <div class="recent-title">${escHtml(p.title)}</div>
          <div class="recent-meta">${escHtml(p.category)} · ${escHtml(p.seller_name || '—')} · ${formatDate(p.created_at)}</div>
        </div>
        <span class="recent-price">₱${Number(p.price).toLocaleString('en-PH', { minimumFractionDigits: 2 })}</span>
      </div>
    `).join('')
  } catch (e) {
    console.error('Recent products error:', e)
  }
}

// ── PRODUCTS ──────────────────────────────────────

async function loadProducts() {
  const tbody = document.getElementById('products-tbody')
  tbody.innerHTML = '<tr class="loading-row"><td colspan="9">Loading...</td></tr>'

  try {
    const res = await fetch(`${BASE}/admin/products`)
    allProducts = await res.json()
    document.getElementById('product-count').textContent = `${allProducts.length} items`
    renderProducts(allProducts)
  } catch (e) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="9">Failed to load products</td></tr>'
  }
}

function renderProducts(list) {
  const tbody = document.getElementById('products-tbody')
  if (list.length === 0) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="9">No products found</td></tr>'
    return
  }
  tbody.innerHTML = list.map(p => `
    <tr>
      <td>${p.id}</td>
      <td>
        ${p.image_url
          ? `<img class="thumb-img" src="${p.image_url}" onerror="this.style.display='none'" />`
          : '<span style="color:#ccc;font-size:1.2rem">📷</span>'
        }
      </td>
      <td class="td-title">${escHtml(p.title)}</td>
      <td><span class="cat-tag">${escHtml(p.category)}</span></td>
      <td>₱${Number(p.price).toLocaleString('en-PH', { minimumFractionDigits: 2 })}</td>
      <td><span class="status-tag status-${(p.status || '').toLowerCase()}">${escHtml(p.status)}</span></td>
      <td>${escHtml(p.seller_name || '—')}</td>
      <td>${formatDate(p.created_at)}</td>
      <td>
        <button class="del-btn" onclick="deleteProduct(${p.id}, '${escHtml(p.title)}')">
          <i class="fa-solid fa-trash"></i> Delete
        </button>
      </td>
    </tr>
  `).join('')
}

function filterProducts() {
  const q = document.getElementById('product-search').value.toLowerCase()
  const filtered = allProducts.filter(p =>
    (p.title || '').toLowerCase().includes(q) ||
    (p.seller_name || '').toLowerCase().includes(q) ||
    (p.category || '').toLowerCase().includes(q)
  )
  renderProducts(filtered)
}

async function deleteProduct(id, title) {
  if (!confirm(`Delete "${title}"?\n\nThis cannot be undone.`)) return
  try {
    const res = await fetch(`${BASE}/admin/products/${id}`, { method: 'DELETE' })
    if (res.ok) {
      allProducts = allProducts.filter(p => p.id !== id)
      renderProducts(allProducts)
      document.getElementById('product-count').textContent = `${allProducts.length} items`
      toast('Product deleted', 'success')
    } else {
      toast('Failed to delete product', 'error')
    }
  } catch (e) {
    toast('Connection error', 'error')
  }
}

// ── USERS ──────────────────────────────────────────

async function loadUsers() {
  const tbody = document.getElementById('users-tbody')
  tbody.innerHTML = '<tr class="loading-row"><td colspan="7">Loading...</td></tr>'

  try {
    const res = await fetch(`${BASE}/admin/users`)
    allUsers = await res.json()
    document.getElementById('user-count').textContent = `${allUsers.length} users`
    renderUsers(allUsers)
  } catch (e) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="7">Failed to load users</td></tr>'
  }
}

function renderUsers(list) {
  const tbody = document.getElementById('users-tbody')
  if (list.length === 0) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="7">No users found</td></tr>'
    return
  }
  tbody.innerHTML = list.map(u => `
    <tr>
      <td>${u.id}</td>
      <td class="td-title">${escHtml(u.name)}</td>
      <td class="td-email">${escHtml(u.email)}</td>
      <td>${escHtml(u.student_id || '—')}</td>
      <td style="max-width:180px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis">${escHtml(u.course || '—')}</td>
      <td>${escHtml(u.year_level || '—')}</td>
      <td>
        <button class="del-btn" onclick="deleteUser(${u.id}, '${escHtml(u.name)}')">
          <i class="fa-solid fa-trash"></i> Delete
        </button>
      </td>
    </tr>
  `).join('')
}

function filterUsers() {
  const q = document.getElementById('user-search').value.toLowerCase()
  const filtered = allUsers.filter(u =>
    (u.name || '').toLowerCase().includes(q) ||
    (u.email || '').toLowerCase().includes(q) ||
    (u.student_id || '').toLowerCase().includes(q)
  )
  renderUsers(filtered)
}

async function deleteUser(id, name) {
  if (!confirm(`Delete user "${name}"?\n\nThis will also delete their products, cart, and messages. This cannot be undone.`)) return
  try {
    const res = await fetch(`${BASE}/admin/users/${id}`, { method: 'DELETE' })
    if (res.ok) {
      allUsers = allUsers.filter(u => u.id !== id)
      renderUsers(allUsers)
      document.getElementById('user-count').textContent = `${allUsers.length} users`
      toast('User deleted', 'success')
    } else {
      toast('Failed to delete user', 'error')
    }
  } catch (e) {
    toast('Connection error', 'error')
  }
}

// ── MESSAGES ──────────────────────────────────────

async function loadMessages() {
  const tbody = document.getElementById('messages-tbody')
  tbody.innerHTML = '<tr class="loading-row"><td colspan="6">Loading...</td></tr>'

  try {
    const res = await fetch(`${BASE}/admin/messages`)
    allMessages = await res.json()
    document.getElementById('msg-count').textContent = `${allMessages.length} messages`
    renderMessages(allMessages)
  } catch (e) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="6">Failed to load messages</td></tr>'
  }
}

function renderMessages(list) {
  const tbody = document.getElementById('messages-tbody')
  if (list.length === 0) {
    tbody.innerHTML = '<tr class="empty-row"><td colspan="6">No messages found</td></tr>'
    return
  }
  tbody.innerHTML = list.map(m => `
    <tr>
      <td>${m.id}</td>
      <td>${escHtml(m.sender_name || m.sender_id)}</td>
      <td>${escHtml(m.receiver_name || m.receiver_id)}</td>
      <td class="td-msg" title="${escHtml(m.message)}">${escHtml(m.message)}</td>
      <td style="white-space:nowrap">${formatDate(m.sent_at)}</td>
      <td><span class="read-tag ${m.is_read ? 'read-yes' : 'read-no'}">${m.is_read ? 'Read' : 'Unread'}</span></td>
    </tr>
  `).join('')
}

function filterMessages() {
  const q = document.getElementById('msg-search').value.toLowerCase()
  const filtered = allMessages.filter(m =>
    (m.message || '').toLowerCase().includes(q) ||
    (m.sender_name || '').toLowerCase().includes(q) ||
    (m.receiver_name || '').toLowerCase().includes(q)
  )
  renderMessages(filtered)
}

// ── HELPERS ───────────────────────────────────────

function formatDate(d) {
  if (!d) return '—'
  try {
    return new Date(d).toLocaleDateString('en-PH', {
      month: 'short', day: 'numeric', year: 'numeric'
    })
  } catch { return d }
}

function escHtml(str) {
  if (!str) return ''
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
}

function toast(msg, type = '') {
  const el = document.createElement('div')
  el.className = `toast ${type}`
  el.textContent = msg
  document.body.appendChild(el)
  setTimeout(() => el.remove(), 3000)
}