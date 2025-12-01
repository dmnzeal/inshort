<script setup lang="ts">
import 'normalize.css';
import '@fontsource/poppins';
import Header from '@/components/Header.vue';
</script>

<template>
  <Header />
  <main>
    <div class="container">
      <router-view />
    </div>
  </main>
</template>

<style>
body {
  font-family: 'Poppins', sans-serif;
  color: #353839;
}
.container {
  max-width: 1024px;
  margin-left: auto;
  margin-right: auto;
  padding: 1rem;
}
a {
  color: #008000;
}
</style>
