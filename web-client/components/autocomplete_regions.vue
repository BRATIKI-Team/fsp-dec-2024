<script setup lang="ts">
import type { IRegion } from '~/types/dtos/region';
import useApi from '~/composables/useApi';

const api = useApi();

const model = defineModel<string | undefined>();
const options = ref<readonly IRegion[]>([]);

api.regions.all().then(response => (options.value = response));
</script>

<template>
  <UInputMenu
    v-model="model"
    placeholder="Выберите регион"
    size="xl"
    :options="[...options]"
    value-attribute="id"
    option-attribute="name" />
</template>
