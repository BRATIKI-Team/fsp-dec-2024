// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2024-11-01',
  devtools: { enabled: true },
  modules: [
    '@sidebase/nuxt-auth',
    '@nuxt/ui',
    '@nuxt/image',
    '@vee-validate/nuxt',
  ],
  extends: ['@nuxt/ui-pro'],
  runtimeConfig: {
    public: {
      backendUrl: process.env.NUXT_BACKEND_URL,
      privacyPolicyUrl: process.env.PRIVACY_POLICY_URL,
      faqUrl: process.env.FAQ_URL,
    },
  },
  image: {
    provider: 'none',
  },
  app: {
    head: {
      title: 'Управление ЕКП ФСП - BRATIKI',
    },
  },
  auth: {
    isEnabled: true,
    baseURL: `${process.env.NUXT_BACKEND_URL}/users/`,
    provider: {
      type: 'local',
      endpoints: {
        signIn: { path: 'login', method: 'post' },
        signUp: { path: 'register', method: 'post' },
        getSession: { path: 'me', method: 'get' },
      },
      token: {
        signInResponseTokenPointer: '/token',
        type: 'Bearer',
        headerName: 'Authorization',
        maxAgeInSeconds: 1800,
        sameSiteAttribute: 'strict',
      },
      refresh: {
        isEnabled: true,
        endpoint: { path: 'refresh-token', method: 'post' },
        refreshOnlyToken: false,
        token: {
          signInResponseRefreshTokenPointer: '/refresh_token',
          refreshRequestTokenPointer: '/refresh_token',
        },
      },
      session: {
        dataType: {
          id: 'string',
          email: 'string',
          role: 'string',
          region: {
            id: 'string',
          },
        },
      },
    },
  },
  tailwindcss: {
    config: {
      theme: {
        extend: {
          colors: {
            elevated: '#F1F5F9',
            dimmed: '#94A3B8',
            accented: '#CBD5E1',
          },
        },
      },
    },
  },
});
