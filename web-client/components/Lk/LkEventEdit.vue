<script setup lang="ts">
import { date, type InferType, number, object, string } from 'yup';
import type { Form, FormSubmitEvent } from '#ui/types';

const schema = object({
  name:  string().required(),
  description:  string().required(),
  dateStart:  date().required(),
  dateEnd:  date().required(),
  num:  number().required(),
  location:  string().required(),
})
type Schema = InferType<typeof schema>
const state = reactive({
  name: '',
  description: '',
  dateStart: '',
  dateEnd: '',
  num: 0,
  location: ''
})

const form = ref<Form<Schema>>()

const loading = ref(false)
async function onSubmit(event: FormSubmitEvent<Schema>) {
  loading.value = true
  form.value!.clear()
  try {

  } catch (err) {

  }
}

</script>

<template>
  <UForm ref="form" class="shadow-md rounded-2xl px-16 py-14" :schema="schema" :state="state"   @submit="onSubmit">
    <UFormGroup label="Название" name="name" class="mb-6">
      <UInput v-model="state.name"  input-class="shadow-none text-xl" />
    </UFormGroup>
    <UFormGroup label="Описание" name="description">
      <UTextarea v-model="state.description" resize textarea-class="shadow-none" />
    </UFormGroup>
  </UForm>
</template>

<style scoped>

</style>