<template>
  <div class="grid h-screen grid-cols-8 grid-rows-1">
    <UCard
      class="flex flex-col items-center justify-center sm:col-span-8 lg:col-span-3 lg:col-start-2">
      <slot />
    </UCard>
  </div>
</template>
