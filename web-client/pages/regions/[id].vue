<script setup lang="ts">
import { useAsyncData, useRouter } from '#app';
import useLoading from '~/composables/useLoading';
import { definePageMeta } from '#imports';
import type { IRegion } from '~/types/dtos/region';

definePageMeta({
  auth: true,
  layout: 'grid',
});

const router = useRouter();
const route = useRoute();
const api = useApi();
const loading = useLoading();

const { data } = await useAsyncData<IRegion>('region_detail', async () => {
  loading.on_load_start();
  return await api.regions.find(route.params.id.toString()).then(
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
</script>

<template>
  <div
    class="mt-8 flex flex-col lg:col-span-10 lg:col-start-2 xl:col-span-8 xl:col-start-3">
    <UCard v-if="data">
      <div class="flex flex-col gap-4">
        <div class="flex items-center gap-4">
          <UButton
            @click="go_back()"
            icon="i-heroicons-arrow-long-left"
            variant="outline"
            size="xl" />
          <div class="text-4xl font-semibold">{{ data.subject }}</div>
        </div>

        <div class="text-2xl">
          {{ data.name }}
        </div>

        <div class="mt-8 flex flex-col gap-4">
          <div>Контакты:</div>
          <div class="flex items-center gap-4" v-if="data.contacts.phone">
            <UIcon class="h-8 w-8" name="i-heroicons-phone" />
            <div>{{ data.contacts.phone }}</div>
          </div>
          <div class="flex items-center gap-4">
            <UIcon class="h-8 w-8" name="i-heroicons-inbox" />
            <div>{{ data.contacts.email }}</div>
          </div>
        </div>

        <NuxtLink
          class="mt-8 flex flex-col gap-4 underline"
          :href="'/events?region=' + data.id"
          >Все события
        </NuxtLink>
      </div>
    </UCard>
  </div>
</template>
