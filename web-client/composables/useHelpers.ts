export default () => {
  const auth_api = useAuth();
  const config_api = useConfig();

  const REQUEST_URL = (postfix: string) =>
    `${config_api.BACKEND_URL()}${postfix}`;
  const AUTH_HEADERS = () => ({ Authorization: auth_api.token.value || '' });

  return {
    REQUEST_URL,
    AUTH_HEADERS,
  };
};
