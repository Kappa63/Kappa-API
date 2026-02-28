from werkzeug.datastructures import FileStorage
from datetime import datetime, timezone
from .DBController import getSession
from Utils.Helpers.DBHelpers import listFromDB, updateInDB, createInDB
from Config import KPortfolioConfig
from Models import Experience, Skill, Project
import uuid
import os
import sqlalchemy as sa
from datetime import date

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

def _listExperiences() -> tuple[list[dict], int]:
    """
    Lists all experiences
    """
    experiences = listFromDB(Experience)
    experiences.sort(key=lambda x: x["startDate"], reverse=True)
    return experiences
    
def _updateExperience(pid: int, updates: dict) -> tuple[dict, int]:
    """
    Updates an experience
    """
    return updateInDB(Experience, pid, updates, "Experience not found")

def _createExperience(role: str, company: str,  startDate: date, highlights: str, endDate: date = None) -> tuple[dict, int]:
    """
    Creates a new experience
    """
    
    return createInDB(Experience(
        role=role,
        company=company,
        startDate=startDate,
        endDate=endDate,
        highlights=highlights,
        # order=order
    )), 201

def _listSkills() -> tuple[list[dict], int]:
    """
    Lists all skills
    """
    skills = listFromDB(Skill)
    skills.sort(key=lambda x: x["order"])
    return skills
    
def _updateSkill(pid: int, updates: dict) -> tuple[dict, int]:
    """
    Updates a skill
    """
    return updateInDB(Skill, pid, updates, "Experience not found")

def _createSkill(category: str, name: str, order: int, icon: str = None) -> tuple[dict, int]:
    """
    Creates a new skill
    """
    return createInDB(Skill(
        category=category,
        name=name,
        icon=icon,
        order=order
    )), 201

def _listProjects() -> tuple[list[dict], int]:
    """
    Lists all projects
    """
    projects = listFromDB(Project)
    projects.sort(key=lambda x: x["order"])
    return projects
    
def _updateProject(pid: int, updates: dict) -> tuple[dict, int]:
    """
    Updates a project
    """
    return updateInDB(Project, pid, updates, "Experience not found")

def _createProject(imageURL: str, title: str,  description: str, order: int, link: str = None) -> tuple[dict, int]:
    """
    Creates a new project
    """
    return createInDB(Project(
        imageURL=imageURL,
        title=title,
        description=description,
        link=link,
        order=order
    )), 201
