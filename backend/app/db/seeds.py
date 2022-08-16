import asyncio

import asyncpg
from faker import Faker

from app.api.dependencies.database import get_repository
from app.core.config import get_app_settings
from app.db.repositories.comments import CommentsRepository
from app.db.repositories.items import ItemsRepository
from app.db.repositories.users import UsersRepository

fake = Faker()
user_name = [fake.user_name() for i in range(100)]
password = [fake.password() for i in range(100)]
slug = [fake.text() for i in range(100)]
title = [fake.word().title() for i in range(100)]
description = [fake.sentence() for i in range(100)]
comments = [fake.text() for i in range(100)]


async def add_x(x):
    SETTINGS = get_app_settings()
    DATABASE_URL = SETTINGS.database_url.replace("postgres://", "postgresql://")
    conn = await asyncpg.connect(DATABASE_URL)
    itemsRepository = ItemsRepository(conn=conn)
    usersRepository = UsersRepository(conn=conn)
    commentsRepository = CommentsRepository(conn=conn)

    for i in range(x):
        user = await usersRepository.create_user(
            username=user_name[i],
            password=password[i],
            email=user_name[i] + "@gmail.com",
        )
        item = await itemsRepository.create_item(
            slug=slug[i],
            seller=user,
            title=title[i],
            description=description[i],
            image="https://picsum.photos/200",
        )
        comment = await commentsRepository.create_comment_for_item(
            body=comments[i] + str(item), item=item, user=user
        )

    await conn.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(add_x(100))
