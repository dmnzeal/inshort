<script setup lang="ts">
import { useAuthStore } from '@/stores/auth';
import api from '@/services/api';
import { onMounted, ref } from 'vue';

const auth = useAuthStore();
const user = ref(null);
const url = ref('');
const qrSrc = ref(null);

async function shorten() {
  const res = api.post('/shorten', { url: url.value });
}

async function generateQR() {
  const res = await api.post(
    '/qr/generate',
    { url: url.value },
    { responseType: 'blob' }
  );
  qrSrc.value = URL.createObjectURL(res.data);
}

onMounted(async () => {
  if (auth.accessToken) {
    const res = await api.get('/users/me');
    user.value = res.data;
    console.log(res.data);
    console.log(auth.accessToken);
  }
});
</script>

<template>
  <div class="wrapper" v-if="user">
    <div class="functions">
      <p>Привет, {{ user.username }}</p>
      <form @submit.prevent>
        <input
          class="input"
          v-model="url"
          type="text"
          required
          placeholder="http://example.com"
        />
        <button class="shorten" @click="shorten">сократить</button>
        <button class="qr" @click="generateQR">создать qr</button>
      </form>
      <img width="256" v-if="qrSrc" :src="qrSrc" alt="" />
    </div>
    <div class="data">
      <p>Ваши ссылки:</p>
      <ul class="list">
        <li class="item info">
          <span>Ссылка</span>Хэш<span><span>Посещения</span></span>
        </li>
        <li class="item" v-for="url in user.urls">
          <span>{{ url.url }} </span>
          <span>http://localhost:8000/{{ url.hash }} </span>
          <span>{{ url.visits }}</span>
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
.wrapper {
  display: flex;
  gap: 1rem;
}
.data {
  flex: 1;
}
form {
  display: grid;
  grid-template-areas:
    'input input'
    'shorten qr';
  grid-template-columns: 128px 128px;
  grid-template-rows: 64px 64px;
  gap: 4px;
}
.input {
  grid-area: input;
}
.shorten {
  grid-area: shorten;
}
.qr {
  grid-area: qr;
}
input {
  background: #fff;
  border: 2px solid #f0f0f0;
  padding: 1rem;
}
button {
  background: #fafafa;
  border: 2px solid #f0f0f0;
  padding: 1rem;
}

.list {
  display: flex;
  flex-direction: column;
  padding: 0;
}
.item {
  border: 2px solid #f0f0f0;
  padding: 1rem;
  display: grid;
  grid-template-columns: 1fr 1fr 100px;
}
.item.info {
  background-color: #a8dcab;
}
</style>
