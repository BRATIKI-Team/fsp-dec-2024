<script setup lang="ts">
const { user, isAdmin } = await useUser();

definePageMeta({
  layout: 'lk',
  middleware: ['auth'],
});

</script>

<template>
  <h1 class="text-4xl font-bold mb-8">События</h1>
  <LkAdminEventList v-if="isAdmin"/>
  <LkEventList v-else/>
</template>

<style scoped>

</style>