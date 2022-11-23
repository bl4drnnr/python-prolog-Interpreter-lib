class ApiResponse(Exception):
    def __init__(self, response, status_code=200):
        self.response = {"data": response, "statusCode": status_code}
        self.status_code = status_code


class SingleArgument(ApiResponse):
    pass


class WrongOption(ApiResponse):
    pass


class WrongJsonFormat(ApiResponse):
    pass


class WrongFactFormat(ApiResponse):
    pass


class WrongPrologFormat(ApiResponse):
    pass
