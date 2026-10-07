class PayloadUsers:
    @staticmethod
    def create_user(nome: str, email: str, password: str, administrador: str):
        data = {
            "nome": nome,
            "email": email,
            "password": password,
            "administrador": administrador
        }
        return data

    @staticmethod
    def update_user(nome: str, email: str, password: str, administrador: str):
        data = {
            "nome": nome,
            "email": email,
            "password": password,
            "administrador": administrador
        }
        return data



