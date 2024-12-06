<script setup lang="ts">
import type { ISearchRequest, ISearchResponse } from '~/types/dtos/search';
import type { IEvent } from '~/types/dtos/event';
import useLoading from '~/composables/useLoading';

definePageMeta({
  auth: true,
  layout: 'grid',
});

const api = useApi();
const loading = useLoading();

const response_state = useState<ISearchResponse<IEvent>>(
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

const event_features = (item: IEvent) =>
  [item.region?.name, item.discipline].filter(
    (x): x is string => x !== undefined
  );

search();
</script>

<template>
  <UPricingCard
    class="lg:col-span-10 lg:col-start-2 xl:col-span-8 xl:col-start-3"
    v-for="item in response_state.items"
    :title="item.name"
    :description="item.description"
    :price="item.datetime.toLocaleDateString()"
    :features="event_features(item)"
    orientation="horizontal" />

  <UButton
    class="lg:col-span-10 lg:col-start-2 xl:col-span-8 xl:col-start-3"
    v-if="response_state.more"
    v-on:click="search()"
    :loading="loading.in_progress.value"
    label="Загрузить ещё..."
    block />
</template>
