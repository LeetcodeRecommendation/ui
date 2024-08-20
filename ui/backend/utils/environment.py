import os


class Environment:
    @staticmethod
    def get_redis_ip() -> str:
        return os.environ["REDIS_IP"]

    @staticmethod
    def get_redis_port() -> int:
        return int(os.environ["REDIS_PORT"])

    @staticmethod
    def get_user_request_uri() -> str:
        return os.environ["USER_REQUEST_URI"]

    @staticmethod
    def get_cassandra_uri() -> list[str]:
        return os.environ["CASSANDRA_URL"].split(";")
