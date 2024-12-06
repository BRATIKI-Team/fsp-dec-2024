export default () => {
  const config = useRuntimeConfig().public;

  const PRIVACY_POLICY_URL = () => config.privacyPolicyUrl;

  return {
    PRIVACY_POLICY_URL
  }
}