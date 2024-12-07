<script setup lang="ts">
const {isAdmin} = await useUser()


definePageMeta({
  layout: 'lk',
});
</script>

<template>
  <LkAdminUserAdd v-if="isAdmin"/>
  <LkUserList v-else/>
</template>

<style scoped></style>