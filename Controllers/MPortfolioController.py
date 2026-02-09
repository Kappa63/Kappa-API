from werkzeug.datastructures import FileStorage
from datetime import datetime, timezone
from .DBController import getSession
from Config import MPortfolioConfig
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
        posts = session.query(Post).order_by(Post.order).all()
        return [{
                    "id": post.id,
                    "imageURL": post.imageURL,
                    "title": post.title,
                    "description": post.description,
                    "category": post.category,
                    "order": post.order,
                    "active": post.active,
                    "createdOn": post.createdOn,
                    "updatedOn": post.updatedOn
                } for post in posts], 200
    
def _updatePost(pid: int, iURL: str = None, ttl: str = None,  desc: str = None,  cat: str = None, ordr: int = None) -> tuple[dict, int]:
    """
    Updates a post
    """
    with getSession() as session:
        if not (post := session.query(Post).filter_by(id=pid).first()):
            return {"error": "Post not found"}, 404
            
        if iURL: post.imageURL = iURL
        if ttl: post.title = ttl
        if desc: post.description = desc
        if cat: post.category = cat
        if ordr is not None: post.order = ordr
        
        post.updatedOn = datetime.now(timezone.utc)
        return {"id": post.id}, 200

def _deletePost(pid: int) -> tuple[dict, int]:
    """
    Deletes a post
    """
    with getSession() as session:
        if not (post := session.query(Post).filter_by(id=pid).first()):
            return {"error": "Post not found"}, 404
        
        session.delete(post)
        return {"message": "Post deleted"}, 200

def _reorderPosts(order_map: dict) -> tuple[dict, int]:
    """
    Updates the order of multiple posts
    order_map: {post_id: new_order}
    """
    with getSession() as session:
        for pid, new_order in order_map.items():
            if (post := session.query(Post).filter_by(id=pid).first()):
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
        newPost = Post(imageURL=imageURL, title=title, description=description, category=category, order=max_order+1)
        session.add(newPost)
        session.flush()
        return {"id": newPost.id, "imageURL": newPost.imageURL, 
                "title": newPost.title, "description": newPost.description,
                "category": newPost.category, "order": newPost.order, "active": newPost.active}, 201
