<script setup lang="ts">
import { ref, onMounted } from 'vue';

const message = ref<string>('');

onMounted(async () => {
  try {
    const response = await fetch('/api/data');
    const data: { message: string } = await response.json();
    message.value = data.message;
  } catch (error) {
    console.error('Error fetching data:', error);
  }
});
</script>

<template>
  <main>
    <header>
      <input placeholder="Type here">
      <button @click="">pesquisar</button>
    </header>
  </main>
  <div>
    <h1>{{ message }}</h1>
  </div>
</template>

<style scoped>
header {
  line-height: 1.5;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }
}
</style>
