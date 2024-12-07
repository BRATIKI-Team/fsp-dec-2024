export default () => {
  const config = useRuntimeConfig().public;

  const PRIVACY_POLICY_URL = () => config.privacyPolicyUrl;
  const BACKEND_URL = () => config.backendUrl;
  const FAQ_URL = () => config.faqUrl;

  return {
    PRIVACY_POLICY_URL,
    BACKEND_URL,
    FAQ_URL,
  };
};
