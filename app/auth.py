from database import Database
import hashlib

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# REGISTRAR USUARIO

def register_user(name, email, password):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                CREATE (u:User {
                    name: $name,
                    email: $email,
                    password: $password,
                    role: 'user'
                })
                RETURN u.name AS name
            """,
                name=name,
                email=email,
                password=hash_password(password)
            )

            return result.single() is not None

    except Exception:
        return False

    finally:
        db.close()


# INICIAR SESION

def login_user(email, password):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (u:User {email: $email})
                RETURN u.name AS name,
                       u.email AS email,
                       u.password AS password,
                       u.role AS role
            """, email=email)

            user = result.single()

            if user and user["password"] == hash_password(password):
                return {
                    "name": user["name"],
                    "email": user["email"],
                    "role": user["role"]
                }

            return None

    finally:
        db.close()


# CREAR ADMINISTRADOR

def create_admin(name, email, password):
    db = Database()

    try:
        with db.driver.session() as session:
            session.run("""
                MERGE (u:User {email: $email})
                ON CREATE SET
                    u.name = $name,
                    u.password = $password,
                    u.role = 'admin'
            """,
                name=name,
                email=email,
                password=hash_password(password)
            )

        return True

    except Exception as error:
        print("Error al crear administrador:", error)
        return False

    finally:
        db.close()