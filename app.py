from flask import Flask,render_template,jsonify,request
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
from Model import db,Jewellery,Customer,CartItem
from flask_jwt_extended import JWTManager ,create_access_token,jwt_required,get_jwt_identity


app=Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['JWT_SECRET_KEY'] = 'SwarnAbhusan'
db.init_app(app)
CORS(app,origins=['http://localhost:5173'],supports_credentials=True)

jwt=JWTManager(app)

@app.route('/')
def home():
        with app.app_context():
        db.create_all()
        # Only add sample data if the table is empty
        if Jewellery.query.count() == 0:
            sample_data = [
                {
                    "name": "Golden Necklace",
                    "price": 29999,
                    "description": "Elegant golden necklace with intricate detailing and a timeless design.",
                    "image1": "https://images.unsplash.com/photo-1601121141418-c1caa10a2a0b?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGdvbGQlMjBqZXdlbGxlcnl8ZW58MHx8MHx8fDA%3D",
                    "image2": "https://images.unsplash.com/photo-1566982038008-464dc5e1c7cd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                    "image3": "https://images.unsplash.com/photo-1560347876-aeef00ee58a1?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                },
                {
                    "name": "Luxury Bracelet",
                    "price": 19999,
                    "description": "A stylish bracelet crafted with high-quality gold for a luxurious look.",
                    "image1": "https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGdvbGQlMjBqZXdlbGxlcnl8ZW58MHx8MHx8fDA%3D",
                    "image2": "https://images.unsplash.com/photo-1616596849592-86a29af3b1ad?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                    "image3": "https://images.unsplash.com/photo-1617963804281-93b8ed0d84ea?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                },
                {
                    "name": "Elegant Earrings",
                    "price": 12999,
                    "description": "Delicate earrings that add a touch of elegance to any outfit.",
                    "image1": "https://images.unsplash.com/photo-1626784215013-13322cb0e471?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8NHx8Z29sZCUyMGpld2VsbGVyeXxlbnwwfHwwfHx8MA%3D%3D",
                    "image2": "https://images.unsplash.com/photo-1581326444541-47a8c8b7a214?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                    "image3": "https://images.unsplash.com/photo-1583132339361-2192774ff90d?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                },
                {
                    "name": "Classic Ring",
                    "price": 34999,
                    "description": "A timeless ring set in gold with a sparkling diamond centerpiece.",
                    "image1": "https://images.unsplash.com/photo-1629118639934-2b241503956c?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTR8fGdvbGQlMjBqZXdlbGxlcnl8ZW58MHx8MHx8fDA%3D",
                    "image2": "https://images.unsplash.com/photo-1603443075446-83d6c2843a6a?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                    "image3": "https://images.unsplash.com/photo-1606813900898-880cf7312c25?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                },
                {
                    "name": "Stylish Pendant",
                    "price": 27999,
                    "description": "A modern pendant that stands out with its unique design and refined craftsmanship.",
                    "image1": "https://images.unsplash.com/photo-1569397288884-4d43d6738fbd?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTh8fGdvbGQlMjBqZXdlbGxlcnl8ZW58MHx8MHx8fDA%3D",
                    "image2": "https://images.unsplash.com/photo-1589558049853-e9fa98b3d110?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                    "image3": "https://images.unsplash.com/photo-1589558249351-e6065ea9d53c?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                },
                {
                    "name": "Chic Brooch",
                    "price": 8999,
                    "description": "A chic brooch designed to add a subtle sparkle and complete your look.",
                    "image1": "https://images.unsplash.com/photo-1617038220319-276d3cfab638?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8OHx8Z29sZCUyMGpld2VsbGVyeXxlbnwwfHwwfHx8MA%3D%3D",
                    "image2": "https://images.unsplash.com/photo-1585036627131-9896b98d9d0b?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                    "image3": "https://images.unsplash.com/photo-1585036571232-8aab8a24d88e?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                },
                {
                    "name": "Chains",
                    "price": 49999,
                    "description": "A majestic crown that symbolizes luxury, elegance, and regal style.",
                    "image1": "https://plus.unsplash.com/premium_photo-1709033404514-c3953af680b4?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTN8fGdvbGQlMjBqZXdlbGxlcnl8ZW58MHx8MHx8fDA%3D",
                    "image2": "https://images.unsplash.com/photo-1583142307388-31f2d43cf1bb?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                    "image3": "https://images.unsplash.com/photo-1583142307340-dcf26a5e4a31?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                },
                {
                    "name": "Modern Bangle",
                    "price": 15999,
                    "description": "A sleek bangle with a contemporary design that makes a bold statement.",
                    "image1": "https://images.unsplash.com/photo-1602173574767-37ac01994b2a?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTJ8fGdvbGQlMjBqZXdlbGxlcnl8ZW58MHx8MHx8fDA%3D",
                    "image2": "https://images.unsplash.com/photo-1573496869437-df4e7e4d7fef?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
                    "image3": "https://images.unsplash.com/photo-1573496869456-8c0d1e5b70c9?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80"
                }
                ]
            for item in sample_data:
                new_item = Jewellery(
                    name=item["name"],
                    price=item["price"],
                    description=item["description"],
                    image1=item["image1"],  # or store all images if needed
                    image2=item["image2"],  # or store all images if needed
                    image3=item["image3"],  # or store all images if needed

                    category="Gold Jewellery",  # example category
                    rating=0.0  # default rating, or use a value if provided
                )
                db.session.add(new_item)
            db.session.commit()

    return 'Hii'

@app.route('/api/cards', methods=['GET'])
def getcards():
    Jewllery = Jewellery.query.all()
    return jsonify([jewellery.to_dict() for jewellery in Jewllery])

# if __name__=='__main__':



@app.route('/api/Signup',methods=['POST'])
def signup():
    data=request.get_json()
    Email=data.get('email')
    Password=data.get("password")
    Address=data.get("address")
    Phone=data.get("number")

    if Customer.query.filter_by(email=Email).first():
        return jsonify({"message":"User already exists"}),400
    else:
        new_user=Customer(
            email=Email,
            password=Password,
            address=Address,
            phone=Phone   

        )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message":"User created successfully"}),200
       
@app.route('/api/Login',methods=['POST'])
def login():
    data=request.get_json()
    print(data)
    email=data.get("email")
    password=data.get("password")

    user=Customer.query.filter_by(email=email).first()


    if user:
        if user.password==password:
            Token=create_access_token(identity=user.email)
            return jsonify(access_token=Token,ok=True),200
        else:
            return jsonify({"message":"Invalid password"}),400
    else:
        return jsonify({"message":"User not found"}),404

@app.route('/api/Cart',methods=['POST','GET'])
@jwt_required()
def cart():
    data=request.get_json()
    prod_id=data.get("Prod_id")
    user_email=get_jwt_identity()
    user=Customer.query.filter_by(email=user_email).first()
    
    if user:

        ci=CartItem(
            customer=user,
            jewellery_id=prod_id,
            quantity=1
        )
        if ci in user.cart_items:

            Use=CartItem.query.filter_by(customer=user,jewellery_id=prod_id).first()
            if Use:
                Use.quantity+=1
                db.session.commit()
                return jsonify({"message":"One More Item Added"})
        
        user.cart_items.append(ci)
        db.session.commit()
        return jsonify({"message":"Item added to cart"}),200
    else:
        return jsonify({"message":"User not found"}),404


@app.route('/api/getcart',methods=['GET'])
@jwt_required()
def getcart():
    user_email=get_jwt_identity()
    user=Customer.query.filter_by(email=user_email).first()
    if user:
        cart_items = CartItem.query.filter_by(customer=user).all()
        products = []
        for items in cart_items:
            item = Jewellery.query.filter_by(id=items.jewellery_id).first().to_dict()
            item['quantity'] = items.quantity
            item['owner']= user.name
            item['address']=user.address
            item['phone']=user.phone
            item['email']=user.email
            products.append(item)
        print(products)
        return jsonify(products)
        
    else:
        return jsonify({"message":"User not found"}),404

@app.route('/api/DelCart',methods=['DELETE'])
@jwt_required()
def removeitem():
    data=request.get_json()
    prod_id=data.get("Prod_id")
    user_email=get_jwt_identity()
    user=Customer.query.filter_by(email=user_email).first()
    
    if user:
        item=CartItem.query.filter_by(customer=user,jewellery_id=prod_id).first()
        if item:
            item.quantity-=1
            if item.quantity <= 0:
                db.session.delete(item)
            else:
                db.session.commit()
            db.session.commit()
            return jsonify({"message":"Item removed from cart"}),200
        else:
            return jsonify({"message":"Item not found in cart"}),404
    else:
        return jsonify({"message":"User not found"}),404

app.run(debug=True)
#   
