from fastapi import Depends, FastAPI
from products import Products
from db import SessionLocal,engine
import db_models
from sqlalchemy.orm import session
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods= ["*"]
)
db_models.Base.metadata.create_all(bind=engine)

product=[ 
    Products(id=1,name= "watch",des= "watch", quantity= 21),
    Products(id=2,name= "watch1",des= "watch", quantity= 22),
    Products(id=3,name= "watch",des= "watch", quantity= 23),
    Products(id=4,name= "watch4",des= "watch", quantity= 24)
]
#use to inject on every path function called depency ingestion
def get_db():
     db=SessionLocal()
     try:
        yield db
     finally:     
        db.close()
def init_db():
      db=SessionLocal()
      try:
        # FIXED: Check if the table is already populated before inserting
        if db.query(db_models.Products).count() == 0:
            # FIXED: Changed variable name to 'item' to avoid overwriting your class name
            for item in product:
                db.add(db_models.Products(**item.model_dump())) #unppack from pydanti products to db products
            db.commit()
            print("Database successfully seeded!")
        else:
            print("Database already has records. Skipping seed step.")
      except Exception as e:
        print(f"Error during seeding: {e}")
      finally:
        db.close()

      #creates only non existing records  
      #for Products in product:
           #db.add(db_models.Products(**Products.model_dump())) 
      #db.commit()
init_db()            
      
@app.get("/products")
def get_all_products(db: session = Depends(get_db)):
    #db= SessionLocal()
    #db.query()
    db_products= db.query(db_models.Products).all()
    return db_products
@app.get("/products/{id}")
def get_product_by_id(id:int, db: session = Depends(get_db)):
    db_product=db.query(db_models.Products).filter(db_models.Products.id==id).first()
    if db_product:
        return db_product
    #for i in product:
          #if (i.id== id):
                #return i
@app.post("/products/add")
def add_new_product(item: Products, db: session = Depends(get_db)):
      db.add(db_models.Products(**item.model_dump()))
      db.commit()
      return product
@app.put("/products/update/{id}")
def product_update(id:int, product_update: Products, db: session = Depends(get_db)):
    db_product=db.query(db_models.Products).filter(db_models.Products.id==id).first()
    if db_product:

        db_product.name= product_update.name
        db.commit()
      #for i in range(len(product)):
            #if product[i].id == id:
                  #product[i] = product_update
                  #return product_update
@app.delete("/products/delete")
def product_update(id:int, db: session = Depends(get_db)):
    db_product=db.query(db_models.Products).filter(db_models.Products.id==id).first()
    if db_product:
        db.delete(db_product)
        db.commit()
      #for i in range(len(product)):
            #if product[i].id == id:
                  #del product[i]
                  #return "product_delete"