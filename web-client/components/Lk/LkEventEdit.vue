<script setup lang="ts">
import { date, type InferType, number, object, string } from 'yup';
import { sub, format, isSameDay, type Duration } from 'date-fns';
import type { Form, FormSubmitEvent } from '#ui/types';
import type { IEvent } from '~/types/dtos/event';

const api = useApi();
const route = useRoute()

const props = withDefaults(defineProps<{
  event?: IEvent
}>(), {});

const disciplines = [
  'Продуктовое программирование'
]

const schema = object({
  name: string().required(),
  description: string().required(),
  participants_count: number().min(1).required(),
  discipline: string().required(),
  location: string().required(),
});
type Schema = InferType<typeof schema>
const state = reactive({
  name: props.event?.name || '',
  discipline: props.event?.discipline || '',
  description: props.event?.description || '',
  participants_count: 1,
  location: props.event?.location || '',
});
const selected = ref({ start: sub(new Date(), { days: 14 }), end: new Date() });

type File = {
  id: string,
  name: string
}
const files = ref<File[]>(props.event?.documents_ids.length ? props.event?.documents_ids.map(i => ({
  id: i,
  name: i,
})) : []);

const protocols = ref<File[]>(props.event?.protocols_ids.length ? props.event?.protocols_ids.map(i => ({
  id: i,
  name: i,
})) : []);

const notification = ref({
  show: props.event != undefined && route.query.new == '1',
  title: 'Успешно',
  description: 'Вы успешно добавили событие!',
  icon: 'i-heroicons-check-circle !w-8 !h-8 text-green-500'
})
const form = ref<Form<Schema>>();

const loading = ref(false);

async function onSubmit(event: FormSubmitEvent<Schema>) {
  loading.value = true;
  form.value!.clear();
  try {


    if (!props.event) {
      const res = await api.events.create({
        name: event.data.name,
        discipline: event.data.discipline,
        description: event.data.description,
        start_date: selected.value.start.toISOString(),
        participants_count: event.data.participants_count,
        location: event.data.location,
        end_date: selected.value.end.toISOString(),
        documents_ids: files.value.map(i => i.id),
        protocols_ids: protocols.value.map(i => i.id),
      });
      notification.value = {
        show: true,
        title: 'Успешно',
        description: 'Вы успешно добавили событие!',
        icon: 'i-heroicons-check-circle !w-8 !h-8 text-green-500'
      }
      setTimeout(() => notification.value.show = false, 3000)
      await navigateTo(`/lk/events/${res.id}?new=1`)
    } else {
      const res = await api.events.update(props.event?.id, {
        name: event.data.name,
        discipline: event.data.discipline,
        description: event.data.description,
        start_date: selected.value.start.toISOString(),
        end_date: selected.value.end.toISOString(),
        participants_count: event.data.participants_count,
        location: event.data.location,
        documents_ids: files.value.map(i => i.id),
        protocols_ids: protocols.value.map(i => i.id),
      });
      notification.value = {
        show: false,
        title: 'Успешно',
        description: 'Вы успешно обновили событие!',
        icon: 'i-heroicons-check-circle !w-8 !h-8 text-green-500'
      }
      notification.value.show = true
      setTimeout(() => notification.value.show = false, 3000)
    }
  } catch (err) {
    console.error(err)
    notification.value = {
      show: true,
      title: 'Ошибка',
      description: 'Произошла непредвиденная ошибка',
      icon: 'i-heroicons-exclamation-circle !w-8 !h-8 text-red-500'
    }
    setTimeout(() => notification.value.show = false, 3000)
  } finally {
    loading.value = false;
  }
}



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
  <UForm ref="form" class="shadow-md rounded-2xl px-16 py-14" :schema="schema" :state="state" @submit="onSubmit">
    <UFormGroup label="Название" name="name" class="mb-6">
      <UInput v-model="state.name" input-class="shadow-none text-xl" />
    </UFormGroup>
    <UFormGroup label="Описание" name="description" class="mb-6">
      <UTextarea v-model="state.description" resize textarea-class="shadow-none" />
    </UFormGroup>

    <div class="flex mb-6">
      <div class="w-1/2 mr-6">
        <UPopover :popper="{ placement: 'bottom-start' }">
          <UFormGroup label="Даты проведения" class="w-full" style="margin-top: -2.4px">
            <div
              class="relative block w-full disabled:cursor-not-allowed disabled:opacity-75 focus:outline-none border-0 form-input rounded-md placeholder-gray-400 dark:placeholder-gray-500 text-sm px-2.5 py-1.5 shadow-sm bg-white dark:bg-gray-900 text-gray-900 dark:text-white ring-1 ring-inset ring-gray-300 dark:ring-gray-700 focus:ring-2 focus:ring-primary-500 dark:focus:ring-primary-400">
              {{ format(selected.start, 'dd.MM.yyyy') }} - {{ format(selected.end, 'dd.MM.yyyy') }}
            </div>
          </UFormGroup>

          <template #panel="{ close }">
            <div class="flex items-center sm:divide-x divide-gray-200 dark:divide-gray-800">
              <DatePicker v-model="selected" @close="close" />
            </div>
          </template>
        </UPopover>
      </div>
      <div class="w-1/2">
        <UFormGroup label="Количество участников" name="num">
          <UInput v-model="state.participants_count" textarea-class="shadow-none" />
        </UFormGroup>

      </div>
    </div>
    <div class="flex mb-10">
      <div class="w-1/2 mr-6">
        <UFormGroup label="Локация" name="location" class="mb-10">
          <UInput v-model="state.location" textarea-class="shadow-none" />
        </UFormGroup>
      </div>
      <div class="w-1/2">
        <UFormGroup label="Дисциплина" name="discipline" class="mb-10">
          <USelectMenu v-model="state.discipline" :options="disciplines" select-class="shadow-none" />
        </UFormGroup>

      </div>
    </div>


    <h3 class="mb-3 text-lg font-bold">Документы</h3>
    <client-only>
      <div class="mb-8">
        <UFileUpload v-model="files" />
      </div>
    </client-only>

    <h3 class="mb-3 text-lg font-bold">Протокол</h3>
    <client-only>
      <div class="mb-8">
        <UFileUpload v-model="protocols" :multiple="false" />
      </div>
    </client-only>

    <div class="flex items-center">
      <UButton type="submit" :loading="loading" class="mr-4">Сохранить</UButton>
      <!--      <UButton variant="secondary">Отправить в ЕКП</UButton>-->

    </div>
  </UForm>


</template>

<style scoped>

</style>