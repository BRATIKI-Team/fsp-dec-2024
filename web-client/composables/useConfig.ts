export default () => {
  const config = useRuntimeConfig().public;

  const PRIVACY_POLICY_URL = () => config.privacyPolicyUrl;
  const BACKEND_URL = () => config.backendUrl;

  return {
    PRIVACY_POLICY_URL,
    BACKEND_URL,
  };
};
