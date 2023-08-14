import uvicorn
from decouple import config
if __name__ == '__main__':
    uvicorn.run(
        'v1.api:app',
        host='0.0.0.0',
        port=config('API_PORT', cast=int),
        reload=True
    )