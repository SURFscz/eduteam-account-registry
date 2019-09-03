# -*- coding: future_fstrings -*-
"""Initial database

Revision ID: a6d9a5b30e14
Revises:
Create Date: 2019-01-07 10:28:20.335581

"""

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = 'a6d9a5b30e14'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("users",
                    sa.Column("id", sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
                    sa.Column("cuid", sa.String(length=255), nullable=False),
                    sa.Column("attributes", sa.JSON(), nullable=True),
                    sa.Column("is_complete", sa.Boolean(), nullable=True),
                    sa.Column("is_disabled", sa.Boolean(), nullable=True),
                    sa.Column("is_deleted", sa.Boolean(), nullable=True),
                    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"),
                              nullable=False),
                    sa.Column("modified_at", sa.DateTime(timezone=True),
                              server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                              nullable=False)
                    )

    op.create_table("remote_accounts",
                    sa.Column("id", sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
                    sa.Column("source_entity_id", sa.String(length=255), nullable=False),
                    sa.Column("source_display_name", sa.String(length=255), nullable=False),
                    sa.Column("attributes", sa.JSON(), nullable=True),
                    sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="cascade"),
                              nullable=False),
                    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"),
                              nullable=False),
                    sa.Column("updated_at", sa.DateTime(timezone=True),
                              server_default=sa.text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
                              nullable=False)
                    )

    op.create_table("email_verifications",
                    sa.Column("id", sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
                    sa.Column("code", sa.String(length=12), nullable=False),
                    sa.Column("email", sa.String(length=255), nullable=False),
                    sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="cascade"), nullable=False),
                    sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"),
                              nullable=False),
                    sa.Column("expires_at", sa.DateTime(timezone=True),
                              nullable=False)
                    )

    op.create_table("aups",
                    sa.Column("id", sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
                    sa.Column("au_version", sa.String(length=36), nullable=False),
                    sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="cascade"), nullable=False),
                    sa.Column("agreed_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"),
                              nullable=False)
                    )

    op.create_table("iuids",
                    sa.Column("id", sa.Integer(), primary_key=True, nullable=False, autoincrement=True),
                    sa.Column("iuid", sa.String(length=255), nullable=False),
                    sa.Column("remote_account_id", sa.Integer(), sa.ForeignKey("remote_accounts.id", ondelete="cascade"), nullable=False),
                    sa.Column("agreed_at", sa.DateTime(timezone=True), server_default=sa.text("CURRENT_TIMESTAMP"),
                              nullable=False)
                    )


def downgrade():
    pass
