# store variables to prevent circular imports
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_cors import CORS

db = SQLAlchemy()
bcrypt = Bcrypt()
cors = CORS()
limiter = Limiter(key_func=get_remote_address)