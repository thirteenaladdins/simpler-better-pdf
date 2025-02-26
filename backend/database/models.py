# models.py
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Document(Base):
    __tablename__ = "documents"
    # Filename (S3 key)
    filename = Column(String)
    # MIME type (e.g., application/pdf)
    filetype = Column(String)
    # Generated presigned URL
    presigned_url = Column(String)
    # URL expiration time

    id = Column(String, primary_key=True, index=True)          # Document UUID
    # S3 object key (e.g., uuid.pdf)

    s3_key = Column(String, unique=True, index=True)

    expires_at = Column(DateTime)
