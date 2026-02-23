from .. import models, schemas ,oauth2
from fastapi import status , HTTPException , Depends , Response ,APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from ..database import get_db
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

@router.get("/" , response_model=List[schemas.PostOut])
# @router.get("/")
def get_posts(db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0,search: Optional[str] = ""):
    
    
    
    # posts = db.query(models.Post).limit(limit).all()
    
    
    # if not posts:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
    
    # if posts[0].owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
    #                         detail="Not authorized to perform requested action")
     
     
    # print(limit)
    # models.Post.owner_id == current_user.id,
    # posts = db.query(models.Post).filter(
    #      models.Post.title.contains(search)).limit(limit).offset(skip ).all()
    
    posts  = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(
         models.Post.title.contains(search)).limit(limit).offset(skip ).all()
     
       
    return  posts


@router.post("/", status_code=status.HTTP_201_CREATED , response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db) , current_user: int = Depends(oauth2.get_current_user)):
        
        
    
        new_post = models.Post(owner_id=current_user.id, **post.model_dump())
       
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
                   
        return  new_post             
                       
        
@router.get("/latest", response_model=schemas.Post)
def get_latest_post(db: Session = Depends(get_db) ,current_user: int = Depends(oauth2.get_current_user)):
        post = db.query(models.Post).filter(models.Post.owner_id == current_user.id).order_by(models.Post.created_at.desc()).first()
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No posts found")
        return  post    


@router.get("/{id}" , response_model=schemas.PostOut)
def get_one_post(id: int , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
        # post = db.query(models.Post).filter(models.Post.id == id).first()
        
        post  = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
        
        print(post)
        
        if not post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"post with id: {id} was not found")
        if post[0].owner_id != current_user.id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="Not authorized to perform requested action")
            
        return  post 

    
@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int , db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    query = db.query(models.Post).filter(models.Post.id == id)
    
    deleted_post = query.first() 
    
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")    
        
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    
    
    
    query.delete(synchronize_session=False)
    
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, post: schemas.PostCreate , db: Session = Depends(get_db) ,current_user: int = Depends(oauth2.get_current_user)):
    
    query = db.query(models.Post).filter(models.Post.id == id)
    
    updated_post = query.first()
    
    if updated_post  == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
   
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
   
    query.update(post.model_dump(), synchronize_session=False)
    
    db.commit()
    
    return query.first()
 
 