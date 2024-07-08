from rest_framework.response import Response


class JsendSuccessResponse:
    def __init__(self, status, data, message: str = ""):
        print(type(data))
        self.response = {"status": status, "data": data, "message" : message}

    def get_response(self):
        return Response(self.response)   