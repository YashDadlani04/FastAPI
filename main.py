from fastapi import Depends,FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Product
from database import session, engine
import database_models
from sqlalchemy.orm import Session

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"]
)

database_models.Base.metadata.create_all(bind= engine)

@app.get("/")
def greet():
    return "Welcome to the mainpage"

greet()
products = [
    Product(id=1, name="Phone", description="A smartphone", price=699.99, quantity=50),
    Product(id=2, name="Laptop", description="A powerful laptop", price=999.99, quantity=30),
    Product(id=3, name="Pen", description="A blue ink pen", price=1.99, quantity=100),
    Product(id=4, name="Table", description="A wooden table", price=199.99, quantity=20),
]

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()


def init_db():
    db=session()

    count= db.query(database_models.Product).count
    if count==0:

        for product in products:
            db.add(database_models.Product(**product.model_dump()))
        db.commit()

init_db()

@app.get("/products")
def get_all_products(db:Session = Depends(get_db)):

    db_products= db.query(database_models.Product).all()
    db.close()
    #create database connection
    # db= session()
    # db.query()
    #write the query

    return db_products

@app.get("/product/{id}")
def get_product_by_id(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        return db_product

    return "product not found"
    # for product in products:
    #     if product.id==id:
    #         return product

    # return "product not found"
    # return products[id-1]


# IF we want to add a product                

@app.post("/products")
def add_product(product: Product, db: Session = Depends(get_db)):
    db.add(database_models.Product(**product.model_dump()))
    db.commit()
    # products.append(product)
    return product   

#if we want to upddate the product we use put
@app.put("/products/{id}")
def update_product(id:int, product:Product, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()
    if db_product:
        db_product.name= product.name
        db_product.description= product.description
        db_product.price= product.price
        db_product.quantity=product.quantity
        db.commit()
        return "Product updated successfully"
    
    else:
        return "No Product found"

    # for i in range(len(products)):
    #     products[i].id==id
    #     products[i]= product
    #     return "Product added successfully"

    # return "No Product found" 

# if we want to delete the product
@app.delete("/products/{id}")
def delete_product(id:int, db: Session = Depends(get_db)):
    db_product = db.query(database_models.Product).filter(database_models.Product.id == id).first()

    if db_product:
        db.delete(db_product)
        db.commit()
        return "Product deleted successfully"
    else:
        return "No Product found"
        
    # for i in range(len(products)):
    #         products[i].id==id
    #         del products[i]
    #         return "Product deleted successfully"
    
    # return "No Product found"
