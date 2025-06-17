from flask import Blueprint, jsonify, request
from server.models.restaurant_pizza import RestaurantPizza
from server import db

restaurant_pizza_bp = Blueprint('restaurant_pizzas', __name__)

@restaurant_pizza_bp.route('/restaurant_pizzas', methods=['POST'])
def create_restaurant_pizza():
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['price', 'pizza_id', 'restaurant_id']
    if not all(field in data for field in required_fields):
        return jsonify({'errors': ['Missing required fields']}), 400
    
    # Validate price range
    if not 1 <= data['price'] <= 30:
        return jsonify({'errors': ['Price must be between 1 and 30']}), 400
    
    try:
        restaurant_pizza = RestaurantPizza(
            price=data['price'],
            pizza_id=data['pizza_id'],
            restaurant_id=data['restaurant_id']
        )
        
        db.session.add(restaurant_pizza)
        db.session.commit()
        
        # Get associated pizza and restaurant
        pizza = restaurant_pizza.pizza
        restaurant = restaurant_pizza.restaurant
        
        return jsonify({
            'id': restaurant_pizza.id,
            'price': restaurant_pizza.price,
            'pizza': pizza.to_dict(),
            'restaurant': restaurant.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'errors': [str(e)]}), 400