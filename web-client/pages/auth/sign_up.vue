<script setup lang="ts">
import type { FormError } from '#ui/types';
import type { SignUpRequest } from '~/types/dtos/sign_up';

definePageMeta({
  layout: 'auth'
})

const { auth } = api();
const loading = ref(false);
const error = ref(false);

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

const onSubmit = (data: {
  readonly email: string | null;
  readonly password: string | null;
}) => {
  if (!validate(data)) return;

  error.value = false;
  loading.value = true;
  auth
    .sign_up(data)
    .catch(() => (error.value = true))
    .then(() => { navigateTo('/auth/sign_in') })
    .finally(() => (loading.value = false));
};
</script>

<template>
  <UAuthForm
    :submit-button="{ label: 'Продолжить' }"
    :fields="fields"
    :validate="errors"
    :loading="loading"
    title="Добро пожаловать!"
    align="top"
    icon="i-heroicons-lock-open"
    :ui="{ base: 'text-center', footer: 'text-center' }"
    @submit="onSubmit">
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
        to="https://www.youtube.com/watch?v=dQw4w9WgXcQ">
        Политикой конфиденциальности</NuxtLink
      >.
    </template>
  </UAuthForm>
</template>
