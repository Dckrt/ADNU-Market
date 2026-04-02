<template>
  <div class="choice-container">
    <h1>What would you like to do today?</h1>
    <div class="grid">
      <router-link to="/products" class="choice-card buy">
        <h2>I want to BUY</h2>
        <p>Browse campus essentials</p>
      </router-link>
      <router-link to="/dashboard" class="choice-card sell">
        <h2>I want to SELL</h2>
        <p>Upload and manage items</p>
      </router-link>
    </div>
  </div>
</template>
