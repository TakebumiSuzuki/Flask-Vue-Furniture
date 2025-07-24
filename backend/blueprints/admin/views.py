from flask import Blueprint

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.post('')
def get_userlist():
    pass