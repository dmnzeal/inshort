import { createApp } from 'vue';
import { createPinia } from 'pinia';

import App from './App.vue';
import router from './router';
import { useAuthStore } from './stores/auth';

const app = createApp(App);

app.use(createPinia());

const auth = useAuthStore();
const accessToken = localStorage.getItem('access_token');
if (accessToken) {
  auth.accessToken = accessToken;
}

app.use(router);

app.mount('#app');
