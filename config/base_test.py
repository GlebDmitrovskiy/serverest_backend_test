from services.log_in.api_log_in import LogIn

class BaseTest:
    def setup_method(self):
        self.api_log_in = LogIn()
