from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + \
    os.path.join(basedir, 'app.sqlite')

db = SQLAlchemy(app)
ma = Marshmallow(app)

# test to show commit vscode ui

CORS(app)


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    url = db.Column(db.String, nullable=False)

    def __init__(self, name, price, url):
        self.name = name
        self.price = price
        self.url = url


class ItemSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "price", "url")


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)

@app.route("/item/add", methods=["POST"])
def add_item():
    name = request.json.get("name")
    price = request.json.get("price")
    url = request.json.get("url")

    record = Item(name, price, url)
    db.session.add(record)
    db.session.commit()

    return jsonify(item_schema.dump(record))


@app.route("/item/get", methods=["GET"])
def get_all_items():
    all_items = Item.query.all()
    return jsonify(items_schema.dump(all_items))


if __name__ == "__main__":
    app.run(debug=True)
