import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


# Load the variables from the .env file
load_dotenv()

# Get the database URL from the environment variables
DATABASE_URL = os.environ["DATABASE_URL"]

# Create the SQLAlchemy engine
engine = create_engine(DATABASE_URL)

# Create a session factory using the database engine
SessionFactory = sessionmaker(bind=engine)

# Create a database session
db_session = SessionFactory()