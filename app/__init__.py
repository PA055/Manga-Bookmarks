import quart.flask_patch

import asyncio
from quart import Quart
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Quart(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

if __name__ == '__main__':
    asyncio.run(app.run_task(port=5050))
