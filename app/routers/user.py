from .. import models, schemas, utils
from fastapi import Response, status , HTTPException ,  Depends , APIRouter

from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)




@router.post("/", status_code=status.HTTP_201_CREATED , response_model=schemas.UserOut) 
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db),):
    
    
    # Hash the password - user.password
    hashed_password = utils.hash_password(user.password)
    user.password = hashed_password
    
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
                   
    return  new_user        


@router.get("/{id}" ,response_model=schemas.UserOut)
def get_user(id: int , db: Session = Depends(get_db) ):
        
        user  = db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"user with id: {id} was not found")
        return  user          


@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)  
def delete_user(id: int , db: Session = Depends(get_db)):
    
    user_query = db.query(models.User).filter(models.User.id == id)
    
    deleted_user = user_query.first()
    
    if deleted_user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} was not found")
        
    user_query.delete(synchronize_session=False)
    
    db.commit()    
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)


