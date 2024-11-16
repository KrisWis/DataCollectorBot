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
    async def add_user(user_id: int, user_reg_date: date, user_geo: str) -> bool:

        user = await AsyncORM.get_user(user_id=user_id)

        if not user:
            user = UsersOrm(user_id=user_id, user_reg_date=user_reg_date, user_geo=user_geo, user_join_contacts=False)
            async with async_session() as session:
                session.add(user)

                await session.commit() 
            return True
        else:
            return False
        

    # Изменение того, что юзер зашел в контакты
    @staticmethod
    async def user_join_contacts(user_id: int) -> bool:
        async with async_session() as session:
            stmt = (update(UsersOrm)
                    .where(UsersOrm.user_id == user_id)
                    .values(user_join_contacts=True))
            
            await session.execute(stmt)
            await session.commit()
            return True