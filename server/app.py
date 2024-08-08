from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=["GET","POST"])
def messages():
    print(request.method)
    if request.method=="GET":
        all_ms = Message.query.order_by(Message.created_at.asc()).all()
        r_list = []
        for message in all_ms:
            r_list.append(message.to_dict())
        return r_list,200
    elif request.method=="POST":

        try:
            data = request.get_json()
            new_message = Message(
                body = data["body"],
                username=data["username"]
            )
            db.session.add(new_message)
            db.session.commit()
            return new_message.to_dict(),201
        except Exception as e:
            print(e)
            return {
                "Error": "Please input all values"
            },400

@app.route('/messages/<int:id>', methods=["GET","PATCH","DELETE"])
def messages_by_id(id):
  
    message = Message.query.filter(Message.id == id).first()
    if message:
        if request.method == "GET":
                return message.to_dict()
        elif request.method=="PATCH":
            try:
                data = request.get_json()
                for key in data:
                    # setattr(object you are changing, key you are changing, what you are changing it to)
                    setattr(message,key,data[key])
                db.session.add(message)
                db.session.commit()
                return message.to_dict(),200
            except Exception as e:
                print(e)
                return {
                    "error": "Validation Error"
                },400
        elif request.method=="DELETE":
            db.session.delete(message)
            db.session.commit()
            return {}
                
    else:
        return {
            "Error": "Not valid id"
        },400
    
if __name__ == '__main__':
    app.run(port=5555)
