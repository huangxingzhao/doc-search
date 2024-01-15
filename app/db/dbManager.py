import os

from sqlalchemy import create_engine, AsyncAdaptedQueuePool
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import scoped_session, sessionmaker, Session

project_dir = os.path.dirname(os.path.abspath(__file__))
# engine = create_async_engine('sqlite+aiosqlite:///' + os.path.join(project_dir, 'test.db'), poolclass=AsyncAdaptedQueuePool,
#                              echo=True, pool_size=5,  # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
#                              pool_recycle=3600)
engine = create_async_engine("postgresql+asyncpg://test:test@8.138.112.81/test", poolclass=AsyncAdaptedQueuePool,
                             echo=True, pool_size=5,  # 连接池的大小默认为 5 个，设置为 0 时表示连接无限制
                             pool_recycle=3600)
# engine.connect()
# todo close,pool
db_session:async_sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
