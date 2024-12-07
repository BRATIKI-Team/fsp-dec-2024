<script setup lang="ts">

import { format } from 'date-fns';

const columns = [
  { key: 'name', label: 'Имя' },
  { key: 'email', label: 'Email' },
  { key: 'actions' },
];

const api = useApi();
const {getSession} = useAuth()
const loading = ref(false);

const page = ref(1);
const pageCount = ref(5);

const users = useState(() => ({
  items: [],
  total: 1,
}));

const updateState = async () => {
  loading.value = true;
  const me = await getSession()
  const reqs = await api.member_reqs.all(me?.region.id);
  loading.value = false;
  return {
    items: events.items.map(i => {
      const datetime = format(i.event.start_date, 'dd.MM.yyyy') + " - " + format(i.event.end_date, 'dd.MM.yyyy')
      return {
        ...i.event,
        datetime: datetime,
        region: i.region?.name,
        regionEmail: i.region?.contacts.email,
      }
    }),
    total: events.total,
  };
}

definePageMeta({
  layout: 'lk',
});
</script>

<template>
  <h1 class="mb-8 text-4xl font-bold">Заявки</h1>
  <div
    class="divide-y divide-gray-200 rounded-2xl shadow-md dark:divide-gray-700">
    <div class="flex items-center justify-between gap-3 px-4 py-3">
      <div class="flex items-center gap-1.5">
        <span class="text-sm leading-5">Rows per page:</span>

        <USelect
          class="me-2 w-20"
          v-model="pageCount"
          :options="[3, 5, 10, 20, 30, 40]"
          size="xs" />
      </div>
      <NuxtLink href="/lk/events/add">
        <UButton class="h-7 w-7 rounded-full p-2">
          <UIcon class="h-5 w-5 cursor-pointer" name="i-heroicons-plus" />
        </UButton>
      </NuxtLink>
    </div>
    <UTable
      :rows="users.items"
      :columns="columns"
      :loading="loading"
      :progress="{ color: 'primary', animation: 'carousel' }">
      <template #actions-data="{ row }"> </template>
      <template #empty-state>
        <div class="flex flex-col items-center justify-center gap-3 py-6">
          <span class="text-sm italic">Нет новых заявок на вступление.</span>
        </div>
      </template>
    </UTable>

    <div
      class="flex justify-end border-t border-gray-200 px-3 py-3.5 dark:border-gray-700">
      <UPagination
        v-model="page"
        :page-count="pageCount"
        :total="users.total" />
    </div>
  </div>
</template>

<style scoped></style>