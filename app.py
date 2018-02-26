#!flask/bin/python
from flask import Flask, jsonify, abort, make_response, request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

import os

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root@localhost/February"
db = SQLAlchemy(app)
ma = Marshmallow(app)

# class Config(object):
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'sqlite:///' + os.path.join(basedir, 'app.db')
#     SQLALCHEMY_TRACK_MODIFICATIONS = False

class Quote(db.Model):
    __tablename__ = 'quote'
    author = db.Column(db.String(20), nullable=True, primary_key=True)
    text = db.Column(db.String(250), nullable=True, primary_key=True)

    def __init__(self, author, text):
        self.author = author
        self.text = text

class QuoteSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('author', 'text')

quote_schema = QuoteSchema()
quotes_schema = QuoteSchema(many=True)

@app.route('/api/quotes', methods=['GET'])
def get_quotes():
    all_quotes = Quote.query.all()
    result = quotes_schema.dump(all_quotes)
    return jsonify(result.data)

# endpoint to create new quote
@app.route("/api/quote", methods=["POST"])
def add_quote():
    author = request.json['author']
    text = request.json['text']
    
    new_quote = Quote(author, text)

    db.session.add(new_quote)
    db.session.commit()

    return quote_schema.jsonify(new_quote)

# endpoint to delete quote
@app.route("/api/quote", methods=["DELETE"])
def user_delete():
    author = request.json['author']
    text = request.json['text']
    quote = Quote.query.filter_by(author=author, text=text).first()
    db.session.delete(quote)
    db.session.commit()

    return quote_schema.jsonify(quote)


if __name__ == '__main__':
    app.run(debug=True)


