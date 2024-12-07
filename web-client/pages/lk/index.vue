<script setup lang="ts">
import type { IUser } from '~/types/dtos/user';
import { type InferType, object, string } from 'yup';
import type { Form, FormSubmitEvent } from '#ui/types';

const auth = useAuth()

// @ts-ignore
const region = useState(() => (auth.data.value as IUser).region)
const schema = object({
  name: string()
    .required("Введите email"),
  description: string().required(),
  phone:  string().required(),
  email:  string().required()
})
type Schema = InferType<typeof schema>
const state = reactive({
  edit: true,
  name: region.value?.name,
  description: region.value?.description,
  phone: region.value?.contacts.phone,
  email: region.value?.contacts.email,
})

const form = ref<Form<Schema>>()

const loading = ref(false)
async function onSubmit(event: FormSubmitEvent<Schema>) {
  loading.value = true
  form.value!.clear()
  try {

  } catch (err) {
    // if (err.statusCode === 422) {
    //   form.value!.setErrors(err.data.errors.map((err) => ({
    //     // Map validation errors to { path: string, message: string }
    //     message: err.message,
    //     path: err.path,
    //   })))
    // }
  }
}

definePageMeta({
  layout: 'lk',
})
</script>

<template>
  <h1 class="text-4xl font-bold mb-8">Представительство</h1>
  <UForm ref="form" class="shadow-md rounded-2xl px-16 py-14" :schema="schema" :state="state"   @submit="onSubmit">
    <div class="flex items-center justify-between">
      <h2 v-if="!state.edit" class="text-4xl font-bold mb-8">{{region?.name}}</h2>
      <div v-else class="mb-2 w-full mr-2">
        <UFormGroup label="Название" name="name">
          <UInput v-model="state.name"  input-class="shadow-none text-xl" />
        </UFormGroup>
      </div>
      <UIcon @click="state.edit = !state.edit" name="i-heroicons-pencil-square" class="w-5 h-5 cursor-pointer">
        asdasd
      </UIcon>
    </div>
    <h3 class="text-2xl font-bold mb-5">Описание</h3>

    <p v-if="!state.edit" class="mb-8">{{region.description}}</p>
    <UFormGroup  v-else name="description">
      <UTextarea v-model="state.description" resize textarea-class="shadow-none" class="mb-8"/>
    </UFormGroup>

    <h3 class="text-2xl font-bold mb-5">Контакты</h3>
    <div class="flex items-center mb-3">
      <UIcon v-if="!state.edit" name="i-heroicons-phone" class="w-5 h-5 mr-1" />
      <p  v-if="!state.edit" class="text-xl">{{region?.contacts?.phone}}</p>
      <UFormGroup v-else name="phone">
        <UInput v-model="state.phone" input-class="shadow-none" icon="i-heroicons-phone"/>
      </UFormGroup>
    </div>
    <div class="flex items-center mb-3">
      <UIcon v-if="!state.edit" name="i-heroicons-envelope" class="w-5 h-5 mr-1 mt-1" />
      <p v-if="!state.edit"  class="text-xl">{{region?.contacts.email}}</p>
     <UFormGroup v-else name="email">
       <UInput v-model="state.email" input-class="shadow-none" icon="i-heroicons-envelope"/>
     </UFormGroup>
    </div>
    <div class="flex">
      <a v-for="soc in region?.contacts.social_links" :key="soc" :href="soc">
        {{soc}}
      </a>
    </div>

    <UButton v-if="state.edit" :loading="loading" type="submit">Сохранить</UButton>
  </UForm>
</template>

<style scoped>

</style>