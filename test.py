from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_potion import Api, ModelResource, fields
from flask_potion.routes import ItemRoute

app = Flask(__name__)
db = SQLAlchemy(app)
api = Api(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)

db.create_all()

class UserResource(ModelResource):
    class Meta:
        model = User

    @ItemRoute.GET
    def greeting(self, user) -> fields.String():
        return "Hello, {}!".format(user.name)

api.add_resource(UserResource)

if __name__ == '__main__':
    app.run()