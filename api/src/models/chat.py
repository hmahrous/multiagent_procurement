# SQL Alchemy models declaration.
# https://docs.sqlalchemy.org/en/20/orm/quickstart.html#declare-models
# mapped_column syntax from SQLAlchemy 2.0.

# https://alembic.sqlalchemy.org/en/latest/tutorial.html
# Note, it is used by alembic migrations logic, see `alembic/env.py`

# Alembic shortcuts:
# # create migration
# alembic revision --autogenerate -m "migration_name"

# # apply all migrations
# alembic upgrade head


from api.src.models import Base
from sqlalchemy import BigInteger, String
from sqlalchemy.orm import mapped_column


# This is a sample class which represents table in database
class Chat(Base):
    __tablename__ = "chat"

    id = mapped_column(BigInteger, primary_key=True)
    prompt = mapped_column(String, nullable=False, default=False)
