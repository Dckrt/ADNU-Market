<template>
  <div class="profile-page-container">
    <div class="profile-card shadow-lg">
      <!-- 1. Header Section: User Logo with Upload Feature -->
      <div class="profile-header">
        <div class="avatar-circle" @click="$refs.fileInput.click()" style="cursor: pointer; overflow: hidden; position: relative;">
          <!-- Displays uploaded picture if exists, otherwise shows your SVG icon -->
          <img v-if="auth.user?.profile_pic" :src="auth.user.profile_pic" style="width: 100%; height: 100%; object-fit: cover;" />
          <svg v-else viewBox="0 0 24 24" fill="currentColor" class="user-icon">
            <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z" />
          </svg>
          <!-- Hidden File Input -->
          <input type="file" ref="fileInput" @change="handlePictureUpload" accept="image/*" style="display: none;" />
        </div>
        <p class="account-type">Student Account</p>
      </div>

      <!-- 2. Details Section (Automatically populated from auth store) -->
      <div class="details-list">
        <div class="detail-item">
          <label>School Email</label>
          <span class="value">{{ auth.user?.email || 'N/A' }}</span>
        </div>

        <div class="detail-item">
          <label>Student ID Number</label>
          <span class="value">{{ auth.user?.student_id_number || '2024-XXXXX' }}</span>
        </div>

        <div class="detail-item">
          <label>Year Level</label>
          <span class="value">{{ auth.user?.year_level || 'Not Set' }}</span>
        </div>

        <div class="detail-item">
          <label>Course</label>
          <span class="value">{{ auth.user?.course || 'Not Set' }}</span>
        </div>
      </div>

      <!-- 3. Action Section -->
      <div class="action-section">
        <button @click="handleLogout" class="signout-btn">
          Log Out
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';

const auth = useAuthStore();
const router = useRouter();

// Function to handle local picture selection and display
const handlePictureUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      // Updates the user object in the store with the base64 image
      auth.user.profile_pic = e.target.result;
      // Optional: Save to localStorage so it persists on refresh
      localStorage.setItem('user', JSON.stringify(auth.user));
    };
    reader.readAsDataURL(file);
  }
};

const handleLogout = () => {
  auth.logout();
  router.push('/auth');
};
</script>

<style scoped>
.profile-page-container {
  display: flex;
  justify-content: center;
  align-items: center;
  padding-top: 60px;
  background-color: #f8fafc;
  min-height: 80vh;
}

.profile-card {
  background: white;
  width: 100%;
  max-width: 420px;
  padding: 2.5rem;
  border-radius: 24px;
  text-align: center;
  border: 1px solid #edf2f7;
}

.avatar-circle {
  width: 80px;
  height: 80px;
  background-color: #f1f5f9;
  color: #003366; /* Ateneo Blue */
  border-radius: 50%;
  margin: 0 auto 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: 2px solid #FFD700; /* Added Gold Border for consistency */
}

.user-icon { width: 45px; height: 45px; }

.account-type {
  font-size: 0.75rem;
  font-weight: 700;
  color: #94a3b8;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  margin-bottom: 2rem;
}

.details-list {
  text-align: left;
  border-top: 1px solid #f1f5f9;
}

.detail-item {
  padding: 15px 0;
  border-bottom: 1px solid #f1f5f9;
}

.detail-item label {
  display: block;
  font-size: 0.8rem;
  color: #64748b;
  margin-bottom: 4px;
  font-weight: 500;
}

.detail-item .value {
  font-size: 1rem;
  color: #1e293b;
  font-weight: 700;
}

.action-section {
  margin-top: 2.5rem;
}

.signout-btn {
  width: 100%;
  padding: 14px;
  background-color: transparent;
  border: 2px solid #ef4444;
  color: #ef4444;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.2s ease;
}

.signout-btn:hover {
  background-color: #ef4444;
  color: white;
}
</style>
