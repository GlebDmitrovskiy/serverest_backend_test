from services.log_in.schemas import LogInSchema
from services.log_in.schemas import NegativeLogIn

import allure
import pytest
from config.base_test import BaseTest
class TestLogIn(BaseTest):
    @allure.story("Позитивная проверка авторизации")
    def test_positive_create_log(self):
        response_post_log_in =  self.api_log_in.create_log_in()
        with allure.step("Валидация ответа и проверка сообщений"):
            data = response_post_log_in.json()
            login_response = LogInSchema(**data)
        assert login_response.message == 'Login realizado com sucesso'
        assert login_response.authorization.startswith('Bearer')
        assert response_post_log_in.status_code == 200

    @allure.story("Негативная проверка авторизации")
    @pytest.mark.parametrize("allure_title, email, password",
                             [("Проверка авторизации message рандом", "fulano@qa.com", "zalupa"),
                              ("Проверка авторизации поле авторизация рандом", "wrong@test.com", "teste")
                                      ])
    def test_negative_create_log(self, allure_title, email, password):
        allure.dynamic.title(allure_title)
        with allure.step("Валидация ответа при ошибке, проверка сообщений об ошибке"):
            response_post_log_in = self.api_log_in.create_log_in(email = email, password = password)
            data = response_post_log_in.json()
            login_response = NegativeLogIn(**data)
        assert login_response.message == "Email e/ou senha inválidos"
        assert response_post_log_in.status_code == 401



