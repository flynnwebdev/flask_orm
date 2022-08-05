from dataclasses import dataclass
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://trello_user:123456@localhost:5432/trello_clone_db"

db = SQLAlchemy(app)

# Declare a model as a dataclass (Python >= 3.7)


@dataclass
class Card(db.Model):
    # Set the db table that will store instances of this model
    __tablename__ = "cards"

    # Define the columns/attributes needed
    # Since it's a dataclass, each attribute must have a type annotation
    # The nice thing about that is we get serialization for free
    id: int = db.Column(db.Integer, primary_key=True)
    title: str = db.Column(db.String(length=150))
    description: str = db.Column(db.Text())
    date: str = db.Column(db.Date())
    status: str = db.Column(db.String())
    priority: str = db.Column(db.String())


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
    # return the data in JSON format
    return jsonify(cards_list)


if __name__ == '__main__':
    app.run(debug=True)
