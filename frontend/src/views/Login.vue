<script setup lang="ts">
import { ref } from 'vue';

import { useAuthStore } from '@/stores/auth';
import router from '@/router';

const username = ref('');
const password = ref('');
const message = ref('');

async function register() {
  try {
    const auth = useAuthStore();
    await auth.login(username.value, password.value);
    router.push('/');
  } catch {
    message.value = 'Что-то пошло не так';
  }
}
</script>

<template>
  <div class="wrapper">
    <h1>Вход</h1>
    <form @submit.prevent>
      <input v-model="username" type="text" placeholder="Логин" />
      <input v-model="password" type="password" placeholder="Пароль" />
      <button @click="register">Войти</button>
    </form>
    <p>
      <small>
        Ещё нет аккаунта?
        <router-link to="/register">Зарегистрироваться</router-link>
      </small>
    </p>
    <p>
      <small v-if="message">
        Ответ: <br />
        {{ message }}
      </small>
    </p>
  </div>
</template>

<style scoped>
@import '@/assets/styles/auth.css';
</style>
