from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://trello_user:123456@localhost:5432/trello_clone_db"

db = SQLAlchemy(app)
ma = Marshmallow(app)


# Declare a model
class Card(db.Model):
    # Set the db table that will store instances of this model
    __tablename__ = "cards"

    # Define the columns/attributes needed
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(length=150))
    description = db.Column(db.Text())
    date = db.Column(db.Date())
    status = db.Column(db.String())
    priority = db.Column(db.String())


class CardSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'date', 'status', 'priority')


@app.cli.command('create')
def create_db():
    # Tell SQLAlchemy to create all tables for all models in the physical DB
    db.create_all()
    print('Tables created')


@app.cli.command('seed')
def seed_db():
    from datetime import date

    # Create a new Card (in memory)
    card = Card(
        title="Start the project",
        description="Stage 1 - create db",
        status="To Do",
        priority="High",
        date=date.today()
    )

    # Add the new card to the current transaction (in memory)
    db.session.add(card)
    # Commit the transaction to the physical DB
    db.session.commit()

    print('Table seeded')


@app.route('/')
def index():
    return 'Hello World!'


@app.route('/cards')
def cards():
    # get all the cards from the database table
    cards_list = Card.query.all()
    # Convert the cards from the database into a JSON format and store them in result
    result = CardSchema(many=True).dump(cards_list)
    # return the data in JSON format
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
