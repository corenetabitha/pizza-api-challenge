import sys
import os
from flask_sqlalchemy import SQLAlchemy

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now import your app
from server import create_app, db
from server.models.restaurant import Restaurant
from server.models.pizza import Pizza
from server.models.restaurant_pizza import RestaurantPizza

app = create_app()

with app.app_context():
    # Clear existing data
    RestaurantPizza.query.delete()
    Pizza.query.delete()
    Restaurant.query.delete()
    
    # Create restaurants
    r1 = Restaurant(name="Dominion Pizza", address="Good Italian, Ngong Road, 5th Avenue")
    r2 = Restaurant(name="Pizza Hut", address="Westgate Mall, Mwanzi Road, Nrb 100")
    
    # Create pizzas
    p1 = Pizza(name="Cheese", ingredients="Dough, Tomato Sauce, Cheese")
    p2 = Pizza(name="Pepperoni", ingredients="Dough, Tomato Sauce, Cheese, Pepperoni")
    
    # Add and commit
    db.session.add_all([r1, r2, p1, p2])
    db.session.commit()
    
    # Create restaurant_pizzas
    rp1 = RestaurantPizza(price=5, pizza_id=p1.id, restaurant_id=r1.id)
    rp2 = RestaurantPizza(price=10, pizza_id=p2.id, restaurant_id=r1.id)
    rp3 = RestaurantPizza(price=8, pizza_id=p1.id, restaurant_id=r2.id)
    
    db.session.add_all([rp1, rp2, rp3])
    db.session.commit()
    
    print("Database seeded successfully!")