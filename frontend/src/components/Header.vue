<script setup lang="ts">
const isLoggedIn = localStorage.getItem('access_token') ? true : false;
</script>
<template>
  <header class="header">
    <div class="container">
      <div class="logo">
        <router-link class="link" to="/">InShort</router-link>
      </div>
      <nav class="menu">
        <router-link v-if="!isLoggedIn" class="link" to="/login"
          >Вход</router-link
        >
        <router-link v-if="isLoggedIn" class="link" to="/dashboard"
          >Главная</router-link
        >
      </nav>
    </div>
  </header>
</template>

<style scoped>
.header {
  background-color: #fafafa;
  border-bottom: 2px solid #f0f0f0;
}
.container {
  max-width: 1024px;
  height: 2rem;
  margin-left: auto;
  margin-right: auto;
  padding: 1rem;
}
.container {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.menu {
  display: flex;
  justify-content: space-around;
  align-items: center;
  gap: 1rem;
}
.link {
  text-decoration: none;
  color: #353839;
}
</style>
