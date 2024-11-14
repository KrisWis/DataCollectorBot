from sqlalchemy import *
from database.models import UsersOrm
from database.db import Base, engine, async_session, date

# Создаём класс для ORM
class AsyncORM:
    # Метод для создания таблиц
    @staticmethod
    async def create_tables():

        async with engine.begin() as conn:
            engine.echo = False

            assert engine.url.database == 'test', 'Дропать прод запрещено'

            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            engine.echo = True


    # Получение пользователя по id
    @staticmethod
    async def get_user(user_id: int) -> UsersOrm:
        async with async_session() as session:

            result = await session.get(UsersOrm, user_id)

            return result
        

    # Добавление пользователя в базу данных
    @staticmethod
    async def add_user(user_id: int, username: str, user_reg_date: date, user_geo: str) -> bool:

        user = await AsyncORM.get_user(user_id=user_id)

        if not user:
            user = UsersOrm(user_id=user_id, username=username, user_reg_date=user_reg_date, user_geo=user_geo)
            async with async_session() as session:
                session.add(user)

                await session.commit() 
            return True
        else:
            return False