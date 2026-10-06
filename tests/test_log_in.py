import allure
from config.base_test import BaseTest
class TestLogIn(BaseTest):
    @allure.story("Проверка авторизации")
    def test_create_log(self):
        response_post_log_in =  self.api_log_in.create_log_in()
        assert response_post_log_in.status_code == 200
