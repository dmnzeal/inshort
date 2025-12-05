import { ref } from 'vue';
import { defineStore } from 'pinia';
import api from '@/services/api';

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref('');
  async function login(username: string, password: string) {
    const res = await api.post('/users/login', {
      username: username,
      password: password,
    });
    accessToken.value = res.data.access_token;
    localStorage.setItem('access_token', res.data.access_token);
  }

  return { accessToken, login };
});
