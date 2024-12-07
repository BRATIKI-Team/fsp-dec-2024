<script setup lang="ts">
import { definePageMeta } from '#imports';
import { useAsyncData, useRoute, useRouter } from '#app';
import useLoading from '~/composables/useLoading';
import type { IEventDetail } from '~/types/dtos/event';

definePageMeta({
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

const download_file = (file_id: string) => api.files.download(file_id);
</script>

<template>
  <div
    class="mt-8 flex flex-col lg:col-span-10 lg:col-start-2 xl:col-span-8 xl:col-start-3">
    <UCard v-if="data">
      <div class="flex flex-col gap-8">
        <div class="flex items-center gap-4">
          <UButton
            v-on:click="go_back()"
            icon="i-heroicons-arrow-long-left"
            variant="outline"
            size="xl" />
          <div class="text-4xl font-semibold">{{ data.event.name }}</div>
        </div>

        <div class="flex flex-col gap-4">
          <div class="flex items-center gap-4">
            <UIcon class="h-8 w-8" name="i-heroicons-calendar-days" />
            <div class="text-xl">
              Дата проведения:
              {{
                data.event.start_date.toLocaleDateString() +
                ' - ' +
                data.event.end_date.toLocaleDateString()
              }}
            </div>
          </div>

          <div class="flex items-center gap-4" v-if="data.region">
            <UIcon class="h-8 w-8" name="i-heroicons-home-modern" />
            <span class="text-xl"
              >Представительство:
              <NuxtLink class="underline" :href="'/regions/' + data.region.id">
                {{ data.region.name }}
              </NuxtLink></span
            >
          </div>
        </div>

        <UAccordion
          v-if="data.event.description"
          size="xl"
          variant="outline"
          :items="[{ label: 'Описание' }]">
          <template #item>
            <p>{{ data.event.description }}</p>
          </template>
        </UAccordion>
        <UAccordion
          v-if="data.protocols.length !== 0"
          size="xl"
          variant="outline"
          :items="[{ label: 'Протоколы' }]">
          <template #item>
            <div class="flex flex-col">
              <UBadge
                class="cursor-pointer hover:scale-[101%]"
                v-for="file in data.results"
                size="lg"
                @click="download_file(file.id)">
                <div class="flex w-full justify-between">
                  <div>{{ file.file_name }}</div>
                  <div>{{ file.upload_at.split('T')[0] }}</div>
                </div>
              </UBadge>
            </div>
          </template>
        </UAccordion>
        <UAccordion
          v-if="data.documents.length !== 0"
          size="xl"
          variant="outline"
          :items="[{ label: 'Документы' }]">
          <template #item>
            <div class="flex flex-col">
              <UBadge
                class="cursor-pointer hover:scale-[101%]"
                v-for="file in data.results"
                size="lg"
                @click="download_file(file.id)">
                <div class="flex w-full justify-between">
                  <div>{{ file.file_name }}</div>
                  <div>{{ file.upload_at.split('T')[0] }}</div>
                </div>
              </UBadge>
            </div>
          </template>
        </UAccordion>
        <UAccordion
          v-if="data.results.length !== 0"
          size="xl"
          variant="outline"
          :items="[{ label: 'Результаты' }]">
          <template #item>
            <div class="flex flex-col">
              <UBadge
                class="cursor-pointer hover:scale-[101%]"
                v-for="file in data.results"
                size="lg"
                @click="download_file(file.id)">
                <div class="flex w-full justify-between">
                  <div>{{ file.file_name }}</div>
                  <div>{{ file.upload_at.split('T')[0] }}</div>
                </div>
              </UBadge>
            </div>
          </template>
        </UAccordion>
      </div>
    </UCard>
  </div>
</template>
