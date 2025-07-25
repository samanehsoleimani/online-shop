from flask import Flask

import config
from blueprints.general import app as general
from blueprints.admin import admin
from blueprints.user import app as user
import config
import extentions

# اپلیکیشن اصلی و ثبت بلوپرینت‌ها
app = Flask(__name__)
app.register_blueprint(general)
app.register_blueprint(user)
app.register_blueprint(admin)

# تنظیمات دیتابیس و راه‌اندازی
app.config["SQLALCHEMY_DATABASE_URI"] =config.SQLALCHEMY_DATABASE_URI
app.config['SECRET_KEY']=config.SECRET_KEY
extentions.db.init_app(app)

with app.app_context():
    extentions.db.create_all()

if __name__ == '__main__':
    app.run()