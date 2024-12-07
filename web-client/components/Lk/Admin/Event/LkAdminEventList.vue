<script setup lang="ts">
import { format } from 'date-fns';

const columns = [
  { key: 'datetime', label: 'Дата' },
  { key: 'name', label: 'Мероприятие' },
  { key: 'person', label: 'Представитель' },
  { key: 'region', label: 'Представительство' },
  { key: 'actions' },
];
const notification = ref({
  show: false,
  title: '',
  description: '',
  icon: 'i-heroicons-check-circle !w-8 !h-8 text-green-500',
});

type Request = {
  datetime: string,
  event_id: string,
  person: string,
  region_id: string,
  name: string,
  id: string,
  region: string,
  status: string
}

const api = useApi();
const loading = ref(false);
const declinedEvent = ref<Request|null>(null);
const declineReason = ref("")

const requests = useState<Array<Request>>(() => []);

const updateState = async () => {
  loading.value = true;
  const reqs = await api.events.requests.all();
  loading.value = false;
  return reqs.map(i => {
    const datetime = format(i.event.start_date, 'dd.MM.yyyy') + ' - ' + format(i.event.end_date, 'dd.MM.yyyy');
    return {
      id: i.id,
      region_id: i.region.id,
      event_id: i.event.id,
      status: i.status,
      datetime: datetime,
      name: i.event.name,
      person: i.region.person,
      region: i.region.subject,
    };
  });
};

onMounted(async () => {
  requests.value = await updateState();
});

const changeStatus = async (row: any, status: string) => {


  switch (status) {
    case 'approved':
      await api.events.requests.change_status(row.id, {
        id: row.id,
        event_id: row.event_id,
        region_id: row.region_id,
        status: status,
        canceled_reason: '',
      });
      notification.value = {
        show: true,
        title: 'Успешно',
        description: 'Вы успешно приняли пользователя!',
        icon: 'i-heroicons-check-circle !w-8 !h-8 text-green-500',
      };
      const rowIdx = requests.value.findIndex(i => i.id == row.id);
      requests.value.splice(rowIdx, 1);
      break;
    case 'declined':
      declinedEvent.value = row;

      break;
  }
  setTimeout(() => notification.value.show = false, 3000);
};

const decline = async () => {
  const row = declinedEvent.value as Request
  await api.events.requests.change_status(row.id as string, {
    id: row.id,
    event_id: row.event_id,
    region_id: row.region_id,
    status: 'declined',
    canceled_reason: declineReason.value,
  });
  const rowIdx = requests.value.findIndex(i => i.id == declinedEvent.value?.id);
  requests.value.splice(rowIdx, 1);
  notification.value = {
    show: true,
    title: 'Отклонен',
    description: 'Заявка пользователя отклонена',
    icon: 'i-heroicons-exclamation-circle !w-8 !h-8 text-red-500',
  };
  setTimeout(() => notification.value.show = false, 3000);
  declinedEvent.value = null
}

definePageMeta({
  layout: 'lk',
});
</script>

<template>
  <UAlert
    class="fixed top-12 right-12 max-w-md transition shadow"
    :class="{
      'opacity-1': notification.show,
      'opacity-0': !notification.show,
    }"
    :icon="notification.icon"
    :description="notification.description"
    :title="notification.title"
    @close="notification.show = false"
    :close-button="{ icon: 'i-heroicons-x-mark-20-solid', color: 'gray', variant: 'link', padded: false }"
  />
  <UModal :model-value="declinedEvent != null">
    <UCard :ui="{ ring: '', divide: 'divide-y divide-gray-100 dark:divide-gray-800' }">
      <template #header>
        <div class="flex items-center justify-between">
          <h3 class="text-base font-semibold leading-6 text-gray-900 dark:text-white">
            Отмена осбытия
          </h3>
          <UButton color="gray" variant="ghost" icon="i-heroicons-x-mark-20-solid" class="-my-1" @click="declinedEvent = null" />
        </div>
      </template>


      <UFormGroup label="Напишите почему вы откланили событие:">
        <UTextarea v-model="declineReason"/>
      </UFormGroup>

      <template #footer >
        <div class="flex justify-end">
          <UButton @click="decline">Отклонить</UButton>
        </div>
      </template>
    </UCard>
  </UModal>
  <div
    class="rounded-2xl shadow-md">

    <UTable
      :rows="requests"
      :columns="columns"
      :loading="loading"
      :progress="{ color: 'primary', animation: 'carousel' }">
      <template #actions-data="{ row }">
        <div class="flex">
          <UIcon @click="changeStatus(row, 'approved')" name="i-heroicons-check"
                 class="w-5 h-5 text-green-500 hover:text-green-600 cursor-pointer mr-2" />
          <UIcon @click="changeStatus(row, 'declined')" name="i-heroicons-no-symbol"
                 class="w-5 h-5 text-red-500 hover:text-red-600 cursor-pointer" />
        </div>
      </template>
      <template #empty-state>
        <div class="flex flex-col items-center justify-center gap-3 py-6">
          <span class="text-sm italic">Нет новых заявок на ЕКП.</span>
        </div>
      </template>
    </UTable>
  </div>
</template>

<style scoped></style>