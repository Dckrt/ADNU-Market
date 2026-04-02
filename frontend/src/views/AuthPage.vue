<template>
  <div class="auth-wrapper">
    <div class="auth-card shadow">
      <!-- Header Section -->
      <div class="auth-header">
        <div class="logo">
        <span class="icon">🛍️</span>
        ADNU <span>Market</span>
       </div>
        <h2>{{ isLogin ? 'Welcome Back' : 'Create Account' }}</h2>
        <p class="subtitle">Ateneo de Naga University Marketplace</p>
      </div>

      <!-- Form Section -->
      <form @submit.prevent="handleSubmit" class="auth-form">
        <div class="input-group">
          <label>University Email</label>
          <input v-model="form.email" type="email" placeholder="username@gbox.adnu.edu.ph" required />
        </div>

        <!-- 1. Main Password Field with Eye -->
        <div class="input-group">
          <label>Password</label>
          <div class="password-wrapper">
            <input 
              v-model="form.password" 
              :type="showPassword ? 'text' : 'password'" 
              placeholder="••••••••" 
              required 
            />
            <button type="button" class="eye-btn" @click="showPassword = !showPassword">
              <!-- Open Eye SVG -->
              <svg v-if="showPassword" xmlns="http://www.w3.org" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
              <!-- Closed Eye SVG -->
              <svg v-else xmlns="http://www.w3.org" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
            </button>
          </div>
        </div>

        <!-- 2. Confirm Password Field with Eye (Only for Registration) -->
        <div v-if="!isLogin" class="input-group">
          <label>Confirm Password</label>
          <div class="password-wrapper">
            <input 
              v-model="form.confirmPassword" 
              :type="showConfirmPassword ? 'text' : 'password'" 
              placeholder="••••••••" 
              required 
            />
            <button type="button" class="eye-btn" @click="showConfirmPassword = !showConfirmPassword">
              <svg v-if="showConfirmPassword" xmlns="http://www.w3.org" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path><circle cx="12" cy="12" r="3"></circle></svg>
              <svg v-else xmlns="http://www.w3.org" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path><line x1="1" y1="1" x2="23" y2="23"></line></svg>
            </button>
          </div>
        </div>

        <!-- Remaining Student Details (Registration Only) -->
        <div v-if="!isLogin" class="registration-extra">
          <div class="input-group">
            <label>Full Name</label>
            <input v-model="form.name" type="text" placeholder="Juan Dela Cruz" required />
          </div>
          <div class="input-group">
            <label>Student ID Number</label>
            <input v-model="form.student_id_number" type="text" placeholder="2024-00000" required />
          </div>
          <div class="input-group">
            <label>Year Level</label>
            <select v-model="form.year_level" required>
              <option value="" disabled>Select Year</option>
              <option value="1st Year">1st Year</option>
              <option value="2nd Year">2nd Year</option>
              <option value="3rd Year">3rd Year</option>
              <option value="4th Year">4th Year</option>
            </select>
          </div>
          <div class="input-group">
            <label>Department / College</label>
            <select v-model="form.department" @change="form.course = ''" required>
              <option value="" disabled>Select College</option>
              <option v-for="(courses, dept) in departmentMap" :key="dept" :value="dept">{{ dept }}</option>
            </select>
          </div>
          <div class="input-group" v-if="form.department">
            <label>Course</label>
            <select v-model="form.course" required>
              <option value="" disabled>Select program</option>
              <option v-for="course in filteredCourses" :key="course" :value="course">{{ course }}</option>
            </select>
          </div>
        </div>

        <button type="submit" class="submit-btn" :disabled="loading">
          {{ loading ? 'Processing...' : (isLogin ? 'Login' : 'Join White Market') }}
        </button>
      </form>

      <div class="auth-footer">
        <p @click="isLogin = !isLogin" class="toggle-link">
          {{ isLogin ? "Don't have an account? Register" : "Already a member? Login" }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import api from '@/services/api'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const auth = useAuthStore()

const isLogin = ref(true)
const loading = ref(false)

const showPassword = ref(false)
const showConfirmPassword = ref(false)

const form = ref({ 
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
  student_id_number: '',
  department: '',
  course: '',
  year_level: '1st Year'
})

const departmentMap = {
  "COLLEGE OF BUSINESS AND ACCOUNTANCY": [
    "BS Accountancy",
    "BS BA Accounting Information Management",
    "BS BA Financial Management and Accounting",
    "BS Entrepreneurship with specialized track on Tourism",
    "BS Tourism Management",
    "BS BA Banking and Finance",
    "BS BA Business Economics – On Hold",
    "BS BA Business Engineering – On Hold",
    "BS BA Business Management Honors Program",
    "BS BA Hospital and Health Care Management – On Hold",
    "BS BA Legal Management",
    "BS BA Management",
    "BS BA Marketing Management"
  ],
  "COLLEGE OF COMPUTER STUDIES": [
    "Bachelor of Library and Information Science",
    "BS Computer Science",
    "BS Digital Illustration and Animation",
    "BS Information Systems",
    "BS Information Technology"
  ],
  "COLLEGE OF EDUCATION": [
    "Bachelor of Early Childhood Education",
    "Bachelor of Elementary Education",
    "Bachelor of Physical Education",
    "Bachelor of Secondary Education major in English",
    "Bachelor of Secondary Education major in Filipino",
    "Bachelor of Secondary Education major in Mathematics",
    "Bachelor of Secondary Education major in Science",
    "Bachelor of Secondary Education major in Social Studies",
    "Bachelor of Special Needs Education with specialization in Early Childhood Education",
    "Bachelor of Special Needs Education with specialization in Elementary School Teaching",
    "Bachelor of Special Needs Education – Generalist",
    "Bachelor of Special Needs Education with specialization in Teaching Deaf and Hard-of-Hearing Learners",
    "Bachelor of Special Needs Education with specialization in Teaching Learners with Visual Impairment"
  ],
  "COLLEGE OF HUMANITIES AND SOCIAL SCIENCES": [
    "AB Broadcasting – ON HOLD",
    "AB Communication",
    "AB Economics",
    "AB English Language Studies",
    "AB Journalism – ON HOLD",
    "AB Literature",
    "AB Philosophy Track 1: Teaching – On Hold",
    "AB Philosophy Track 2: Pre-Law",
    "AB Philosophy Track 3: Foreign Service/International Relations",
    "AB Political Science",
    "AB Religious and Values Education",
    "BS Development Communication",
    "BS Psychology"
  ],
  "COLLEGE OF SCIENCE AND ENGINEERING": [
    "Bachelor of Engineering Technology major in Computer Engineering Technology",
    "BS Biology",
    "BS Civil Engineering",
    "BS Architecture",
    "BS Computer Engineering",
    "BS Electronics Engineering",
    "BS Environmental Management",
    "BS Mathematics"
  ],
  "COLLEGE OF NURSING": [
    "BS Nursing"
  ]
}

const filteredCourses = computed(() => 
  form.value.department ? departmentMap[form.value.department] : []
)


const handleSubmit = async () => {

  // ✅ EMAIL VALIDATION
  if (!form.value.email.endsWith('@gbox.adnu.edu.ph')) {
    alert("Use your official ADNU GBOX email only")
    return
  }

  // 🔥 REGISTER VALIDATION (IMPORTANT FIX)
  if (!isLogin.value) {
    if (
      !form.value.name ||
      !form.value.email ||
      !form.value.password ||
      !form.value.student_id_number ||
      !form.value.department ||
      !form.value.course ||
      !form.value.year_level
    ) {
      alert("Please fill all fields ❌")
      return
    }

    if (!form.value.student_id_number.includes('-')) {
      alert("Student ID must contain '-' (example: 2024-12345)")
      return
    }

    if (form.value.password !== form.value.confirmPassword) {
      alert("Passwords do not match")
      return
    }
  }

  try {
    loading.value = true

    if (isLogin.value) {
      // 🔥 LOGIN
      const res = await api.login({
        email: form.value.email,
        password: form.value.password
      })

      console.log("LOGIN RESPONSE:", res.data)

      auth.user = res.data
      localStorage.setItem('user', JSON.stringify(res.data))

      alert("Login successful! ✅")
      router.push('/')

    } else {
      // 🔥 REGISTER
      const res = await api.register({
        name: form.value.name,
        email: form.value.email,
        password: form.value.password,
        student_id_number: form.value.student_id_number,
        course: form.value.course,
        year_level: form.value.year_level,
        department: form.value.department
      })

      console.log("REGISTER RESPONSE:", res.data)

      alert("Registered successfully! 🎉 Please login.")
      isLogin.value = true
    }

  } catch (err) {
    console.error("AUTH ERROR:", err)

    if (err.response) {
      alert(err.response.data.message || "Authentication failed ❌")
    } else {
      alert("Server not reachable ❌")
    }

  } finally {
    // 🔥 VERY IMPORTANT FIX
    loading.value = false
  }
}
</script>

<style scoped>
.auth-wrapper { min-height: 100vh; display: flex; align-items: center; justify-content: center; background-color: #003366; padding: 20px; }
.auth-card { background: white; width: 100%; max-width: 480px; padding: 2rem; border-radius: 16px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); max-height: 90vh; overflow-y: auto; }
.auth-header { text-align: center; margin-bottom: 1.5rem; }
.logo { font-size: 1.5rem; font-weight: 800; color: #003366; margin-bottom: 0.5rem; }
.logo span { color: #FFD700; }
.auth-form { display: flex; flex-direction: column; gap: 1rem; }
.input-group { display: flex; flex-direction: column; gap: 4px; text-align: left;}
.input-group label { font-size: 0.8rem; font-weight: 700; color: #003366; }

/* 4. Password Eye Layout Fixes */
.password-wrapper { position: relative; display: flex; align-items: center; }
.eye-btn { position: absolute; right: 10px; background: none; border: none; cursor: pointer; color: #666; display: flex; align-items: center; }
.eye-btn:hover { color: #003366; }

input, select { padding: 10px; border: 1px solid #ddd; border-radius: 8px; font-size: 0.95rem; width: 100%; box-sizing: border-box; }
.submit-btn { background-color: #FFD700; color: #003366; padding: 12px; border: none; border-radius: 8px; font-weight: 800; font-size: 1rem; cursor: pointer; transition: 0.3s; margin-top: 10px; }
.submit-btn:hover:not(:disabled) { background-color: #e6c200; transform: translateY(-2px); }
.auth-footer { margin-top: 1.2rem; text-align: center; font-size: 0.85rem; color: #666; }
.toggle-link { color: #003366; font-weight: bold; cursor: pointer; text-decoration: underline; }
</style>
