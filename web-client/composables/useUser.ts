import type { IUser } from '~/types/dtos/user';
import { UserRole } from '~/types/dtos/user';

export default async () => {
  const {getSession} = useAuth()
  const user = await getSession() as IUser|null
  const isAdmin = user?.role == UserRole.SUPER_ADMIN

  return {user, isAdmin}
}