from werkzeug.datastructures import FileStorage
from datetime import datetime, timezone
from .DBController import getSession
from Config import MPortfolioConfig
from Models import Post
import uuid
import os

def _uploadImage(img:FileStorage) -> tuple[bool, int]:
    """
    Uploads an Image to the servers UPLOADS_FOLDER

    Parameters:
        ``img`` (``filestorage``):
            image
    Returns:
        ``tuple``:
            Containing:
            - dict keys: `filename`
            - int: HTTP status code
    """
    fn = os.path.join(MPortfolioConfig.PORTFOLIO_UPLOADS_FOLDER, f"{uuid.uuid4()}.jpg")
    img.save(fn)
    return {"filename":fn}, 201

def _listPosts() -> tuple[dict, int]:
    """
    Lists all posts

    Returns:
        ``tuple``:
            Containing:
            - list[dict] keys: `id`, `imageURL`, `title`, `description`, `category`, `state` `createdOn`, `updatedOn`
            - int: HTTP status code
    """
    with getSession() as session:
        posts = session.query(Post).all()
        return [{
                    "id": post.id,
                    "imageURL": post.imageURL,
                    "title": post.title,
                    "description": post.description,
                    "category": post.category,
                    "state": post.state,
                    "createdOn": post.createdOn,
                    "updatedOn": post.updatedOn
                } for post in posts], 200
    
def _createPost(iURL: str, ttl: str,  desc: str,  cat: str) -> tuple[dict, int]:
    """
    Creates a new user

    Parameters:
        ``iURL`` (``str``):
            Image url
        ``ttl`` (``str``):
            Post title
        ``desc`` (``str``):
            description
        ``cat`` (``str``):
            category
    Returns:
        ``tuple``:
            Containing:
            - dict keys: `id`, `imageURL`, `title`, `description`, `category`, `state`
            - int: HTTP status code
    """
    with getSession() as session:
        newPost = Post(imageURL=iURL, title=ttl, description=desc, category=cat)
        session.add(newPost)
        session.flush()
        return {"id": newPost.id, "imageURL": newPost.imageURL, 
                "title": newPost.title, "description": newPost.description,
                "category": newPost.category, "state": newPost.state}, 201