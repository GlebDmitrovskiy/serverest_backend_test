from config.base_test import BaseTest
from services.users.schemas import UsersCreateSchema
from services.users.schemas import NegativeCreateSchema
from services.users.schemas import UsersGetSchema
from services.users.schemas import NegativeUserGetById
from services.users.schemas import UserGetByIdBody
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
import faker


class TestUsers(BaseTest):
    fake = faker.Faker()

    @pytest.fixture
    def create_and_delete_user(self):
        my_email = self.fake.email()
        data = {
            "nome": text_generator(10),
            "email": my_email,
            "password": text_generator(15),
            "administrador": random_role_by_admin()
        }

        response_post_user = self.api_users.create_user(**data)
        id_user = response_post_user.json().get("_id")
        yield id_user, data
        try:
            assert response_post_user.status_code == 201
        finally:
            self.api_users.delete_user(id_user=id_user)

    @allure.feature("Добавление пользователя")
    @allure.story("Позитивная проверка создания пользователя")
    def test_positive_create_user(self):
        with allure.step("Создание пользователя"):
            fake = faker.Faker()
            my_email = fake.email()
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
            response_get_user_for_post = self.api_users.get_user_by_id(id_user=id_user)
        with allure.step("Валидация тела и проверка сообщений"):
            assert UsersCreateSchema(**data)
            validation_data_201 = UsersCreateSchemaStatusCod201(**data_post)
        with allure.step("Проверка сообщения о создании пользователя и проверка id в ответе"):
            assert response_post_user.status_code == 201
            assert response_get_user_for_post.status_code == 200
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

    @allure.story("Негативная проверка создания")
    @pytest.mark.parametrize("allure_title, nome, email, password, administrador",
                             [("Проверка негативного создания nome int", 1, fake.email(),
                               text_generator(20), random_role_by_admin()),
                              ("Проверка негативного создания nome float", 1.5, fake.email(),
                               text_generator(15), random_role_by_admin()),
                              ("Проверка негативного создания nome bool", False, fake.email(),
                               text_generator(20), random_role_by_admin()),
                              ("Проверка негативного создания nome пустое", "", fake.email(),
                               text_generator(20), random_role_by_admin()),
                              ("Проверка негативного создания nome None", None, fake.email(),
                               text_generator(20), random_role_by_admin()),
                              ("Проверка негативного создания email int", text_generator(10), 5, text_generator(20),
                               random_role_by_admin()),
                              ("Проверка негативного создания email float", text_generator(15), 2.28,
                               text_generator(15), random_role_by_admin()),
                              ("Проверка негативного создания email bool", text_generator(10), True, text_generator(20),
                               random_role_by_admin()),
                              ("Проверка негативного создания email пустое", text_generator(12), "", text_generator(20),
                               random_role_by_admin()),
                              ("Проверка негативного создания email None", text_generator(15), None, text_generator(20),
                               random_role_by_admin()),
                              ("Проверка негативного создания password int", text_generator(15), fake.email(), 1,
                               random_role_by_admin()),
                              ("Проверка негативного создания password float", text_generator(20), fake.email(), 1.5,
                               random_role_by_admin()),
                              ("Проверка негативного создания password bool", text_generator(20), fake.email(), False,
                               random_role_by_admin()),
                              ("Проверка негативного создания password пустое", text_generator(20), fake.email(), "",
                               random_role_by_admin()),
                              ("Проверка негативного создания password None", text_generator(15), fake.email(), None,
                               random_role_by_admin()),
                              ("Проверка негативного создания  administrador int", text_generator(15), fake.email(),
                               text_generator(15), 1),
                              ("Проверка негативного создания  administrador float", text_generator(20), fake.email(),
                               text_generator(20), 2.28),
                              ("Проверка негативного создания  administrador bool", text_generator(15), fake.email(),
                               text_generator(25), True),
                              ("Проверка негативного создания  administrador пустое", text_generator(10), fake.email(),
                               text_generator(13), ""),
                              ("Проверка негативного создания  administrador None", text_generator(19), fake.email(),
                               text_generator(23), None)
                              ])
    def test_negative_create_user(self, allure_title, nome: str, email: str, password: str, administrador: str):
        data = {
            "nome": nome,
            "email": email,
            "password": password,
            "administrador": administrador
        }
        response_post_user = self.api_users.create_user(**data)
        id_user = response_post_user.json().get("_id")
        response_get = self.api_users.get_user_by_id(id_user=id_user)
        try:
            assert response_post_user.status_code == 400
        finally:
            print(response_post_user.json())
            self.api_users.delete_user(id_user=id_user)
        with allure.step("Проверка, что пользователь с негативными параметрами, не создался"):
            assert response_post_user.status_code == 400
            assert response_get.status_code == 400

    @allure.story("Позитивная проверка обновления")
    @pytest.mark.parametrize("allure_title, nome, email, password, administrador",
                             [("Обновление поля nome", text_generator(15), fake.email(), text_generator(20),
                               random_role_by_admin())
                              ])
    def test_positive_put_user(self, create_and_delete_user, allure_title, nome, email, password, administrador):
        with allure.step("Обновление пользователя и проверка что его данные обновилось"):
            data_put = create_and_delete_user[1]
            new_data = {
                "nome": nome,
                "email": email,
                "password": password,
                "administrador": administrador
            }
            response_put = self.api_users.update_user(id_user=create_and_delete_user[0], **new_data)
            data_response_put = response_put.json()
            validate_put = UpdateUserEmailOld(**data_response_put)
            assert response_put.status_code == 200
            assert validate_put
            assert validate_put.message == "Registro alterado com sucesso"
            assert self.api_users.get_user_by_id(create_and_delete_user[0]).status_code == 200
            response_get = self.api_users.get_user_by_id(create_and_delete_user[0]).json()
            assert response_get.get("nome") == new_data["nome"]
            assert response_get.get("email") == new_data["email"]
            assert response_get.get("password") == new_data["password"]
            assert response_get.get("administrador") == new_data["administrador"]

        with allure.step("Обновление email у пользователя и проверка что его email обновилось"):
            data_put["email"] = self.fake.email()
            response_put_email = self.api_users.update_user("huesos228", **data_put)
            data_response_put_email = response_put_email.json()
            validate_put_email = UpdateUserEmailNew(**data_response_put_email)
            new_id = response_put_email.json()["_id"]
            assert response_put_email.status_code == 201
            assert validate_put_email.message == "Cadastro realizado com sucesso"
            assert validate_put_email
            response_get_email = self.api_users.get_user_by_id(id_user=new_id).json()
            assert response_get_email["email"] == data_put["email"]
            assert self.api_users.get_user_by_id(id_user=new_id).status_code == 200
            response_delete_put_email = self.api_users.delete_user(new_id)
            assert response_delete_put_email.status_code == 200
            assert self.api_users.get_user_by_id(new_id).status_code == 400

        #доделать отдельно емайл пароль и администратора в пут
