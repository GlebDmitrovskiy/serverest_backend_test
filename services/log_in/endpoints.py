from resources.base_url import base_url

URL = base_url()


class Endpoints:
    @staticmethod
    def post_login():
        url = URL + "/login"
        return url
