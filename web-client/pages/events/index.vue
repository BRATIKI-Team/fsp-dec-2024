<script setup lang="ts">
import { definePageMeta } from '#imports';
import type {
  ICriterion,
  ICriterionStrings,
  ISearchRequest,
  ISearchResponse,
} from '~/types/dtos/search';
import type { IEventDetail } from '~/types/dtos/event';
import useApi from '~/composables/useApi';
import Autocomplete_disciplines from '~/components/autocomplete_disciplines.vue';
import Autocomplete_regions from '~/components/autocomplete_regions.vue';
import type { Badge } from '#ui/types';
import { format } from 'date-fns';

definePageMeta({ layout: 'grid' });

const api = useApi();
const loading = ref(false);
const route = useRoute();

const disciplines_filter = useState<string | undefined>(
  'events_disciplines_filter'
);
const regions_filter = useState<string | undefined>('events_regions_filter');
const range_filter = useState('events_range_filter', () => ({
  start: new Date(new Date().getFullYear(), 0, 1, 0, 0, 0, 0),
  end: new Date(new Date().getFullYear(), 11, 31),
}));
const approved_filter = useState('events_approved_filter', () => false);

const region_id = route.query.region?.toString();
if (region_id) {
  regions_filter.value = region_id;
}

const response_state = useState<ISearchResponse<IEventDetail>>(
  'events_response',
  () => ({
    total: 0,
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
  if (loading.value) {
    return;
  }

  loading.value = true;

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

      loading.value = false;
    },
    () => {
      loading.value = false;
    }
  );
};

const event_features = (item: IEventDetail) =>
  [item.region?.name, item.event.discipline].filter(
    (x): x is string => x !== undefined
  );

const event_status = (item: IEventDetail): Badge | undefined => {
  if (item.is_approved_event) {
    return { label: 'Включён в ЕКП' };
  }

  return undefined;
};

const event_date_range = (item: IEventDetail): string =>
  `${item.event.start_date.toLocaleDateString()} ${item.event.end_date.toLocaleDateString()}`;

const date_range = (range: { start: Date; end: Date }) =>
  format(range.start, 'dd.MM.yyyy') + ' - ' + format(range.end, 'dd.MM.yyyy');

const on_item_click = (item: IEventDetail) =>
  navigateTo(`/events/${item.event.id}`);

watch(
  () => [
    regions_filter.value,
    disciplines_filter.value,
    range_filter.value,
    approved_filter.value,
  ],
  () => {
    const criteria: readonly ICriterion[] = [
      ...[
        ...[
          {
            field: 'regions',
            value: [regions_filter.value],
          },
          {
            field: 'disciplines',
            value: [disciplines_filter.value],
          },
        ].filter(
          (item): item is ICriterionStrings => !item.value.includes(undefined)
        ),
        {
          field: 'daterange',
          value: {
            start: range_filter.value.start,
            end: range_filter.value.end,
          },
        },
      ],
      ...(approved_filter.value
        ? [
            {
              field: 'ekp',
              value: true,
            },
          ]
        : []),
    ];

    request_state.value = {
      page: 1,
      page_size: 10,
      criteria: criteria,
    };

    response_state.value = {
      total: 0,
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
      variant="outline"
      size="xl"
      :items="[
        { label: 'Фильтры', icon: 'i-heroicons-adjustments-horizontal' },
      ]">
      <template #item>
        <div class="flex flex-col gap-3">
          <autocomplete_disciplines v-model="disciplines_filter" />
          <autocomplete_regions v-model="regions_filter" />
          <UPopover>
            <UInput
              class="w-full"
              placeholder="Выберите промежуток времени"
              size="xl"
              :model-value="date_range(range_filter)" />

            <template #panel="{ close }">
              <DatePicker v-model="range_filter" @close="close" />
            </template>
          </UPopover>
          <div>
            <UCheckbox
              v-model="approved_filter"
              label="События ЕКП"></UCheckbox>
          </div>
        </div>
      </template>
    </UAccordion>

    <UEventSkeleton v-if="loading" />
    <UEventSkeleton v-if="loading" />
    <UEventSkeleton v-if="loading" />

    <UPricingCard
      class="cursor-pointer hover:scale-[101%]"
      v-for="item in response_state.items"
      v-on:click="on_item_click(item)"
      :badge="event_status(item)"
      :title="item.event.name"
      :description="item.event.description"
      :price="event_date_range(item)"
      :features="event_features(item)"
      :ui="{ amount: { price: 'text-xl text-center' } }"
      orientation="horizontal" />

    <UCard
      class="text-center"
      v-if="response_state.items.length === 0 && !loading"
      >К сожалению, здесь ничего нет :( Попробуйте поменять фильтры.
    </UCard>

    <UButton
      v-if="response_state.more"
      v-on:click="search()"
      :loading="loading"
      loading-icon="i-heroicons-arrow-path"
      label="Загрузить ещё..."
      variant="outline"
      size="xl"
      block />
  </div>
</template>
