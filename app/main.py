# argon2-cffi this for hashing
# CORS vs CSRF vs XSS vs SQL Injection vs JWT vs OAuth2 vs OpenID Connect


from fastapi import  FastAPI 
from .routers import post , user , auth , vote
from fastapi.middleware.cors import CORSMiddleware

# from . import models 
# from .database import engine 
               
# this will create the tables in the database if they do not exist
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.title = "My FastAPI Application"

app.description = "This is a sample FastAPI application with multiple routers for posts, users, authentication, and voting."

app.version = "1.0.0"



# test fetch from frontend to backend and check if the CORS policy is working or not
#code here  : fetch("http://localhost:8000/")
#   .then(res => res.json())
#   .then(data => console.log(data))
#   .catch(err => console.error(err));


orgins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=orgins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
   

app.include_router(post.router)
app.include_router(user.router)  
app.include_router(auth.router)   
app.include_router(vote.router)
      
      
@app.get("/")
def root():
    return {"message": "Hello World!"}