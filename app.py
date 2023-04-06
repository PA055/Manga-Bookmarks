from app import api_app
from app import app, db
from app.models import *
from app.helper import *
import uvicorn


if __name__ == '__main__':
    uvicorn.run(api_app, host='0.0.0.0', port=8080)
