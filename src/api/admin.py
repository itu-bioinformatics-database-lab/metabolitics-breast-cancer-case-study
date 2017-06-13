from flask_admin.contrib.sqla import ModelView
from flask_admin import Admin

from .app import app
from .models import Analysis, User, db

admin = Admin(app, name='microblog', template_mode='bootstrap3')

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Analysis, db.session))
