from flask import Flask
from flask_sqlalchemy import SQLAlchemy
app=Flask(__name__)
#set the database uri using SQLAlchemy.
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://pracdb_dev:123456@localhost:5432/pracdatabase"
# to avoid the deprecation warning
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#create apps cli command and name it create, it will be run in the terminal as 'flask create'
#the cli command will invoke the create_db function
db = SQLAlchemy(app)


@app.cli.command("create")
def create_db():
    db.create_all()
    print("Created database tables")


#create classes/model to create objects/structure of the database
class Card(db.Model):
    #define the table name for the database
    __tablename__ = 'CARDS'
    #set the primary key, we need to define that each attribute is also a column in the db table. db is the object we just created above. 
    id = db.Column(db.Integer, primary_key=True)
    #add the rest of the attributes 
    title = db.Column(db.String())
    description = db.Column(db.String())
    date = db.Column(db.Date())
    status = db.Column(db.String())
    priority = db.Column(db.String())

@app.cli.command("seed")
def seed_db():
    from datetime import date
    # create the card object
    card1 = Card(
        # set the attributes, not the id, SQLAlchemy will manage that for us
        title = "Start the project",
        description = "Stage 1, creating the database",
        status = "To Do",
        priority = "High",
        date = date.today()
    )
    # Add the object as a new row to the table
    db.session.add(card1)
    # commit the changes
    db.session.commit()
    print("Table seeded")  

#if table is dropped/deleted it must be created and then seeded for it to be replaced
@app.cli.command("drop")
def drop_db():
    db.drop_all()
    print("Tables dropped") 


@app.route('/')
def hello():
    return 'Hello World! still working'

@app.route('/test')
def test():
    return 'successful'