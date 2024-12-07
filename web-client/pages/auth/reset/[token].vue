<script setup lang="ts">
import type { FormError } from '#ui/types';
import type { ResetPasswordRequest } from '~/types/dtos/reset';

definePageMeta({ layout: 'auth' });

const api = useApi();
const route = useRoute();

const loading = ref(false);
const error = ref(false);

const token = route.params.token.toString();

const fields = [
  {
    name: 'password',
    type: 'password',
    label: 'Пароль',
    placeholder: 'Введите новый пароль',
  },
];

const validate = (state: {
  readonly password: string | null;
  readonly token: string;
}): state is ResetPasswordRequest => {
  return state.password !== null;
};

const errors = (state: { readonly password: string | null }): FormError[] => {
  if (!state.password) {
    return [{ path: 'password', message: 'Пароль обязателен!' }];
  }
  return [];
};

const onSubmit = async (data: { readonly password: string | null }) => {
  const request = {
    ...data,
    token: token,
  };

  if (!validate(request)) return;

  error.value = false;
  loading.value = true;
  api.auth.reset(request).then(
    () => {
      loading.value = false;
      error.value = false;

      navigateTo('/auth/sign_in');
    },
    () => {
      error.value = true;
      loading.value = false;
    }
  );
};
</script>

<template>
  <UAuthForm
    :submit-button="{ label: 'Продолжить' }"
    :fields="fields"
    :validate="errors"
    :loading="loading"
    title="Восстановление пароля."
    align="top"
    icon="i-heroicons-shield-exclamation"
    :ui="{ base: 'text-center', footer: 'text-center' }"
    @submit="onSubmit">
    <template #description>
      Вспомнили пароль?
      <NuxtLink class="text-primary font-medium" to="/auth/sign_in"
        >Войти
      </NuxtLink>
    </template>

    <template #validation>
      <UAlert
        v-if="error"
        color="red"
        icon="i-heroicons-information-circle-20-solid"
        title="Что-то пошло не так. Невалидный токен." />
    </template>
  </UAuthForm>
</template>
