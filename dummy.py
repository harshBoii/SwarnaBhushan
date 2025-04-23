# from fastapi import FastAPI, Depends, HTTPException, status, Request
# from fastapi.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi_jwt_extended import (
#     JWTManager, create_access_token, jwt_required, get_jwt_identity
# )
# from sqlalchemy.orm import Session
# from pydantic import BaseModel, EmailStr
# from typing import List, Optional

# from Model import db, Jewellery, Customer, CartItem  # Your SQLAlchemy models
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker

# # Database setup
# DATABASE_URL = "sqlite:///./test.db"
# engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# # FastAPI app setup
# app = FastAPI()

# # CORS setup
# origins = ["http://localhost:5173"]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# # JWT setup
# app.state.jwt_secret_key = "SwarnAbhusan"
# jwt = JWTManager(app)

# # Dependency to get DB session
# def get_db():
#     db_session = SessionLocal()
#     try:
#         yield db_session
#     finally:
#         db_session.close()

# # Pydantic Schemas
# class JewellerySchema(BaseModel):
#     id: Optional[int]
#     name: str
#     price: float
#     description: str
#     image1: str
#     image2: str
#     image3: str
#     category: Optional[str]
#     rating: Optional[float]

#     class Config:
#         orm_mode = True

# class SignupRequest(BaseModel):
#     email: EmailStr
#     password: str
#     address: str
#     number: str

# class LoginRequest(BaseModel):
#     email: EmailStr
#     password: str

# class CartRequest(BaseModel):
#     Prod_id: int

# # Startup event to create tables and insert sample data
# @app.on_event("startup")
# def startup():
#     db.metadata.create_all(bind=engine)
#     db_session = SessionLocal()
#     if db_session.query(Jewellery).count() == 0:
#         sample_data = [
#             {
#                 "name": "Golden Necklace",
#                 "price": 29999,
#                 "description": "Elegant golden necklace with intricate detailing and a timeless design.",
#                 "image1": "https://images.unsplash.com/photo-1601121141418-c1caa10a2a0b?w=900&auto=format&fit=crop&q=60&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MTB8fGdvbGQlMjBqZXdlbGxlcnl8ZW58MHx8MHx8fDA%3D",
#                 "image2": "https://images.unsplash.com/photo-1566982038008-464dc5e1c7cd?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
#                 "image3": "https://images.unsplash.com/photo-1560347876-aeef00ee58a1?ixlib=rb-1.2.1&auto=format&fit=crop&w=800&q=80",
#                 "category": "Gold Jewellery",
#                 "rating": 0.0
#             },
#             # ... (add the rest of your sample data here)
#         ]
#         for item in sample_data:
#             new_item = Jewellery(**item)
#             db_session.add(new_item)
#         db_session.commit()
#     db_session.close()

# @app.get("/")
# def home():
#     return {"message": "Hii"}

# @app.get("/api/cards", response_model=List[JewellerySchema])
# def get_cards(db: Session = Depends(get_db)):
#     jewellery = db.query(Jewellery).all()
#     return jewellery

# @app.post("/api/Signup")
# def signup(request: SignupRequest, db: Session = Depends(get_db)):
#     if db.query(Customer).filter_by(email=request.email).first():
#         raise HTTPException(status_code=400, detail="User already exists")
#     new_user = Customer(
#         email=request.email,
#         password=request.password,
#         address=request.address,
#         phone=request.number
#     )
#     db.add(new_user)
#     db.commit()
#     return {"message": "User created successfully"}

# @app.post("/api/Login")
# def login(request: LoginRequest, db: Session = Depends(get_db)):
#     user = db.query(Customer).filter_by(email=request.email).first()
#     if user:
#         if user.password == request.password:
#             token = create_access_token(identity=user.email)
#             return {"access_token": token, "ok": True}
#         else:
#             raise HTTPException(status_code=400, detail="Invalid password")
#     else:
#         raise HTTPException(status_code=404, detail="User not found")

# @app.post("/api/Cart")
# @jwt_required()
# def add_to_cart(request: CartRequest, db: Session = Depends(get_db)):
#     user_email = get_jwt_identity()
#     user = db.query(Customer).filter_by(email=user_email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     prod_id = request.Prod_id
#     ci = CartItem(customer=user, jewellery_id=prod_id, quantity=1)
#     existing = db.query(CartItem).filter_by(customer=user, jewellery_id=prod_id).first()
#     if existing:
#         existing.quantity += 1
#         db.commit()
#         return {"message": "One More Item Added"}
#     user.cart_items.append(ci)
#     db.commit()
#     return {"message": "Item added to cart"}

# @app.get("/api/getcart")
# @jwt_required()
# def get_cart(db: Session = Depends(get_db)):
#     user_email = get_jwt_identity()
#     user = db.query(Customer).filter_by(email=user_email).first()
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     cart_items = db.query(CartItem).filter_by(customer=user).all()
#     products = []
#     for items in cart_items:
#         item = db.query(Jewellery).filter_by(id=items.jewellery_id).first()
#         if item:
#             item_dict = item.to_dict()
#             item_dict['quantity'] = items.quantity
#             item_dict['owner'] = getattr(user, 'name', None)
#             item_dict['address'] = user.address
#             item_dict['phone'] = user.phone
#             item_dict['email'] = user.email
#             products.append(item_dict)
#     return products

# # Run with: uvicorn main:app --reload

