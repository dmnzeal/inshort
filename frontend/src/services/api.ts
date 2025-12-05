import { useAuthStore } from '@/stores/auth';
import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

api.interceptors.request.use(config => {
  const auth = useAuthStore();
  if (auth.accessToken) {
    config.headers.Authorization = `Bearer ${auth.accessToken}`;
  }
  return config;
});

export default api;
