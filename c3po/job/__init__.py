"""Create job blueprint"""
from flask import Blueprint

from .scheduler import sched

job_bp = Blueprint("job", __name__)
