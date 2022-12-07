from fastapi import status, HTTPException, Depends, Response, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import database, schemas, models, oauth2


from ..database import get_db
from .. import models, schemas, oauth2


router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)


@router.post("/", status_code=status.HTTP_201_CREATED)
async def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user = Depends(oauth2.get_current_user)):

    post = db.query(models.Vote).filter(
        models.Post.id == vote.post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {vote.post_id} does not exist.")

    vote_query = db.query(models.Vote).filter(
        models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"user {current_user.id} has already voted on post.")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    elif vote.dir == 0:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}

    return vote