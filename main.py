from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlmodel import Session, select

from database import init_db, engine
from models import User, Message
from schemas import UserCreate, UserRead, MessageCreate, MessageRead


def get_session():
    with Session(engine) as session:
        yield session


app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/")
def read_root():
    return {"message": "API messagerie OK"}


# -----------------------
# USERS
# -----------------------

@app.post("/users", response_model=UserRead, status_code=201)
def create_user(user_in: UserCreate, session: Session = Depends(get_session)):
    existing = session.exec(
        select(User).where(User.username == user_in.username)
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Nom d'utilisateur déjà pris")

    user = User(username=user_in.username, email=user_in.email)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@app.get("/users", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session)):
    return session.exec(select(User)).all()


@app.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return user


# -----------------------
# MESSAGES
# -----------------------

@app.post("/messages", response_model=MessageRead, status_code=201)
def send_message(msg_in: MessageCreate, session: Session = Depends(get_session)):
    sender = session.get(User, msg_in.sender_id)
    receiver = session.get(User, msg_in.receiver_id)

    if not sender or not receiver:
        raise HTTPException(status_code=400, detail="Expéditeur ou destinataire inexistant")

    if msg_in.sender_id == msg_in.receiver_id:
        raise HTTPException(status_code=400, detail="On ne peut pas s'envoyer un message à soi-même")

    if not msg_in.subject.strip() or not msg_in.body.strip():
        raise HTTPException(status_code=400, detail="Sujet et contenu ne doivent pas être vides")

    message = Message(
        sender_id=msg_in.sender_id,
        receiver_id=msg_in.receiver_id,
        subject=msg_in.subject,
        body=msg_in.body,
    )

    session.add(message)
    session.commit()
    session.refresh(message)

    return MessageRead(
        id=message.id,
        sender_id=message.sender_id,
        receiver_id=message.receiver_id,
        sender_name=sender.username,
        receiver_name=receiver.username,
        subject=message.subject,
        body=message.body,
        is_read=message.is_read,
        sent_at=message.sent_at,
    )


# INBOX avec filtres (Partie 5)
@app.get("/users/{user_id}/inbox", response_model=list[MessageRead])
def get_inbox(
    user_id: int,
    unread_only: bool = False,
    search: str | None = None,
    session: Session = Depends(get_session),
):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    query = select(Message).where(Message.receiver_id == user_id)

    if unread_only:
        query = query.where(Message.is_read == False)  # noqa: E712

    if search:
        query = query.where(Message.subject.ilike(f"%{search}%"))

    query = query.order_by(Message.sent_at.desc())

    messages = session.exec(query).all()

    result: list[MessageRead] = []
    for m in messages:
        result.append(
            MessageRead(
                id=m.id,
                sender_id=m.sender_id,
                receiver_id=m.receiver_id,
                sender_name=session.get(User, m.sender_id).username,
                receiver_name=session.get(User, m.receiver_id).username,
                subject=m.subject,
                body=m.body,
                is_read=m.is_read,
                sent_at=m.sent_at,
            )
        )

    return result


@app.get("/users/{user_id}/sent", response_model=list[MessageRead])
def get_sent(user_id: int, session: Session = Depends(get_session)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")

    query = (
        select(Message)
        .where(Message.sender_id == user_id)
        .order_by(Message.sent_at.desc())
    )

    messages = session.exec(query).all()

    result: list[MessageRead] = []
    for m in messages:
        result.append(
            MessageRead(
                id=m.id,
                sender_id=m.sender_id,
                receiver_id=m.receiver_id,
                sender_name=session.get(User, m.sender_id).username,
                receiver_name=session.get(User, m.receiver_id).username,
                subject=m.subject,
                body=m.body,
                is_read=m.is_read,
                sent_at=m.sent_at,
            )
        )

    return result


@app.get("/messages/{message_id}", response_model=MessageRead)
def get_message(message_id: int, session: Session = Depends(get_session)):
    m = session.get(Message, message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message introuvable")

    return MessageRead(
        id=m.id,
        sender_id=m.sender_id,
        receiver_id=m.receiver_id,
        sender_name=session.get(User, m.sender_id).username,
        receiver_name=session.get(User, m.receiver_id).username,
        subject=m.subject,
        body=m.body,
        is_read=m.is_read,
        sent_at=m.sent_at,
    )


@app.patch("/messages/{message_id}/read", response_model=MessageRead)
def mark_as_read(message_id: int, session: Session = Depends(get_session)):
    m = session.get(Message, message_id)
    if not m:
        raise HTTPException(status_code=404, detail="Message introuvable")

    m.is_read = True
    session.add(m)
    session.commit()
    session.refresh(m)

    return MessageRead(
        id=m.id,
        sender_id=m.sender_id,
        receiver_id=m.receiver_id,
        sender_name=session.get(User, m.sender_id).username,
        receiver_name=session.get(User, m.receiver_id).username,
        subject=m.subject,
        body=m.body,
        is_read=m.is_read,
        sent_at=m.sent_at,
    )
