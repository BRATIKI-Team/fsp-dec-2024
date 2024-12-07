<script setup lang="ts">
const route = useRoute();
const api = useApi();
const event = await api.events.find(route.params.id as string);

definePageMeta({
  layout: 'lk',
  middleware: 'auth',
});
</script>

<template>
  <h1 class="mb-8 text-4xl font-bold">Редактировать событие</h1>
  <LkEventEdit edit :event="event.event" />
</template>

<style scoped></style>