class ApiResponse(Exception):
    def __init__(self, response, status_code=200):
        self.response = {"data": response, "statusCode": status_code}
        self.status_code = status_code


class WrongJsonFormat(ApiResponse):
    def __init__(self, response="Wrong JSON format", status_code=500):
        super().__init__(response, status_code)


class WrongFactFormat(ApiResponse):
    def __init__(self, response="Wrong fact format", status_code=500):
        super().__init__(response, status_code)


class WrongPrologFormat(ApiResponse):
    def __init__(self, response="Wrong PROLOG format", status_code=500):
        super().__init__(response, status_code)


class WrongConditionFormat(ApiResponse):
    def __init__(self, response="Wrong format of condition", status_code=500):
        super().__init__(response, status_code)


class WrongConditionStatementFormat(ApiResponse):
    def __init__(self, response="Wrong format of condition statement", status_code=500):
        super().__init__(response, status_code)


class ExecutionError(ApiResponse):
    def __init__(self, response="Error while executing code", status_code=500):
        super().__init__(response, status_code)
