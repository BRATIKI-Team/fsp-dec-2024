<script setup lang="ts">
const columns = [
  { key: 'id', label: 'ID заявки' },
  { key: 'email', label: 'Email' },
  { key: 'actions' },
];
const notification = ref({
  show: false,
  title: '',
  description: '',
  icon: 'i-heroicons-check-circle !w-8 !h-8 text-green-500',
});

const api = useApi();
const { getSession } = useAuth();
const loading = ref(false);

const page = ref(1);
const pageCount = ref(5);

const me = await getSession();

const users = useState<Array<{ id: string, email: string }>>(() => []);

const updateState = async () => {
  loading.value = true;
  const reqs = await api.member_reqs.all(me?.region.id);
  loading.value = false;
  return reqs.map(i => ({
    id: i.id,
    email: i.user.email,
  }));
};

onMounted(async () => {
  users.value = await updateState();
});

const changeStatus = async (row: any, status: string) => {
  await api.member_reqs.change_status(row.id, status);
  const rowIdx = users.value.findIndex(i => i.id == row.id);
  users.value.splice(rowIdx, 1);
  switch (status) {
    case 'approved':
      notification.value = {
        show: true,
        title: 'Успешно',
        description: 'Вы успешно приняли пользователя!',
        icon: 'i-heroicons-check-circle !w-8 !h-8 text-green-500',
      };
      break;
    case 'declined':
      notification.value = {
        show: true,
        title: 'Отклонен',
        description: 'Заявка пользователя отклонена',
        icon: 'i-heroicons-exclamation-circle !w-8 !h-8 text-red-500',
      };
      break;
  }
  setTimeout(() => notification.value.show = false, 3000);
};

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
  <h1 class="mb-8 text-4xl font-bold">Заявки</h1>
  <div
    class="rounded-2xl shadow-md">

    <UTable
      :rows="users"
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
          <span class="text-sm italic">Нет новых заявок на вступление.</span>
        </div>
      </template>
    </UTable>
  </div>
</template>

<style scoped></style>