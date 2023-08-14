from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

"""
    Import các class cần cho việc tạo bảng. Import class nào thì tạo bảng đó
"""

from .models.Post import Post
