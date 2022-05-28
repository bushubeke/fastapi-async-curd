
  
from setuptools import setup

dependencies=["SQLAlchemy>=1.4.32","psycopg2-binary>=2.9.3","asyncpg>=0.25.0","fastapi>=0.75.0","email-validator==1.1.3","PyJWT>=2.3.0","passlib>=1.7.4","sqlalchemy-json>=0.5.0"]
# Metadata goes in setup.cfg. These are here for GitHub's dependency graph.
setup(name="Flask-SQLAlchemy", install_requires=dependencies)