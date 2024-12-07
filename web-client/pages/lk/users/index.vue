<script setup lang="ts">
import useLoading from '~/composables/useLoading';

const columns = [
  { key: 'name', label: 'Имя' },
  { key: 'email', label: 'Email' },
  { key: 'actions' },
];

const api = useApi();
const loading = ref(false);

const page = ref(1);
const pageCount = ref(5);


const users = useState(() => ({
  items: [],
  total: 1
}))

definePageMeta({
  layout: 'lk'
})
</script>

<template>
  <h1 class="text-4xl font-bold mb-8">Заявки</h1>
  <div class="shadow-md rounded-2xl divide-y divide-gray-200 dark:divide-gray-700">
    <div class="flex items-center justify-between gap-3 px-4 py-3">
      <div class="flex items-center gap-1.5">
        <span class="text-sm leading-5">Rows per page:</span>

        <USelect
          v-model="pageCount"
          :options="[3, 5, 10, 20, 30, 40]"
          class="me-2 w-20"
          size="xs"
        />
      </div>
      <NuxtLink href="/lk/events/add">
        <UButton class="w-7 h-7 rounded-full p-2">
          <UIcon name="i-heroicons-plus" class="w-5 h-5 cursor-pointer"/>
        </UButton>
      </NuxtLink>
    </div>
    <UTable :rows="users.items" :columns="columns" :loading="loading.in_progress.value"
            :progress="{ color: 'primary', animation: 'carousel' }">
      <template #actions-data="{ row }">

      </template>
      <template #empty-state>
        <div class="flex flex-col items-center justify-center py-6 gap-3">
          <span class="italic text-sm">Нет новых заявок на вступление.</span>
        </div>
      </template>
    </UTable>

    <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
      <UPagination v-model="page" :page-count="pageCount" :total="users.total" />
    </div>
  </div>
</template>

<style scoped>

</style>