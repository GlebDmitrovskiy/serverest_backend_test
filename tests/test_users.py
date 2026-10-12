from config.base_test import BaseTest
from services.users.schemas import UsersCreateSchema, NegativeUpdateUserEmail
from services.users.schemas import UsersGetSchema
from services.users.schemas import NegativeUserGetById
from services.users.schemas import UserGetByIdBody
from services.users.schemas import DeleteUser
from services.users.schemas import NegativeDeleteUser
from services.users.schemas import UpdateUserEmailNew
from services.users.schemas import UpdateUserEmailOld
from services.users.schemas import NegativeUpdateUserEmail
from services.users.schemas import UsersCreateSchemaStatusCod201
from config.text_generator import text_generator
from config.random_role import random_role_by_admin
from helpers.users_helper import UsersHelper
import allure
import pytest
import faker


class TestUsers(BaseTest):
    fake = faker.Faker()
    user_helper = UsersHelper()

    def cleanup_db(self):
        users_ids = self.user_helper.get_users(self.api_users.get_users)
        self.user_helper.cleanup_db(users_ids, self.api_users.delete_user)

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
            self.api_users.delete_user(id_user=id_user)
        with allure.step("Проверка, что пользователь с негативными параметрами, не создался"):
            assert response_post_user.status_code == 400
            assert response_get.status_code == 400

    @allure.story("Позитивная проверка обновления")
    @pytest.mark.parametrize("field, value",
                             [(None, (text_generator(15), fake.email(), text_generator(20), random_role_by_admin())),
                              ("nome", text_generator(15)),
                              ("email", fake.email()),
                              ("password", text_generator(20)),
                              ("administrador", random_role_by_admin())
                              ])
    def test_positive_put_user(self, create_and_delete_user, field, value):
        with allure.step("Обновление пользователя и проверка что его данные обновились"):
            data_put = create_and_delete_user[1]
        with allure.step("Обновление всего тела сразу и проверка обновления по одному полю пользователя"):
            if field is None:
                new_data = {
                    "nome": value[0],
                    "email": value[1],
                    "password": value[2],
                    "administrador": value[3]
                }
                response_put = self.api_users.update_user(id_user=create_and_delete_user[0], **new_data)
                response_get = self.api_users.get_user_by_id(create_and_delete_user[0]).json()
                data_response_put = response_put.json()
                validate_put = UpdateUserEmailOld(**data_response_put)
                assert response_put.status_code == 200
                assert validate_put
                assert validate_put.message == "Registro alterado com sucesso"
                assert self.api_users.get_user_by_id(create_and_delete_user[0]).status_code == 200
                assert response_get.get("nome") == new_data["nome"]
                assert response_get.get("email") == new_data["email"]
                assert response_get.get("password") == new_data["password"]
                assert response_get.get("administrador") == new_data["administrador"]
            else:
                data_put = create_and_delete_user[1]
                data_put[field] = value
                response_put = self.api_users.update_user(create_and_delete_user[0], **data_put)
                data_response_put = response_put.json()
                validate_put = UpdateUserEmailOld(**data_response_put)
                response_get = self.api_users.get_user_by_id(create_and_delete_user[0]).json()
                assert response_put.status_code == 200
                assert validate_put.message == "Registro alterado com sucesso"
                assert validate_put
                assert response_get["nome"] == data_put["nome"]
                assert response_get["email"] == data_put["email"]
                assert response_get["password"] == data_put["password"]
                assert response_get["administrador"] == data_put["administrador"]

        with allure.step("Обновление email у пользователя и проверка что его email обновилось"):
            data_put["email"] = self.fake.email()
            response_put_email = self.api_users.update_user("huesos228", **data_put)
            data_response_put = response_put_email.json()
            validate_put_email = UpdateUserEmailNew(**data_response_put)
            new_id = response_put_email.json()["_id"]
        with allure.step(
                "Получение ответа от put, проверка ответа о смене почты с неизвестным id, валидация ответа и проверка о удалении нового созданного пользователя"):
            assert response_put_email.status_code == 201
            assert validate_put_email.message == "Cadastro realizado com sucesso"
            assert validate_put_email
            response_get_email = self.api_users.get_user_by_id(id_user=new_id).json()
            assert response_get_email["email"] == data_put["email"]
            assert self.api_users.get_user_by_id(id_user=new_id).status_code == 200
            response_delete_put_email = self.api_users.delete_user(new_id)
            assert response_delete_put_email.status_code == 200
            assert self.api_users.get_user_by_id(new_id).status_code == 400

    @allure.story("Негативная проверка обновления")
    @pytest.mark.parametrize("allure_title, field, value",
                             [("Негативная проверка,  все поля, int", None,
                               (1, 1, 1, 1)),
                              ("Негативная проверка, поле nome, int", "nome", 1),
                              ("Негативная проверка, поле email, int", "email", 1),
                              ("Негативная проверка, поле password, int", "password", 1),
                              ("Негативная проверка, поле admininstrador, int", "administrador", 1),
                              ("Негативная проверка, все поля, float", None,
                               (1.5, 1, 5, 1, 5, 1, 5)),
                              ("Негативная проверка, поле nome, float", "nome", 1.5),
                              ("Негативная проверка, поле email, float", "email", 1.5),
                              ("Негативная проверка, поле password, float", "password", 1.5),
                              ("Негативная проверка, поле admininstrador, float", "administrador", 1.5),
                              ("Негативная проверка, все поля, bool", None,
                               (False, True, False, False)),
                              ("Негативная проверка, поле nome, bool", "nome", True),
                              ("Негативная проверка, поле email, bool", "email", True),
                              ("Негативная проверка, поле password, bool", "password", True),
                              ("Негативная проверка, поле admininstrador, bool", "administrador", True),
                              ("Негативная проверка, все поля, пустые", None,
                               ("", "", "", "")),
                              ("Негативная проверка, поле nome, пустое", "nome", ""),
                              ("Негативная проверка, поле email, пустое", "email", ""),
                              ("Негативная проверка, поле password, пустое", "password", ""),
                              ("Негативная проверка, поле admininstrador, пустое", "administrador", ""),
                              ("Негативная проверка, все поля, None", None,
                               (None, None, None, None)),
                              ("Негативная проверка, поле nome, None", "nome", None),
                              ("Негативная проверка, поле email, None", "email", None),
                              ("Негативная проверка, поле password, None", "password", None),
                              ("Негативная проверка, поле admininstrador, None", "administrador", None)
                              ])
    def test_negative_update_user(self, create_and_delete_user, allure_title, field, value):

        with allure.step("Негативное обновление почты пользователя и проверка что его данные не обновились"):

            with allure.step("Проверка на подачу в обновление существующего email у пользователя и проверка на ошибку"):
                with allure.step("Проверка на подачу в обновление существующего email с PostLogIn"):
                    data_put_email = create_and_delete_user[1]
                    data_put_email["email"] = "fulano@qa.com"
                    response_put_email = self.api_users.update_user(create_and_delete_user[0], **data_put_email)
                    data_response_put = response_put_email.json()
                    validate_put_email = NegativeUpdateUserEmail(**data_response_put)
                    assert response_put_email.status_code == 400
                    assert validate_put_email
                    assert validate_put_email.message == "Este email já está sendo usado"

        with allure.step("Негативное обновление пользователя и проверка что его данные не обновились"):
            data_put = create_and_delete_user[1]

        with allure.step("Обновление всего тела сразу и проверка обновления по одному полю пользователя"):
            if field is None:
                list_error_for_none = [{'nome': 'nome deve ser uma string',
                                        'email': 'email deve ser uma string',
                                        'password': 'password deve ser uma string',
                                        'administrador': "administrador deve ser 'true' ou 'false'"},
                                       {'nome': 'nome não pode ficar em branco',
                                        'email': 'email não pode ficar em branco',
                                        'password': 'password não pode ficar em branco',
                                        'administrador': "administrador deve ser 'true' ou 'false'"}
                                       ]
                new_data = {
                    "nome": value[0],
                    "email": value[1],
                    "password": value[2],
                    "administrador": value[3]
                }
                response_put = self.api_users.update_user(id_user=create_and_delete_user[0], **new_data)
                data_response_put = response_put.json()
                assert response_put.status_code == 400
                assert data_response_put in list_error_for_none


            else:
                list_error = [{'nome': 'nome deve ser uma string'}, {'email': 'email deve ser uma string'},
                              {'password': 'password deve ser uma string'},
                              {'administrador': "administrador deve ser 'true' ou 'false'"},
                              {'nome': 'nome não pode ficar em branco'}, {'nome': 'nome não pode ficar em branco'},
                              {'email': 'email não pode ficar em branco'},
                              {'password': 'password não pode ficar em branco'},
                              {'administrador': "administrador não pode ficar em branco"},
                              ]
                data_put[field] = value
                data_put = create_and_delete_user[1]
                data_put[field] = value
                response_put = self.api_users.update_user(create_and_delete_user[0], **data_put)
                data_response_put = response_put.json()
                assert data_response_put in list_error
                assert response_put.status_code == 400

    def test_get_users(self, create_and_delete_user):
        self.cleanup_db()
        my_data = create_and_delete_user[1]
        response_get_users = self.api_users.get_users()
        validation_get_users = UsersGetSchema(**response_get_users.json())
        print(response_get_users.json())
        user_get = response_get_users.json()["usuarios"][-1]
        assert my_data["nome"] == user_get["nome"]
        assert my_data["email"] == user_get["email"]
        assert response_get_users.status_code == 200
        assert validation_get_users

    #def test_get_user_by_id(self, create_and_delete_user):
