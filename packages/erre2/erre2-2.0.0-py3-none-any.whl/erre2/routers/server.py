from fastapi import APIRouter, Depends, Request, HTTPException
from erre2_0.dependencies import get_auth_token, get_db, get_erre2_version
from erre2_0.authentication import get_current_user, check_admin
from erre2_0.database.crud import get_server, update_server
from sqlalchemy.orm import Session
from erre2_0.database import schemas, models
from typing import Optional
import bcrypt

router = APIRouter(
    prefix="/server",
    tags=["server"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", tags=["server"], response_model=schemas.Server)
async def read_server(request: Request, db: Session = Depends(get_db)):
    """
    Gets current state of server
    """
    s: models.Server = get_server(db)
    return schemas.Server(name=s.name, university=s.university, monetization_link=s.monetization_link, motd=s.motd,
                          owner_id=s.owner_id,
                          owner=s.owner.to_schema())


@router.patch("/", tags=["server"], response_model=schemas.Server)
async def patch_server(request: Request, server: schemas.Server, db: Session = Depends(get_db),
                       current_user: models.User = Depends(get_current_user)):
    """
    Updates the state of the server
    """
    if not check_admin(current_user):
        raise HTTPException(403, "You are not authorized.")
    s: models.Server = update_server(db, server)
    if s:
        return schemas.Server(name=s.name, university=s.university, monetization_link=s.monetization_link, motd=s.motd,
                              owner_id=s.owner_id)


@router.get("/planetarium", tags=["server"], response_model=schemas.Planetarium)
async def planetarium_retrieve(version=Depends(get_erre2_version), db: Session = Depends(get_db)):
    """
    Responds to the planetarium master server
    """
    s = get_server(db)
    if s:
        return schemas.Planetarium(version=version, type="Erre2",
                                   server=schemas.Server(name=s.name, university=s.university,
                                                         monetization_link=s.monetization_link,
                                                         motd=s.motd, owner_id=s.owner_id,
                                                         owner=s.owner.to_schema()))
