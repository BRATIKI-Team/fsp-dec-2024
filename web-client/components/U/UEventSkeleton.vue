<script setup lang="ts">

</script>

<template>
  <div
       class="rounded-xl divide-y divide-gray-200 dark:divide-gray-800 ring-1 ring-gray-200 dark:ring-gray-800 shadow bg-white dark:bg-gray-900 relative flex flex-col self-stretch w-full cursor-pointer hover:scale-[101%]">
    <!--v-if-->
    <div
      class="flex-1 gap-6 lg:gap-x-8 xl:gap-x-10 flex flex-col lg:grid lg:grid-cols-10 sm:p-6 p-6 lg:p-8 xl:p-10">
      <div class="lg:col-span-7">
        <div class="flex items-center gap-3">
          <USkeleton class="h-8 w-full" />
        </div>
        <div class="text-sm sm:text-base text-gray-500 dark:text-gray-400 mt-2">
          <USkeleton class="h-20 w-full" />
        </div>
        <div class="flex items-center align-center text-center w-full flex-row my-6 lg:my-8">
          <div class="flex border-gray-200 dark:border-gray-800 w-full border-t border-solid"></div><!--v-if-->
        </div>
        <div class="flex-1">
          <ul class="grid lg:grid-cols-2 text-sm gap-3">
            <li class="flex items-center gap-x-3 min-w-0">
              <USkeleton class="h-4 w-full" />
            </li>
            <li class="flex items-center gap-x-3 min-w-0">
              <USkeleton class="h-4 w-full" />
            </li>
          </ul>
        </div>
      </div><!--v-if-->
      <div
        class="flex flex-col lg:items-center justify-center gap-y-6 lg:col-span-3 border-t lg:border-l lg:border-t-0 border-gray-200 dark:border-gray-800 pt-6 lg:pt-0 lg:pl-8 xl:pl-10 w-full">
        <div class="w-full flex lg:block">
          <USkeleton class="h-12 w-full mr-0 lg:mb-2 lg:mr-0"/>
          <USkeleton class="h-12 w-full"/>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>

</style>