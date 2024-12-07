<script setup lang="ts">
import { definePageMeta } from '#imports';
import type {
  ICriterion,
  ISearchRequest,
  ISearchResponse,
} from '~/types/dtos/search';
import type { IEventDetail } from '~/types/dtos/event';
import useLoading from '~/composables/useLoading';
import useApi from '~/composables/useApi';
import Autocomplete_disciplines from '~/components/autocomplete_disciplines.vue';
import Autocomplete_regions from '~/components/autocomplete_regions.vue';

definePageMeta({
  auth: true,
  layout: 'grid',
});

const api = useApi();
const loading = useLoading();

const disciplines_filter = ref<string | undefined>();
const regions_filter = ref<string | undefined>();

const response_state = useState<ISearchResponse<IEventDetail>>(
  'events_response',
  () => ({
    page: 0,
    page_size: 10,
    items: [],
    more: false,
  })
);
const request_state = useState<ISearchRequest>('events_request', () => ({
  page: 1,
  page_size: 10,
  criteria: [],
}));

const search = () => {
  if (loading.in_progress.value) {
    return;
  }

  loading.on_load_start();

  api.events.search(request_state.value).then(
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

const event_features = (item: IEventDetail) =>
  [item.region?.name, item.event.discipline].filter(
    (x): x is string => x !== undefined
  );

watch(
  () => [regions_filter.value, disciplines_filter.value],
  () => {
    const criteria: readonly ICriterion[] = [
      {
        field: 'regions',
        value: [regions_filter.value],
      },
      {
        field: 'disciplines',
        value: [disciplines_filter.value],
      },
    ].filter((item): item is ICriterion => !item.value.includes(undefined));

    request_state.value = {
      page: 1,
      page_size: 10,
      criteria: criteria,
    };

    response_state.value = {
      page: 0,
      page_size: 10,
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
    <UAccordion
      :items="[
        { label: 'Фильтры', icon: 'i-heroicons-adjustments-horizontal' },
      ]">
      <template #item>
        <div class="flex flex-col gap-3">
          <autocomplete_disciplines v-model="disciplines_filter" />
          <autocomplete_regions v-model="regions_filter" />
        </div>
      </template>
    </UAccordion>

    <UPricingCard
      v-for="item in response_state.items"
      :title="item.event.name"
      :description="item.event.description"
      :price="item.event.datetime.toLocaleDateString()"
      :features="event_features(item)"
      orientation="horizontal" />

    <UCard class="text-center" v-if="response_state.items.length === 0"
      >К сожалению, здесь ничего нет :( Попробуйте поменять фильтры.
    </UCard>

    <UButton
      v-if="response_state.more"
      v-on:click="search()"
      :loading="loading.in_progress.value"
      label="Загрузить ещё..."
      variant="soft"
      block />
  </div>
</template>
