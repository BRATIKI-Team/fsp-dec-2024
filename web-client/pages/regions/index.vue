<script setup lang="ts">
import { definePageMeta } from '#imports';
import type {
  ICriterion,
  ICriterionString,
  ISearchRequest,
  ISearchResponse,
} from '~/types/dtos/search';
import useLoading from '~/composables/useLoading';
import useApi from '~/composables/useApi';
import type { IRegion } from '~/types/dtos/region';

definePageMeta({ layout: 'grid' });

const api = useApi();
const loading = useLoading();

const search_term_filter = useState<string | undefined>(
  'regions_search_term_filter'
);

const response_state = useState<ISearchResponse<IRegion>>(
  'regions_response',
  () => ({
    total: 0,
    page: 0,
    page_size: 20,
    items: [],
    more: false,
  })
);
const request_state = useState<ISearchRequest>('regions_request', () => ({
  page: 1,
  page_size: 20,
  criteria: [],
}));

const search = () => {
  if (loading.in_progress.value) {
    return;
  }

  loading.on_load_start();

  api.regions.search(request_state.value).then(
    response => {
      response_state.value = {
        ...response,
        items: [...response_state.value.items, ...response.items],
      };
      request_state.value = {
        ...request_state.value,
        page: request_state.value.page + 1,
      };

      loading.on_load_end();
    },
    () => loading.on_error()
  );
};

const on_item_click = (item: IRegion) => navigateTo(`/regions/${item.id}`);

watch(
  () => [search_term_filter.value],
  () => {
    const criteria: readonly ICriterion[] = [
      {
        field: 'search',
        value: search_term_filter.value,
      },
    ].filter((item): item is ICriterionString => item.value !== undefined);

    request_state.value = {
      page: 1,
      page_size: 20,
      criteria: criteria,
    };

    response_state.value = {
      total: 0,
      page: 0,
      page_size: 20,
      items: [],
      more: false,
    };

    search();
  },
  { immediate: true }
);
</script>

<template>
  <div
    class="mt-8 flex flex-col gap-8 lg:col-span-10 lg:col-start-2 xl:col-span-8 xl:col-start-3">
    <UInput
      v-model="search_term_filter"
      placeholder="Поиск..."
      size="xl"
      icon="i-heroicons-magnifying-glass" />

    <div class="grid gap-8 sm:grid-cols-1 lg:grid-cols-2">
      <UCard
        class="cursor-pointer hover:scale-[101%] sm:col-span-2 lg:col-span-1"
        v-for="item in response_state.items"
        @click="on_item_click(item)">
        <div class="flex flex-col gap-4">
          <span class="text-xl">{{ item.subject }}</span>
          <span class="text-sm text-gray-500">{{ item.name }}</span>
        </div>
      </UCard>
    </div>

    <UCard class="text-center" v-if="response_state.items.length === 0"
      >К сожалению, здесь ничего нет :( Попробуйте поменять фильтры.
    </UCard>

    <UButton
      v-if="response_state.more"
      v-on:click="search()"
      :loading="loading.in_progress.value"
      loading-icon="i-heroicons-arrow-path"
      label="Загрузить ещё..."
      variant="outline"
      size="xl"
      block />
  </div>
</template>
