from flask import Blueprint, request, jsonify
from marvel_comic_characters.helpers import token_required,random_comic_generator
from marvel_comic_characters.models import db, Comic, comic_schema, comics_schema

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/getdata')
@token_required
def getdata(our_user):
    return {'some': 'value'}


#Create Comic Endpoint
@api.route('/drones', methods = ["POST"])
@token_required
def create_comic(our_user):
    
    name = request.json['name']
    description = request.json['description']
    price = request.json['price']
    
    random_comic =  random_comic_generator()
    user_token = our_user.token

    print(f"User Token: {our_user.token}")

    drone = Comic(name, description, price) 
    db.session.add(comic)
    db.session.commit()

    response =comic_schema.dump(drone)

    return jsonify(response)

#Retrieve(READ) all comics drones
@api.route('/drones', methods = ['GET'])
@token_required
def get_comics(our_user):
    owner = our_user.token
    drones = Comic.query.filter_by(user_token = owner).all()
    response = comics_schema.dump(drones)

    return jsonify(response)

#retrieve one sigular individual lonely comic

@api.route('/drones/<id>', methods = ['GET'])
@token_required
def get_drone(our_user, id):    
    if id:
        comic = Comic.query.get(id)
        response = comic_schema.dump(comic)
        return jsonify(response)
    else:
        return jsonify({'message': 'Valid Id equired'}), 401
    
#update drone by id
@api.route('/drones/<id>', methods = ["PUT"])
@token_required
def update_drone(our_user, id): 
    comic = Comic.query.get(id)   
    comic.name = request.json['name']
    comic.description = request.json['description']
    
    comic.random_comic = random_comic_generator()
    comic.user_token = our_user.token  

    db.session.commit()

    response = comic_schema.dump(comic)

    return jsonify(response)
#Delete comic by id
@api.route('/drones/<id>', methods = ['DELETE'])
@token_required
def delete_drones(our_user, id):
    comic = Comic.query.get(id)
    db.session.delete(comic)
    db.session.commit()

    response = comic_schema.dump(comic)
    return jsonify(response)
