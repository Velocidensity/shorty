from __future__ import annotations

from sqlalchemy.sql import func

from shorty._app import db
from shorty.helpers import generate_stem


class URL(db.Model):
    """Database table to store shortened URLs"""
    stem = db.Column(db.String(5), index=True, primary_key=True)
    url = db.Column(db.String(2048), index=True)
    user_ip = db.Column(db.String(48))
    hits = db.Column(db.Integer, default=0)
    added_time = db.Column(db.DateTime(timezone=False), server_default=func.now())

    @classmethod
    def get(cls, stem: str) -> URL | None:
        """
        Returns saved URL for a given stem

        Args:
            stem: Shortened URL stem

        Returns:
            URL if found
        """
        mapping = cls.query.filter_by(stem=stem).first()
        return mapping

    @classmethod
    def find(cls, url: str) -> URL | None:
        """
        Finds a stem for a given URL, if one exists

        Args:
            url: Full URL

        Returns:
            URL if found, None otherwise
        """
        mapping = cls.query.filter_by(url=url).first()
        return mapping

    @classmethod
    def add(cls, url: str, user_ip: str, force: bool = False) -> URL:
        """
        Adds a stem -> URL mapping

        Args:
            url: Full URL
            user_ip: Creating user's IP address
            force: Add a new mapping even if one exists for the given URL

        Returns:
            Added or existing mapping for a given URL
        """
        if force or not (mapping := cls.find(url)):
            mapping = URL(
                stem=generate_stem(),
                url=url,
                user_ip=user_ip,
            )
            db.session.add(mapping)
            db.session.commit()

        return mapping

    @classmethod
    def hit(cls, stem: str) -> bool:
        """Adds an extra hit to the counter for a given URL

        Args:
            stem: Shortened URL stem

        Returns:
            Operation success status
        """
        mapping = cls.query.filter_by(stem=stem).first()
        if mapping:
            mapping.hits = (mapping.hits or 0) + 1
            db.session.commit()
            return True
        return False

    def __repr__(self):
        return '<URL {}>'.format(self.stem)
