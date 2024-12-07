<script setup lang="ts">
import { definePageMeta } from '#imports';
import { useAsyncData, useRoute, useRouter } from '#app';
import useLoading from '~/composables/useLoading';
import type { IEventDetail } from '~/types/dtos/event';
import { EventRequestStatus } from '~/types/dtos/request';

definePageMeta({
  auth: true,
  layout: 'grid',
});

const router = useRouter();
const route = useRoute();
const loading = useLoading();
const api = useApi();

const { data, refresh } = await useAsyncData<IEventDetail>(
  'event_detail',
  async () => {
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
  }
);

const event_request_create = (id: string) => {
  if (loading.in_progress.value) {
    return;
  }

  loading.on_load_start();
  api.requests.create(id).then(
    response => {
      refresh();
      loading.on_load_end();
      return response;
    },
    error => {
      loading.on_error();
      return error;
    }
  );
};

const go_back = () => router.back();
const go_region = (id: string) => navigateTo(`/regions/${id}`);

const button_tooltip = (item: IEventDetail): string | undefined => {
  if (item.request === null) return 'Ваша заявка будет рассмотрена ЦП ФСП.';

  if (item.request.status === EventRequestStatus.PENDING)
    return 'Ваша заявка на рассмотрении в ЦП ФСП.';
  if (item.request.status === EventRequestStatus.DECLINED)
    return 'Ваша заявка была отклонена.';

  return undefined;
};
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

        <div class="mt-8 flex w-full">
          <div class="lg:w-full"></div>

          <UTooltip class="w-full lg:w-fit" :text="button_tooltip(data)">
            <UButton
              class="text-nowrap"
              v-if="data.request?.status !== EventRequestStatus.APPROVED"
              :loading="loading.in_progress.value"
              loading-icon="i-heroicons-arrow-path"
              @click="event_request_create(data.event.id)"
              :disabled="data.request !== null"
              block
              variant="solid"
              label="Подать заявку на внесение в ЕКП" />
          </UTooltip>
        </div>
      </div>
    </UCard>
  </div>
</template>
