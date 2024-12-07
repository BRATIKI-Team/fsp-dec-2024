<script setup lang="ts">

definePageMeta({
  layout: 'lk',
  middleware: 'auth'
})
</script>

<template>
  <h1 class="text-4xl font-bold mb-8">Новое событие</h1>
  <LkEventEdit/>
</template>

<style scoped>

</style>