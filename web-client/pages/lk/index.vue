<script setup lang="ts">
const {isAdmin} = await useUser()
definePageMeta({
  layout: 'lk',
})
</script>

<template>
 <LkRegionEdit v-if="!isAdmin"/>
</template>

<style scoped>

</style>