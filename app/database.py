import os
from pathlib import Path

from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv(Path(__file__).resolve().parent.parent / ".env")


class Database:

    def __init__(self):
        uri = os.getenv("NEO4J_URI")
        user = os.getenv("NEO4J_USER")
        password = os.getenv("NEO4J_PASSWORD")

        if not uri or not user or not password:
            raise ValueError(
                "Faltan las credenciales de conexion en el archivo .env"
            )

        self.driver = GraphDatabase.driver(
            uri,
            auth=(user, password)
        )

    def verify_connection(self):
        self.driver.verify_connectivity()
        return True

    def close(self):
        self.driver.close()