from services.log_in.api_log_in import LogIn
from services.users.api_users import Users
class BaseTest:
    def setup_method(self):
        self.api_log_in = LogIn()
        self.api_users = Users()