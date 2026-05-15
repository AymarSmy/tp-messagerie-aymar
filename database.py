from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///./messagerie.db"

engine = create_engine(DATABASE_URL, echo=False)


def init_db() -> None:
    import models  

    SQLModel.metadata.create_all(engine)

