from fastapi.responses import JSONResponse

class CurlException(Exception):
    def __init__(self, content):
        self.content = content

def handle(content):
    return JSONResponse(
        status_code=403,
        content=content,
    )
