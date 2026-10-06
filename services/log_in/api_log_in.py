from services.log_in.endpoints import Endpoints
from services.log_in.payload_log_in import PayLoadLogIn
import requests
class LogIn:
    def __init__(self):
        self.endpoints_log_in = Endpoints()
        self.payload_log_in = PayLoadLogIn()

    def create_log_in(self):
        """
        Функция для авторизации
        :return: response
        """
        response = requests.post(url = self.endpoints_log_in.post_login(), json = self.payload_log_in.creat_log())
        return response