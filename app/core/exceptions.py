from fastapi import HTTPException, status


class NotFound(HTTPException):
    def __init__(self, detail: str = "المورد غير موجود"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=detail)


class Unauthorized(HTTPException):
    def __init__(self, detail: str = "غير مصرح"):
        super().__init__(status_code=status.HTTP_401_UNAUTHORIZED, detail=detail)


class Forbidden(HTTPException):
    def __init__(self, detail: str = "ليس لديك صلاحية"):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


class Conflict(HTTPException):
    def __init__(self, detail: str = "بيانات مكررة"):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class BadRequest(HTTPException):
    def __init__(self, detail: str = "طلب غير صالح"):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)
