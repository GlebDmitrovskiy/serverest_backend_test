class PayLoadLogIn:
    @staticmethod
    def creat_log(email = None, password = None):
        """
        Создает пользователя с почтой и паролем
        :return: data
        """
        data = {
            "email": email or "fulano@qa.com",
            "password": password or "teste"
        }
        return data