from pydantic_settings import BaseSettings

#Snowflake Credentials
class DBSettings(BaseSettings):
    db_user: str = "<user>"
    db_password: str = "<password>"
    db_account: str = "<account-id>"
    db_warehouse: str = "<warehouse>"
    db_database: str = "<db-name>"
    db_schema: str = "<schema-name>"

db_settings = DBSettings()

class Constants(BaseSettings):
    SUCCESS: str = "Success"
    ERROR: str = "Error Occured. Please Try again leter!"
    SAGEMAKER_URL: str = "<api-url>"

constants = Constants()