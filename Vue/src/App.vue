<template>

<loader v-if="preloader" object="#62a0ea" color1="#ffffff" color2="#e01b24" size="3" speed="1.3" bg="#343a40" objectbg="#999793" opacity="80" disableScrolling="false" name="circular"></loader>

  <RouterView></RouterView>
</template>

<script setup>
  import { ref } from 'vue';

  let preloader = ref(true);

  window.onload = () => {
    preloader.value = !preloader.value
  }
</script>