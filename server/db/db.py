import os

from flask_jsontools.formatting import JsonSerializableBase
from flask_migrate import command
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData()
Base = declarative_base(cls=(JsonSerializableBase,), metadata=metadata)


class SQLAlchemyPrePing(SQLAlchemy):
    def apply_pool_defaults(self, app, options):
        options["pool_pre_ping"] = True
        options["echo"] = app.config["SQLALCHEMY_ECHO"]
        super().apply_pool_defaults(app, options)


db = SQLAlchemyPrePing()


def db_migrations(sqlalchemy_database_uri):
    migrations_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../migrations/")
    from alembic.config import Config
    config = Config(migrations_dir + "alembic.ini")
    config.set_main_option("sqlalchemy.url", sqlalchemy_database_uri)
    config.set_main_option("script_location", migrations_dir)
    command.upgrade(config, "head")


class User(Base, db.Model):
    __tablename__ = "users"
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    cuid = db.Column("cuid", db.String(length=255), nullable=False)
    attributes = db.Column("attributes", db.JSON(), nullable=False)
    is_complete = db.Column("is_complete", db.Boolean(), nullable=True, default=False)
    is_disabled = db.Column("is_disabled", db.Boolean(), nullable=True, default=False)
    is_deleted = db.Column("is_deleted", db.Boolean(), nullable=True, default=False)
    remote_accounts = db.relationship("RemoteAccount", back_populates="user",
                                      cascade="all, delete-orphan",
                                      passive_deletes=True)
    aups = db.relationship("Aup", back_populates="user",
                           cascade="all, delete-orphan",
                           passive_deletes=True)
    created_at = db.Column("created_at", db.DateTime(timezone=True), server_default=db.text("CURRENT_TIMESTAMP"),
                           nullable=False)

    @classmethod
    def find_by_iuid_values(cls, iuid_values):
        return User.query\
            .join(User.remote_accounts)\
            .join(RemoteAccount.iuids)\
            .filter(Iuid.iuid.in_(iuid_values))\
            .all()


class RemoteAccount(Base, db.Model):
    __tablename__ = "remote_accounts"
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    source_entity_id = db.Column("source_entity_id", db.String(length=255), nullable=False)
    source_display_name = db.Column("source_display_name", db.String(length=255), nullable=True)
    attributes = db.Column("attributes", db.JSON(), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="remote_accounts")
    iuids = db.relationship("Iuid", back_populates="remote_account",
                            cascade="all, delete-orphan",
                            passive_deletes=True)
    created_at = db.Column("created_at", db.DateTime(timezone=True), server_default=db.text("CURRENT_TIMESTAMP"),
                           nullable=False)


class EmailVerification(Base, db.Model):
    __tablename__ = "email_verifications"
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    code = db.Column("code", db.String(length=12), nullable=False)
    email = db.Column("email", db.String(length=255), nullable=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User")
    created_at = db.Column("created_at", db.DateTime(timezone=True), server_default=db.text("CURRENT_TIMESTAMP"),
                           nullable=False)
    expires_at = db.Column("expires_at", db.DateTime(timezone=True))


class Aup(Base, db.Model):
    __tablename__ = "aups"
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    au_version = db.Column("au_version", db.String(length=255), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey("users.id"))
    user = db.relationship("User", back_populates="aups")
    agreed_at = db.Column("agreed_at", db.DateTime(timezone=True), server_default=db.text("CURRENT_TIMESTAMP"),
                          nullable=False)


class Iuid(Base, db.Model):
    __tablename__ = "iuids"
    id = db.Column("id", db.Integer(), primary_key=True, nullable=False, autoincrement=True)
    iuid = db.Column("iuid", db.String(length=255), nullable=False)
    remote_account_id = db.Column(db.Integer(), db.ForeignKey("remote_accounts.id"))
    remote_account = db.relationship("RemoteAccount", back_populates="iuids")
