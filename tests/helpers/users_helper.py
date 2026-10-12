class UsersHelper:
    def get_users(self, get_method, users_ids: list = []):
        users = get_method()
        for user in users.json()['usuarios']:
            users_ids.append(user['_id'])

        return users_ids

    def cleanup_db(self, users_ids, delete_method):
        for user_id in users_ids:
            delete_method(user_id)
