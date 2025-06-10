from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text

from config.settings import db_settings
from models.review import Review

def connect_snowflake():
    engine = create_engine(
        f'snowflake://{db_settings.db_user}:{db_settings.db_password}@{db_settings.db_account}/{db_settings.db_database}/{db_settings.db_schema}?warehouse={db_settings.db_warehouse}'
    )

    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def get_random_user_ids(session, limit=10):
    table_name = Review.__tablename__
    query = text(f"""
        SELECT DISTINCT "User ID"
        FROM {table_name}
        ORDER BY RANDOM()
        LIMIT :limit
    """)
    result = session.execute(query, {'limit': limit})
    return [row[0] for row in result]

def get_purchased(session, user_id):
    table_name = Review.__tablename__
    query = text(f"""
        SELECT DISTINCT "Product Title"
        FROM {table_name}
        WHERE "User ID"=:user_id
        LIMIT 10
    """)
    results = session.execute(query, {"user_id": user_id})
    return [row[0] for row in results]