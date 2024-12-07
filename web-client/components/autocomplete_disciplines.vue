<script setup lang="ts">
import useApi from '~/composables/useApi';

const api = useApi();

const model = defineModel<string | undefined>();
const options = ref<readonly string[]>([]);

api.disciplines.all().then(response => (options.value = response));
</script>

<template>
  <UInputMenu
    v-model="model"
    placeholder="Выберите дисциплину"
    :options="[...options]" />
</template>
