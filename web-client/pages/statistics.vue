<script setup lang="ts">
import { definePageMeta } from '#imports';
import useLoading from '~/composables/useLoading';
import useApi from '~/composables/useApi';
import type { FileResponse } from '~/types/dtos/file';

definePageMeta({ layout: 'grid' });

const api = useApi();
const loading = useLoading();

const response_state = useState<readonly FileResponse[]>(
  'statistics_response',
  () => []
);

const download_file = (file_id: string) => api.statistics.download(file_id);

const search = () => {
  if (loading.in_progress.value) {
    return;
  }

  loading.on_load_start();

  api.statistics.all().then(
    response => {
      response_state.value = response;
      loading.on_load_end();
    },
    () => loading.on_error()
  );
};

if (response_state.value.length === 0) {
  search();
}
</script>

<template>
  <div
    class="mt-8 flex flex-col gap-8 lg:col-span-10 lg:col-start-2 xl:col-span-8 xl:col-start-3">
    <span
      >Отчёты о результатах мероприятий с периодичностью в год. Обновляются
      каждый раз, как появляются новые данные о результатах событий.</span
    >

    <div class="flex flex-col gap-4">
      <UBadge
        class="cursor-pointer hover:scale-[101%]"
        v-for="file in response_state"
        size="lg"
        @click="download_file(file.id)">
        <div class="flex w-full justify-between">
          <div>{{ file.file_name }}</div>
          <div>{{ file.upload_at.split('T')[0] }}</div>
        </div>
      </UBadge>
    </div>
  </div>
</template>
