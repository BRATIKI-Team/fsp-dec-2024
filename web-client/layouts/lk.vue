<template>
  <header class="mx-auto px-16 shadow-md py-4 flex justify-between max-w-4xl rounded-2xl">
    <div class="flex">
      <NuxtLink href="/lk" class="flex items-center font-semibold mr-5 " :class="{'text-primary': route.path == '/lk'}">
        <UIcon name="i-heroicons-home" class="w-5 h-5 mr-1" />
        Глваная
      </NuxtLink>
      <NuxtLink href="/lk/events" class="flex items-center font-semibold mr-5" :class="{'text-primary': route.path.startsWith('/lk/events') }">
        <UIcon name="i-heroicons-calendar-days" class="w-5 h-5 mr-1" />
        События
      </NuxtLink>
      <NuxtLink href="/lk/users" class="flex items-center font-semibold" :class="{'text-primary':  route.path.startsWith('/lk/users')}">
        <UIcon name="i-heroicons-user" class="w-5 h-5 mr-1" />
        Участники
      </NuxtLink>
    </div>
    <UAvatar
      src="https://avatars.githubusercontent.com/u/739984?v=4"
      alt="Avatar"
    />
  </header>
  <main class="max-w-4xl mt-16 mx-auto">
    <slot />
  </main>
</template>
<script setup lang="ts">
const colorMode = useColorMode()
colorMode.preference = 'light'
colorMode.value = 'light'
const route = useRoute()
definePageMeta({
  middleware: ['auth']
})
</script>