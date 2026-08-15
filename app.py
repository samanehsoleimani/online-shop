from flask import Flask

import config
from blueprints.general import app as general
from blueprints.admin import admin
from blueprints.user import app as user
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from sqlalchemy import text

import extentions
from models.user import User
from models.category import Category
app = Flask(__name__)


app.register_blueprint(general)
app.register_blueprint(user)
app.register_blueprint(admin)


app.config["SQLALCHEMY_DATABASE_URI"] = config.SQLALCHEMY_DATABASE_URI
app.config["SECRET_KEY"] = config.SECRET_KEY

extentions.db.init_app(app)


csrf = CSRFProtect(app)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "user.login"


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



with app.app_context():

    # ساخت جدول‌هایی که وجود ندارند
    extentions.db.create_all()


    result = extentions.db.session.execute(
        text("PRAGMA table_info(products)")
    )

    columns = [row[1] for row in result]


    if 'category_id' not in columns:

        extentions.db.session.execute(
            text("""
                ALTER TABLE products
                ADD COLUMN category_id INTEGER
            """)
        )

        extentions.db.session.commit()



    categories = [
        ("ست های جذاب", "set.jpg"),
        ("بیلر ها", "beler.png"),
        ("سارافون ها", "sarafon.png")
    ]


    for name, image in categories:

        existing_category = Category.query.filter_by(
            name=name
        ).first()


        if existing_category is None:

            category = Category(
                name=name,
                image=image
            )

            extentions.db.session.add(category)


    extentions.db.session.commit()



if __name__ == '__main__':
    app.run(debug=True)
