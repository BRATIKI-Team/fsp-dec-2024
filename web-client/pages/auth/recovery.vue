<script setup lang="ts">
import type { FormError } from '#ui/types';
import type { ForgetPasswordRequest } from '~/types/dtos/reset';

definePageMeta({ layout: 'auth' });

const api = useApi();

const loading = ref(false);
const error = ref(false);

const fields = [
  {
    name: 'email',
    type: 'email',
    label: 'Email',
    placeholder: 'Введите Ваш email',
  },
];

const validate = (state: {
  readonly email: string | null;
}): state is ForgetPasswordRequest => {
  return state.email !== null;
};

const errors = (state: { readonly email: string | null }): FormError[] => {
  if (!state.email) {
    return [{ path: 'email', message: 'Email обязателен!' }];
  }
  return [];
};

const onSubmit = async (data: { readonly email: string | null }) => {
  if (!validate(data)) return;

  error.value = false;
  loading.value = true;
  api.auth.forget(data).then(
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
    title="Введите Email для восстановления пароля."
    align="top"
    icon="i-heroicons-envelope"
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
        title="Что-то пошло не так. Невалидный Email." />
    </template>

    <template #footer>
      После подтверждения Вам придёт письмо с ссылкой для восстановления пароля.
    </template>
  </UAuthForm>
</template>
