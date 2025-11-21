import json 
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
# We assume load_dotenv is called earlier, but adding it here for completeness
from dotenv import load_dotenv 

# Load environment variables (from .env locally, or Render ENV in production)
load_dotenv()

db_url_raw = os.getenv("DATABASE_URL")
# This variable is set by the Dockerfile (ENV SQLALCHEMY_CONNECT_ARGS)
ssl_connect_args_json = os.getenv("SQLALCHEMY_CONNECT_ARGS") 

if db_url_raw is None:
    # This prevents the application from starting if the URL is missing
    raise EnvironmentError(
        "DATABASE_URL not found in environment variables. Deployment will fail."
    )
    
# --- FINAL FIX: TRANSFORM THE DIALECT TO USE PYMYSQL ---
DATABASE_URL = db_url_raw
if DATABASE_URL.startswith('mysql'):
    # This replaces 'mysql:' (from TiDB ENV) or 'mysql+mysqlconnector' (from local dev)
    # with the correct installed driver: 'mysql+pymysql'
    # The '1' limits the replacement to the first occurrence
    DATABASE_URL = DATABASE_URL.replace('mysql:', 'mysql+pymysql:', 1).replace('mysql+mysqlconnector', 'mysql+pymysql')
    
# --- SSL CONNECTION LOGIC (CRUCIAL FOR TiDB) ---
connect_args = {}
if ssl_connect_args_json:
    try:
        # We parse the JSON string provided by the Dockerfile ENV variable
        connect_args = json.loads(ssl_connect_args_json)
    except json.JSONDecodeError as e:
        # If the JSON is invalid, the deployment is faulty
        raise EnvironmentError(f"SQLALCHEMY_CONNECT_ARGS is invalid JSON: {e}")

# --- ENGINE CREATION (Uses the transformed URL and SSL args) ---
engine = create_engine(
    DATABASE_URL, 
    pool_pre_ping=True, 
    pool_recycle=3600,
    # This applies the '{"ssl": {"ca": "tidb_ca_cert.pem"}}' to the driver
    connect_args=connect_args 
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
