# =========================================================================
# Flask
# =========================================================================

DEBUG = True
# python3 -c "import os;print(os.urandom(32))"
SECRET_KEY = '\xf0\xb6\x19\xb94Uo\x1b\xf9\x8b\x0e\xa1@RK\x11T_\xb9Q\xde\x1d\x80\xfa\xd4t\xcbZN:1@'

# =========================================================================
# SQLAlchemy
# =========================================================================

SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/bambank.sqlite'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# =========================================================================
# WTForms
# =========================================================================

WTF_CSRF_ENABLED = True