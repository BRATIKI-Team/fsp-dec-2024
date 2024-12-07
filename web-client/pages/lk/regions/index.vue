<script setup lang="ts">
const {isAdmin} = await useUser()
import { type InferType, object, string } from 'yup';
import type { Form, FormSubmitEvent } from '#ui/types';
import { UserRole } from '~/types/dtos/user';

if (isAdmin) {
  navigateTo("/lk")
}
const api = useApi()
const res = await api.regions.all()

const options = res.map(i => ({
  id: i.id,
  label: i.subject
}))

const notification = ref({
  show: false,
  title: '',
  description: '',
  icon: 'i-heroicons-check-circle !w-8 !h-8 text-green-500',
});


const schema = object({
  email: string().email().required(),
  role: string().required(),
  password: string().required(),
});
type Schema = InferType<typeof schema>
const state = reactive({
  email: '',
  password: '',
  role: UserRole.MEMBER
});

const form = ref<Form<Schema>>();

const loading = ref(false);
const roles = [
  UserRole.MEMBER,
  UserRole.ADMIN,
]

const region = ref(options[0])

async function onSubmit(data: FormSubmitEvent<Schema>) {
  loading.value = true;
  form.value!.clear();
  try {
    const { id } = await api.auth.register({
      email: data.data.email,
      password: data.data.password,
    })
    await api.regions.assign(region.value.id, data.data.role, id)
    notification.value = {
      show: true,
      title: 'Успешно',
      description: 'Вы успешно создали пользователя',
      icon: 'i-heroicons-check !w-8 !h-8 text-green-500',
    };
    setTimeout(() => notification.value.show = false, 3000);
  } catch(e) {

  }
  loading.value = false
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
  <h1 class="text-4xl font-bold mb-8">Добавить представительство</h1>
  <UForm ref="form" :schema="schema" :state="state" @submit="onSubmit" class="shadow-md rounded-2xl px-16 py-14">
    <UFormGroup label="Email" name="email" class="mb-6">
      <UInput v-model="state.email"  input-class="shadow-none" />
    </UFormGroup>
    <UFormGroup label="Пароль" name="password" class="mb-6">
      <UInput v-model="state.password" type="password"  input-class="shadow-none" />
    </UFormGroup>
    <UFormGroup label="Роль" name="role" class="mb-6">
      <USelect v-model="state.role" :options="roles" input-class="shadow-none" />
    </UFormGroup>
    <UFormGroup label="Представительство" name="region" class="mb-6">
      <USelectMenu
        searchable
        searchable-placeholder="Search a person..."
        class="w-full"
        placeholder="Select a person"
        :options="options"
        v-model="region"
      />
    </UFormGroup>
    <UButton :loading="loading" type="submit">Сохранить</UButton>
  </UForm>
</template>

<style scoped>

</style>