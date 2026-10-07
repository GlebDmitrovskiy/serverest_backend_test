from services.users.endpoints import Endpoints
from services.users.payload_users import PayloadUsers
import requests

class Users:
    def __init__(self):
        self.endpoints = Endpoints()
        self.payload = PayloadUsers()

    def create_user(self, nome: str, email: str, password: str, administrador: str):
        response = requests.post(url = self.endpoints.create_user(), json= self.payload.create_user(nome, email, password, administrador ))
        return response

    def get_user_by_id(self, id_user: str):
        response = requests.get(url = self.endpoints.get_user_by_id(id_user = id_user))
        return response

    def get_users(self):
        response = requests.get(url = self.endpoints.get_users())

    def delete_user(self, id_user: str):
        response = requests.delete(url = self.endpoints.delete_user(id_user = id_user))
        return response

    def update_user(self, id_user, nome: str, email: str, password: str, administrador: str):
        response = requests.put(url = self.endpoints.update_users(id_user= id_user), json = self.payload.update_user(nome, email, password, administrador ))
        return response
