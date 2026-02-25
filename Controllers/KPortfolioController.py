from werkzeug.datastructures import FileStorage
from datetime import datetime, timezone
from .DBController import getSession
from Utils.Helpers.DBHelpers import listFromDB, updateInDB, softDeleteFromDB, createInDB
from Config import KPortfolioConfig
from Models import Post, General
import uuid
import os
import sqlalchemy as sa

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
    fn = os.path.join(KPortfolioConfig.PORTFOLIO_UPLOADS_FOLDER, f"{uuid.uuid4()}.jpg")
    img.save(fn)
    return {"filename":fn}, 201

def _listPosts() -> tuple[list[dict], int]:
    """
    Lists all posts

    Returns:
        ``tuple``:
            Containing:
            - list[dict] keys: `id`, `imageURL`, `title`, `description`, `category`, `state` `createdOn`, `updatedOn`
            - int: HTTP status code
    """
    return listFromDB(Post)
    
def _updatePost(pid: int, updates: dict) -> tuple[dict, int]:
    """
    Updates a post
    """
    return updateInDB(Post, pid, updates, "Post not found")

def _deletePost(pid: int) -> tuple[dict, int]:
    """
    Deletes a post
    """
    return softDeleteFromDB(Post, pid, "Post not found")

def _reorderPosts(order_map: dict) -> tuple[dict, int]:
    """
    Updates the order of multiple posts
    order_map: {post_id: new_order}
    """
    with getSession() as session:
        for pid, new_order in order_map.items():
            print(pid)
            print(new_order)
            if (post := session.query(Post).filter_by(id=int(pid)).first()):
                print(post.order)
                post.order = new_order

        return {"message": "Order updated"}, 200

def _getGeneral() -> tuple[dict, int]:
    """
    Gets text content
    """
    with getSession() as session:
        items = session.query(General).all()
        return {item.key: item.value for item in items}, 200

def _updateGeneral(data: dict) -> tuple[dict, int]:
    """
    Updates text content
    """
    with getSession() as session:
        for key, value in data.items():
            if (item := session.query(General).filter_by(key=key).first()):
                item.value = value
            else:
                session.add(General(key=key, value=value))
        return {"message": "Updated"}, 200
    
def _createPost(imageURL: str, title: str,  description: str,  category: str) -> tuple[dict, int]:
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
        # Get max order to append to end
        max_order = session.query(sa.func.max(Post.order)).scalar() or 0
    
    return createInDB(Post(
        imageURL=imageURL, 
        title=title, 
        description=description, 
        category=category, 
        order=max_order+1
    )), 201
