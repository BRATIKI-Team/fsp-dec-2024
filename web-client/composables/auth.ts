import type { SignInRequest } from '~/types/dtos/sign_in';
import type { SignUpRequest } from '~/types/dtos/sign_up';

export default () => {
  const auth = useAuth();

  const sign_in = async (request: SignInRequest) => auth.signIn(request);

  const sign_up = async (request: SignUpRequest) => auth.signUp(request);

  const session = async () => auth.getSession();

  return {
    sign_in,
    sign_up,
    session,
  };
};
