from database import Database
import uuid
from datetime import date

# ARTICULOS

def create_article(user_email, title, text):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (u:User {email: $email})
                CREATE (a:Article {
                    id: $id,
                    title: $title,
                    date: $date,
                    text: $text
                })
                CREATE (u)-[:CREATED]->(a)
                RETURN a.id AS id
            """,
                email=user_email,
                id=str(uuid.uuid4()),
                title=title,
                date=str(date.today()),
                text=text
            )

            record = result.single()
            return record["id"] if record else None

    finally:
        db.close()


def get_articles():
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (a:Article)
                RETURN a.id AS id,
                       a.title AS title,
                       a.date AS date,
                       a.text AS text
                ORDER BY a.date DESC
            """)

            return [dict(record) for record in result]

    finally:
        db.close()


def update_article(article_id, title, text, user_email, role):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (a:Article {id: $id})
                MATCH (u:User {email: $email})
                WHERE $role = 'admin'
                   OR EXISTS {
                       MATCH (u)-[:CREATED]->(a)
                   }
                SET a.title = $title,
                    a.text = $text
                RETURN a.id AS id
            """,
                id=article_id,
                title=title,
                text=text,
                email=user_email,
                role=role
            )

            return result.single() is not None

    finally:
        db.close()


def delete_article(article_id, user_email, role):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (a:Article {id: $id})
                MATCH (u:User {email: $email})
                WHERE $role = 'admin'
                   OR EXISTS {
                       MATCH (u)-[:CREATED]->(a)
                   }
                DETACH DELETE a
                RETURN count(a) AS deleted
            """,
                id=article_id,
                email=user_email,
                role=role
            )

            return result.single()["deleted"] > 0

    finally:
        db.close()

# COMENTARIOS

def create_comment(user_email, article_id, name, url):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (u:User {email: $email})
                MATCH (a:Article {id: $article_id})
                CREATE (c:Comment {
                    id: $id,
                    name: $name,
                    url: $url
                })
                CREATE (u)-[:WROTE]->(c)
                CREATE (a)-[:HAS_COMMENT]->(c)
                RETURN c.id AS id
            """,
                email=user_email,
                article_id=article_id,
                id=str(uuid.uuid4()),
                name=name,
                url=url
            )

            record = result.single()
            return record["id"] if record else None

    finally:
        db.close()


def get_comments(article_id):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (a:Article {id: $id})-[:HAS_COMMENT]->(c:Comment)
                RETURN c.id AS id,
                       c.name AS name,
                       c.url AS url
            """, id=article_id)

            return [dict(record) for record in result]

    finally:
        db.close()



def update_comment(comment_id, name, url, user_email, role):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (c:Comment {id: $id})
                MATCH (u:User {email: $email})
                WHERE $role = 'admin'
                   OR EXISTS {
                       MATCH (u)-[:WROTE]->(c)
                   }
                SET c.name = $name,
                    c.url = $url
                RETURN c.id AS id
            """,
                id=comment_id,
                name=name,
                url=url,
                email=user_email,
                role=role
            )

            return result.single() is not None

    finally:
        db.close()


def delete_comment(comment_id, user_email, role):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (c:Comment {id: $id})
                MATCH (u:User {email: $email})
                WHERE $role = 'admin'
                   OR EXISTS {
                       MATCH (u)-[:WROTE]->(c)
                   }
                DETACH DELETE c
                RETURN count(c) AS deleted
            """,
                id=comment_id,
                email=user_email,
                role=role
            )

            return result.single()["deleted"] > 0

    finally:
        db.close()

# ETIQUETAS

def create_tag(article_id, name, url):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (a:Article {id: $article_id})
                MERGE (t:Tag {name: $name})
                ON CREATE SET t.url = $url
                MERGE (a)-[:HAS_TAG]->(t)
                RETURN t.name AS name
            """,
                article_id=article_id,
                name=name,
                url=url
            )

            return result.single() is not None

    finally:
        db.close()


def get_tags(article_id):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (a:Article {id: $id})-[:HAS_TAG]->(t:Tag)
                RETURN t.name AS name, t.url AS url
            """, id=article_id)

            return [dict(record) for record in result]

    finally:
        db.close()


# CATEGORIAS

def create_category(article_id, name, url):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (a:Article {id: $article_id})
                MERGE (c:Category {name: $name})
                ON CREATE SET c.url = $url
                MERGE (a)-[:IN_CATEGORY]->(c)
                RETURN c.name AS name
            """,
                article_id=article_id,
                name=name,
                url=url
            )

            return result.single() is not None

    finally:
        db.close()


def get_categories(article_id):
    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (a:Article {id: $id})-[:IN_CATEGORY]->(c:Category)
                RETURN c.name AS name, c.url AS url
            """, id=article_id)

            return [dict(record) for record in result]

    finally:
        db.close()

# MODIFICAR Y ELIMINAR ETIQUETAS


def update_tag(name, new_name, url, role):
    if role != "admin":
        return False

    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (t:Tag {name: $name})
                SET t.name = $new_name,
                    t.url = $url
                RETURN t.name AS name
            """,
                name=name,
                new_name=new_name,
                url=url
            )

            return result.single() is not None

    finally:
        db.close()


def delete_tag(name, role):
    if role != "admin":
        return False

    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (t:Tag {name: $name})
                DETACH DELETE t
                RETURN count(t) AS deleted
            """, name=name)

            return result.single()["deleted"] > 0

    finally:
        db.close()

# MODIFICAR Y ELIMINAR CATEGORIAS


def update_category(name, new_name, url, role):
    if role != "admin":
        return False

    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (c:Category {name: $name})
                SET c.name = $new_name,
                    c.url = $url
                RETURN c.name AS name
            """,
                name=name,
                new_name=new_name,
                url=url
            )

            return result.single() is not None

    finally:
        db.close()


def delete_category(name, role):
    if role != "admin":
        return False

    db = Database()

    try:
        with db.driver.session() as session:
            result = session.run("""
                MATCH (c:Category {name: $name})
                DETACH DELETE c
                RETURN count(c) AS deleted
            """, name=name)

            return result.single()["deleted"] > 0

    finally:
        db.close()

def create_sample_data():
    user_email = "admin@blog.com"

    samples = [
        {
            "title": "La importancia de la tecnologia en la educacion",
            "text": "La tecnologia ha transformado la educacion mediante herramientas digitales que facilitan el aprendizaje, la comunicacion y el acceso a la informacion.",
            "category": ("Educacion", "https://example.com/educacion"),
            "tags": [
                ("Tecnologia", "https://example.com/tecnologia"),
                ("Innovacion", "https://example.com/innovacion")
            ],
            "comments": [
                ("Ana", "https://example.com/ana"),
                ("Carlos", "https://example.com/carlos")
            ]
        },
        {
            "title": "Consejos para proteger tu informacion en internet",
            "text": "La seguridad digital es importante para proteger nuestros datos personales. Utilizar contrasenas seguras y evitar enlaces sospechosos ayuda a prevenir riesgos.",
            "category": ("Seguridad", "https://example.com/seguridad"),
            "tags": [
                ("Internet", "https://example.com/internet"),
                ("Privacidad", "https://example.com/privacidad")
            ],
            "comments": [
                ("Luis", "https://example.com/luis"),
                ("Maria", "https://example.com/maria")
            ]
        },
        {
            "title": "El futuro de la inteligencia artificial",
            "text": "La inteligencia artificial ofrece nuevas posibilidades en diferentes areas, como la educacion, la medicina, la industria y el desarrollo de software.",
            "category": ("Tecnologia", "https://example.com/tecnologia"),
            "tags": [
                ("Inteligencia Artificial", "https://example.com/ia"),
                ("Innovacion", "https://example.com/innovacion")
            ],
            "comments": [
                ("Sofia", "https://example.com/sofia"),
                ("Pedro", "https://example.com/pedro")
            ]
        }
    ]

    existing_articles = get_articles()
    created = 0

    for sample in samples:
        article = next(
            (a for a in existing_articles
             if a["title"] == sample["title"]),
            None
        )

        if article is None:
            article_id = create_article(
                user_email,
                sample["title"],
                sample["text"]
            )
            created += 1
        else:
            article_id = article["id"]

        if not article_id:
            continue

        for name, url in sample["comments"]:
            existing_comments = get_comments(article_id)

            if not any(c["name"] == name for c in existing_comments):
                create_comment(user_email, article_id, name, url)

        for name, url in sample["tags"]:
            existing_tags = get_tags(article_id)

            if not any(t["name"] == name for t in existing_tags):
                create_tag(article_id, name, url)

        category_name, category_url = sample["category"]
        existing_categories = get_categories(article_id)

        if not any(c["name"] == category_name for c in existing_categories):
            create_category(article_id, category_name, category_url)

    return created