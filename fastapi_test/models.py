import random
import string
from sqlalchemy import Column, String, TIMESTAMP, func
from database import Base


class Link(Base):
    __tablename__ = 'links'
    short_link_length = 6
    letters = string.ascii_letters + string.digits
    short_link = Column(
        String(short_link_length),
        nullable=False, primary_key=True)
    full_link = Column(String(500), nullable=False)
    created = Column(
        TIMESTAMP, server_default=func.current_timestamp(),
        nullable=False)

    def __init__(self, full_link):
        self.full_link = full_link
        self.short_link = self.generate_short_link(full_link)

    def generate_short_link(self, link) -> str:
        return ''.join(random.choice(self.letters)
                       for _ in range(self.short_link_length))
