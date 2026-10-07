from config.base_test import BaseTest
from services.users.schemas import UsersCreateSchema
from services.users.schemas import NegativeCreateSchema
from services.users.schemas import UsersGetSchema
from services.users.schemas import NegativeUserGetById
from services.users.schemas import UserGetById
from services.users.schemas import DeleteUser
from services.users.schemas import NegativeDeleteUser
from services.users.schemas import UpdateUserEmailNew
from services.users.schemas import UpdateUserEmailOld
from services.users.schemas import NegativeUpdateUser
from services.users.schemas import UsersCreateSchemaStatusCod201
from services.users.schemas import UsersCreateSchemaStatusCod400
from config.text_generator import text_generator
from config.random_role import random_role_by_admin
import allure
import pytest


class TestUsers(BaseTest):
        # @pytest.fixture
        # def create_and_delete_user(self):
        #    my_email = "zalupa.bigcock@gmail.com"
        #    data = {
        #        "nome": text_generator(10),
        #        "email": my_email,
        #        "password": text_generator(15),
        #        "administrador": random_role_by_admin()
        #    }
    #
    #    self.api_users.create_user(**data)
    #
    #    #self.api_users.get_user_by_id(id_user=)
    #    #yield


    @allure.feature("Добавление пользователя")
    @allure.story("Позитивная проверка создания пользователя")
    def test_positive_create_user(self):
        with allure.step("Создание пользователя"):
            my_email = "zalupa.bigcocker@gmail.com"
            data = {
                "nome": text_generator(10),
                "email": my_email,
                "password": text_generator(15),
                "administrador": random_role_by_admin()
            }
            response_post_user = self.api_users.create_user(**data)
        with allure.step("Получение id и data"):
            id_user = response_post_user.json().get("_id")
            data_post = response_post_user.json()
        with allure.step("Валидация тела и проверка сообщений"):
            UsersCreateSchema(**data)
            validation_data_201 = UsersCreateSchemaStatusCod201(**data_post)
        with allure.step("Проверка сообщения о создании пользователя и проверка id в ответе"):
            assert validation_data_201.message == "Cadastro realizado com sucesso"
            assert validation_data_201.id == id_user
        with allure.step("Гарантированное удаление пользователя, при не успешном создании пользователя"):
            try:
                assert response_post_user.status_code == 201
            finally:
                response_delete_user = self.api_users.delete_user(id_user=id_user)
        with allure.step("Проверка что пользователь удален и валидация ответа"):
            response_get_user = self.api_users.get_user_by_id(id_user=id_user)
            assert response_delete_user.status_code == 200
            data_delete_response = response_delete_user.json()
            validation_delete_response = DeleteUser(**data_delete_response)
        with allure.step("Проверка сообщения об удалении"):
            assert validation_delete_response.message == "Registro excluído com sucesso"
        with allure.step("Проверка об отсутсвии пользователя, который удален и валидация ответа"):
            assert response_get_user.status_code == 400
            data_get = response_get_user.json()
            validation_get_response = NegativeUserGetById(**data_get)
        with allure.step("Проверка сообщения ошибки, при получении удаленного пользователя"):
            assert validation_get_response.message == "Usuário não encontrado"

