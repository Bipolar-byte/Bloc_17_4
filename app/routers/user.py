from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from app.models.user import User
from app.schemas import CreateUser, UpdateUser
from slugify import slugify

router = APIRouter(prefix='/users', tags=['users'])


@router.get('/')
async def all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get('/{user_id}')
async def user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post('/create')
async def create_user(user: CreateUser, db: Session = Depends(get_db)):
    new_user = User(
        username=user.username,
        firstname=user.firstname,
        lastname=user.lastname,
        age=user.age,
        slug=slugify(user.username)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Обновляем объект с новым ID (если база возвращает его)
    return {
        'status_code': status.HTTP_201_CREATED,
        'transaction': 'User created successfully',
        'user': new_user  # Возвращаем созданного пользователя
    }


@router.put('/update/{user_id}')
async def update_user(user_id: int, user: UpdateUser, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    for key, value in user.dict(exclude_unset=True).items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)  # Обновляем объект с новыми данными
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User updated successfully',
        'user': db_user  # Возвращаем обновленного пользователя
    }


@router.delete('/delete/{user_id}')
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {
        'status_code': status.HTTP_200_OK,
        'transaction': 'User deleted successfully',
        'user_id': user_id  # Возвращаем ID удаленного пользователя
    }
