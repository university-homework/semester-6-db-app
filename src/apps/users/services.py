from apps.users.infrastructure.repositories import UserRepository


class UserService:
    @staticmethod
    async def get_user_by_id(user_id: int):
        conditions = {
            'id': user_id,
        }
        return await UserRepository().get(conditions, is_single=True)

    @staticmethod
    async def get_all_users():
        return await UserRepository().get_all_users()
