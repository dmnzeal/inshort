<script setup lang="ts">
import { ref } from 'vue';

import api from '@/services/api';

const username = ref('');
const password = ref('');
const message = ref('');

async function register() {
  try {
    const res = await api.post('/users/register', {
      username: username.value,
      password: password.value,
    });
    message.value = res.data;
  } catch {
    message.value = 'Что-то пошло не так';
  }
}
</script>

<template>
  <div class="wrapper">
    <h1>Регистрация</h1>
    <form @submit.prevent>
      <input v-model="username" type="text" placeholder="Логин" />
      <input v-model="password" type="password" placeholder="Пароль" />
      <button @click="register">Зарегистрироваться</button>
    </form>
    <p>
      <small>
        Уже есть аккаунт?
        <router-link to="/login">Войти</router-link>
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
