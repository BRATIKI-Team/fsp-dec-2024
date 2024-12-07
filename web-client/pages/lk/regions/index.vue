<script setup lang="ts">
const {isAdmin} = await useUser()
import { bool, type InferType, object, string } from 'yup';
import type { Form, FormSubmitEvent } from '#ui/types';

if (!isAdmin) {
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
  name: string().required(),
  subject: string().required(),
  is_main: bool(),
});
type Schema = InferType<typeof schema>
const state = reactive({
  name: "",
  subject: "",
  is_main: false
});

const form = ref<Form<Schema>>();

const loading = ref(false);
const region = ref(options[0])

async function onSubmit(data: FormSubmitEvent<Schema>) {
  loading.value = true;
  form.value!.clear();
  try {
    await api.regions.create({
      name: data.data.name,
      subject: data.data.subject,
      is_main: data.data.is_main,
    })
    notification.value = {
      show: true,
      title: 'Успешно',
      description: 'Вы успешно создали представительство',
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
    <UFormGroup label="Название" name="subject" class="mb-6">
      <UInput v-model="state.subject"  input-class="shadow-none" />
    </UFormGroup>
    <UFormGroup label="Регион или округ" name="name" class="mb-6">
      <UInput v-model="state.name"  input-class="shadow-none" />
    </UFormGroup>
    <UCheckbox v-model="state.is_main" name="is_main" label="Является центральным представительством" class="mb-6" />
    <UButton :loading="loading" type="submit">Сохранить</UButton>
  </UForm>
</template>

<style scoped>

</style>