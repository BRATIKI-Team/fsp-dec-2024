<template>
  <div class="relative grid h-screen grid-cols-8 grid-rows-1">
    <UCard
      class="z-10 flex flex-col items-center justify-center sm:col-span-8 lg:col-span-3 lg:col-start-2">
      <slot />
    </UCard>

    <NuxtImg
      class="absolute h-screen object-cover opacity-5 xl:w-full"
      src="bg.gif" />
  </div>
</template>
