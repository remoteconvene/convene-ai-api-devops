from sqlalchemy.orm import Session

from src.apis.v1.models.auth import ConsumerAuthRequest
from src.core.db.models.consumer import Consumer
from src.core.db.models.consumer_token import ConsumerToken
from src.core.db.sql_session_manager import get_db


def update_consumer_token(consumer: Consumer, auth: ConsumerAuthRequest, token: str):
    with get_db() as db:
        if not consumer_token_exists(db, consumer, auth):
            new_consumer_token = ConsumerToken(
                consumer_id=consumer.id,
                email=auth.email,
                scopes=", ".join(auth.scopes) if len(auth.scopes) > 0 else "",
                jwt_token=token,
                status=True,
            )
            db.add(new_consumer_token)
            db.commit()
            db.refresh(new_consumer_token)
        else:
            db.query(ConsumerToken).filter(
                (ConsumerToken.consumer_id == consumer.id)
                & (ConsumerToken.email == auth.email)
            ).update({"jwt_token": token})
            db.commit()


def consumer_token_exists(
    db: Session, consumer: Consumer, auth: ConsumerAuthRequest
) -> bool:
    return (
        db.query(ConsumerToken)
        .filter(
            (ConsumerToken.consumer_id == consumer.id)
            & (ConsumerToken.email == auth.email)
        )
        .first()
        is not None
    )


def get_consumer_token_detail(token: str):
    with get_db() as db:
        return db.query(ConsumerToken).filter(ConsumerToken.jwt_token == token).first()


def get_consumer_token(consumer_id: int, jwt_token: str):
    with get_db() as db:
        db.query(ConsumerToken).filter(
            ConsumerToken.consumer_id == consumer_id,
            ConsumerToken.jwt_token == jwt_token,
        ).one()
