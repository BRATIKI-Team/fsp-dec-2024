<script setup lang="ts">
import type { FormError } from '#ui/types';
import type { SignUpRequest } from '~/types/dtos/sign_up';
import useConfig from '~/composables/useConfig';

definePageMeta({ layout: 'auth' });

const api = useApi();
const config_api = useConfig();

const loading = ref(false);
const error = ref(false);
const isModalOpen = ref(false);

const state = ref<{ readonly email: string; readonly password: string } | null>(
  null
);

const res = await api.regions.all();

const options = res.map(i => ({
  id: i.id,
  label: i.subject,
}));

const region = ref(options[0]);

const fields = [
  {
    name: 'email',
    type: 'text',
    label: 'Email',
    placeholder: 'Введите Ваш email',
  },
  {
    name: 'password',
    type: 'password',
    label: 'Пароль',
    placeholder: 'Введите Ваш пароль',
  },
];

const validate = (state: {
  readonly email: string | null;
  readonly password: string | null;
}): state is SignUpRequest => {
  return state.email !== null && state.password !== null;
};

const errors = (state: {
  readonly email: string | null;
  readonly password: string | null;
}): FormError[] => {
  if (!state.email) {
    return [{ path: 'email', message: 'Email обязателен!' }];
  }
  if (!state.password) {
    return [{ path: 'password', message: 'Пароль обязателен!' }];
  }
  return [];
};

const onFormSubmit = (data: {
  readonly email: string | null;
  readonly password: string | null;
}) => {
  if (!validate(data)) return;

  state.value = data;
  isModalOpen.value = true;
};

const onModalSubmit = () => {
  if (state.value === null) return;

  loading.value = false;
  error.value = false;

  api.auth
    .register({
      ...state.value,
      region_id: region.value.id,
    })
    .then(
      () => {
        loading.value = false;
        error.value = false;

        navigateTo('/auth/sign_in');
      },
      () => {
        loading.value = false;
        error.value = true;
      }
    );
};
</script>

<template>
  <UModal v-model="isModalOpen">
    <UCard>
      <div class="flex flex-col gap-4">
        <span>Ещё всего один шаг! Укажите Ваш регион.</span>

        <USelectMenu
          class="w-full"
          v-model="region"
          searchable
          searchable-placeholder="Выберите регион..."
          placeholder="Выберите регион"
          :options="options" />

        <UButton block @click="onModalSubmit" label="Подтвердить" />
      </div>
    </UCard>
  </UModal>

  <UAuthForm
    :submit-button="{ label: 'Продолжить' }"
    :fields="fields"
    :validate="errors"
    :loading="loading"
    title="Добро пожаловать!"
    align="top"
    icon="i-heroicons-lock-open"
    :ui="{ base: 'text-center', footer: 'text-center' }"
    @submit="onFormSubmit">
    <template #description>
      Уже есть аккаунт?
      <NuxtLink class="text-primary font-medium" to="/auth/sign_in"
        >Войти
      </NuxtLink>
    </template>

    <template #validation>
      <UAlert
        v-if="error"
        color="red"
        icon="i-heroicons-information-circle-20-solid"
        title="Что-то пошло не так. Проверьте данные." />
    </template>

    <template #footer>
      Регистрируясь в системе, Вы соглашаетесь с
      <NuxtLink
        class="text-primary font-medium"
        :to="config_api.PRIVACY_POLICY_URL()">
        Политикой конфиденциальности
      </NuxtLink>
      .
    </template>
  </UAuthForm>
</template>
