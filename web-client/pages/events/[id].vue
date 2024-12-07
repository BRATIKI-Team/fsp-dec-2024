<script setup lang="ts">
import { definePageMeta } from '#imports';
import { useAsyncData, useRoute, useRouter } from '#app';
import useLoading from '~/composables/useLoading';
import type { IEventDetail } from '~/types/dtos/event';

definePageMeta({
  auth: true,
  layout: 'grid',
});

const router = useRouter();
const route = useRoute();
const loading = useLoading();
const api = useApi();

const { data } = await useAsyncData<IEventDetail>('event_detail', async () => {
  loading.on_load_start();
  return await api.events.find(route.params.id.toString()).then(
    response => {
      loading.on_load_end();
      return response;
    },
    error => {
      loading.on_error();
      return error;
    }
  );
});

const go_back = () => router.back();
const go_region = (id: string) => navigateTo(`/regions/${id}`);
</script>

<template>
  <div
    class="mt-8 flex flex-col lg:col-span-10 lg:col-start-2 xl:col-span-8 xl:col-start-3">
    <UCard v-if="data">
      <div class="flex flex-col gap-4">
        <div class="flex items-center gap-4">
          <UButton
            v-on:click="go_back()"
            icon="i-heroicons-arrow-long-left"
            variant="outline"
            size="xl" />
          <div class="text-4xl font-semibold">{{ data.event.name }}</div>
        </div>

        <div class="flex items-center gap-4">
          <UIcon class="h-8 w-8" name="i-heroicons-calendar-days" />
          <div class="text-2xl">
            {{
              data.event.start_date.toLocaleDateString() +
              ' - ' +
              data.event.end_date.toLocaleDateString()
            }}
          </div>
        </div>

        <div class="flex items-center gap-4" v-if="data.region">
          <UIcon class="h-8 w-8" name="i-heroicons-home-modern" />
          <div
            class="cursor-pointer text-2xl underline"
            @click="go_region(data.region.id)">
            {{ data.region.name }}
          </div>
        </div>

        <UAccordion
          v-if="data.event.description"
          variant="outline"
          :items="[{ label: 'Описание' }]">
          <template #item>
            <p>{{ data.event.description }}</p>
          </template>
        </UAccordion>
        <UAccordion
          v-if="data.protocols.length !== 0"
          variant="outline"
          :items="[{ label: 'Положение' }]">
          <template #item></template>
        </UAccordion>

        <UButton
          class="ml-auto mt-8 w-full lg:w-fit"
          block
          variant="solid"
          label="Подать заявку на внесение в ЕКП" />
      </div>
    </UCard>
  </div>
</template>
