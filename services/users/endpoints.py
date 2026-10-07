from resources.base_url import base_url
URL = base_url()
class Endpoints:
    @staticmethod
    def create_user():
        url = URL + "/usuarios"
        return url

    @staticmethod
    def get_users():
        url = URL + "/usuarios"
        return url

    @staticmethod
    def delete_user(id_user: str):
        url = URL + f"/usuarios/{id_user}"
        return url

    @staticmethod
    def get_user_by_id(id_user: str):
        url = URL + f"/usuarios/{id_user}"
        return url

    @staticmethod
    def update_users(id_user: str):
        url = URL + f"/usuarios/{id_user}"
        return url