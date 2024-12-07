<script setup lang="ts">
import useLoading from '~/composables/useLoading';
import { format } from 'date-fns';

const auth = useAuth();

const me = await auth.getSession();
const columns = [
  { key: 'datetime', label: 'Дата' },
  { key: 'name', label: 'Название' },
  { key: 'region', label: 'Представительство' },
  { key: 'regionEmail', label: 'Представитель' },
  { key: 'actions' },
];

const api = useApi();
const loading = ref(false);

const page = ref(1);
const pageCount = ref(5);

const updateState = async () => {
  loading.value = true;
  const events = await api.events.search({
    page: page.value,
    page_size: pageCount.value,
    criteria: [
      {
        field: 'region_id',
        // @ts-ignore
        value: [me.region.id],
      },
    ],
  });
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

const events = await useState(() => ({
  items: [],
  total: 0
}));
onMounted(async () => {
  events.value = await updateState()
})
watch(page, async () => {
  events.value = await updateState()
});
watch(pageCount, async () => {
  events.value = await updateState()
});


definePageMeta({
  layout: 'lk',
  middleware: ['auth'],
});

const items = (row: any) => [
  [{
    label: 'Edit',
    icon: 'i-heroicons-pencil-square',
    click: () => navigateTo(`/lk/events/${row.id}`),
  }], [{
    label: 'Удалить',
    icon: 'i-heroicons-trash',
    click: () => {

    }
  }],
];

</script>

<template>
  <h1 class="text-4xl font-bold mb-8">События</h1>

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
    <UTable :rows="events.items" :columns="columns" :loading="loading"
            :progress="{ color: 'primary', animation: 'carousel' }">
      <template #actions-data="{ row }">
        <UDropdown :items="items(row)">
          <UButton color="gray" variant="ghost" icon="i-heroicons-ellipsis-horizontal-20-solid" />
        </UDropdown>
      </template>
      <template #empty-state>
        <div class="flex flex-col items-center justify-center py-6 gap-3">
          <span class="italic text-sm">Ничего нет!</span>
          <NuxtLink href="/lk/events/add">
            <UButton label="Добавить событие" />
          </NuxtLink>
        </div>
      </template>
    </UTable>

    <div class="flex justify-end px-3 py-3.5 border-t border-gray-200 dark:border-gray-700">
      <UPagination v-model="page" :page-count="pageCount" :total="events.total" />
    </div>
  </div>
</template>

<style scoped>

</style>