<template>
  <UHeader :links="links">
    <template #logo>
      <NuxtImg class="h-8" src="header_logo.png" />
    </template>

    <template #right>
      <UColorModeButton />
      <UButton
        icon="i-heroicons-arrow-right-start-on-rectangle"
        color="gray"
        variant="ghost" />
    </template>
  </UHeader>

  <UMain>
    <ULandingGrid>
      <slot />
    </ULandingGrid>
  </UMain>

  <ULandingGrid
    class="bg-background mt-8 border-t border-gray-200 p-8 dark:border-gray-800">
    <div
      class="flex justify-between lg:col-span-10 lg:col-start-2 xl:col-span-8 xl:col-start-3">
      <NuxtImg class="hidden h-24 dark:block" src="footer_logo.png" />
      <div class="flex flex-col">
        <div class="text-sm text-gray-800 dark:text-gray-400">Контакты</div>
        <div>info@fsp-russia.com</div>
        <div>125047, г. Москва</div>
        <div>2-я Брестская, д. 8, этаж 9</div>
      </div>
      <div class="flex flex-col">
        <div class="text-sm text-gray-800 dark:text-gray-400">Пресс-служба</div>
        <div>press@fsp-russia.com</div>
      </div>
      <div class="flex flex-col">
        <div class="text-sm text-gray-800 dark:text-gray-400">
          Социальные сети
        </div>
        <div>vk.com/russiafsp</div>
        <div>t.me/fsprussia</div>
      </div>
    </div>
  </ULandingGrid>
</template>

<script setup lang="ts">
const links = [
  {
    label: 'О нас',
    icon: 'i-heroicons-book-open',
    to: '/faq',
  },
  {
    label: 'Афиша',
    icon: 'i-heroicons-calendar-days',
    to: '/events',
  },
  {
    label: 'Представительства',
    icon: 'i-heroicons-user-group',
    to: '/regions',
  },
];
</script>
