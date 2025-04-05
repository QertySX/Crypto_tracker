from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from core.models.users import Base
from core.settings import settings

# СОЗДАНИЕ ФАБРИКИ СЕССИЙ
class DatabaseHelper:
    def __init__(self, port: str, host: str, name: str, password: str, user: str):
        self.engine = create_async_engine(
            f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{name}",
        )
        self.session_factory = async_sessionmaker(
            bind=self.engine, autoflush=False,
            autocommit=False,
            expire_on_commit=False
        )

    async def create_db(self):
        async with self.engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

db_helper = DatabaseHelper(
    port=settings.port,
    host=settings.host,
    name=settings.name,
    password=settings.password,
    user=settings.user
)


