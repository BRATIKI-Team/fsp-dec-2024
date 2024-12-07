<script setup lang="ts">
import type { FormError } from '#ui/types';
import type { SignInRequest } from '~/types/dtos/sign_in';
import useConfig from '~/composables/useConfig';

definePageMeta({ layout: 'auth' });

const auth_api = useAuth();
const config_api = useConfig();

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
}): state is SignInRequest => {
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

const onSubmit = async (data: {
  readonly email: string | null;
  readonly password: string | null;
}) => {
  if (!validate(data)) return;

  error.value = false;
  loading.value = true;
  try {
    await auth_api.signIn(data, { callbackUrl: '/lk' });
  } catch (_) {
    error.value = true;
    loading.value = false;
  }
};
</script>

<template>
  <UAuthForm
    :submit-button="{ label: 'Продолжить' }"
    :fields="fields"
    :validate="errors"
    :loading="loading"
    title="С возвращением!"
    align="top"
    icon="i-heroicons-lock-closed"
    :ui="{ base: 'text-center', footer: 'text-center' }"
    @submit="onSubmit">
    <template #description>
      Ещё нет аккаунта?
      <NuxtLink class="text-primary font-medium" to="/auth/sign_up"
        >Зарегистрироваться
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
      Входя в систему, Вы соглашаетесь с
      <NuxtLink
        class="text-primary font-medium"
        :to="config_api.PRIVACY_POLICY_URL()">
        Политикой конфиденциальности
      </NuxtLink>
      .
    </template>
  </UAuthForm>
</template>
