from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import Project, Task
from . import db, api

# ----------------------------
# Parsers
# ----------------------------
# Parser cho Project
project_parser = reqparse.RequestParser()
project_parser.add_argument('name', type=str, required=True, help='Name is required')
project_parser.add_argument('description', type=str, required=True, help='Description is required')

# Parser cho Task
task_parser = reqparse.RequestParser()
task_parser.add_argument('name', type=str, required=True, help='Task name is required')
task_parser.add_argument('description', type=str)
task_parser.add_argument('deadline', type=str)
task_parser.add_argument('status', type=str, choices=('Not Started', 'In Progress', 'Completed'), default='Not Started')

# ----------------------------
# Project API
# ----------------------------
class ProjectAPI(Resource):
    @jwt_required()
    def get(self, project_id=None):
        if project_id:
            project = Project.query.get_or_404(project_id)
            return {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "start_date": str(project.start_date),
                "end_date": str(project.end_date),
                "status": project.status
            }
        projects = Project.query.all()
        return [{"id": project.id, "name": project.name, "description": project.description} for project in projects]

    @jwt_required()
    def post(self):
        current_user = get_jwt_identity()
        if current_user['role'] != 'Admin':  # Chỉ Admin được tạo dự án
            return {"message": "Admins only!"}, 403

        args = project_parser.parse_args()
        project = Project(name=args['name'], description=args['description'])
        db.session.add(project)
        db.session.commit()
        return {"message": "Project created successfully", "id": project.id}, 201

    @jwt_required()
    def put(self, project_id):
        args = project_parser.parse_args()
        project = Project.query.get_or_404(project_id)
        project.name = args['name']
        project.description = args['description']
        db.session.commit()
        return {"message": "Project updated successfully"}

    @jwt_required()
    def delete(self, project_id):
        project = Project.query.get_or_404(project_id)
        db.session.delete(project)
        db.session.commit()
        return {"message": "Project deleted successfully"}

# ----------------------------
# Task API
# ----------------------------
class TaskAPI(Resource):
    @jwt_required()
    def get(self, project_id=None, task_id=None):
        if task_id:
            task = Task.query.get_or_404(task_id)
            return {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "deadline": str(task.deadline),
                "status": task.status,
                "project_id": task.project_id
            }
        tasks = Task.query.filter_by(project_id=project_id).all()
        return [{"id": task.id, "name": task.name, "status": task.status} for task in tasks]

    @jwt_required()
    def post(self, project_id):
        current_user = get_jwt_identity()
        if current_user['role'] != 'Admin':
            return {"message": "Admins only!"}, 403

        args = task_parser.parse_args()
        task = Task(
            name=args['name'],
            description=args.get('description'),
            deadline=args.get('deadline'),
            status=args['status'],
            project_id=project_id
        )
        db.session.add(task)
        db.session.commit()
        return {"message": "Task created successfully", "id": task.id}, 201

    @jwt_required()
    def put(self, task_id):
        args = task_parser.parse_args()
        task = Task.query.get_or_404(task_id)
        task.name = args['name']
        task.description = args.get('description')
        task.deadline = args.get('deadline')
        task.status = args['status']
        db.session.commit()
        return {"message": "Task updated successfully"}

    @jwt_required()
    def delete(self, task_id):
        task = Task.query.get_or_404(task_id)
        db.session.delete(task)
        db.session.commit()
        return {"message": "Task deleted successfully"}

# ----------------------------
# Register API endpoints
# ----------------------------
api.add_resource(ProjectAPI, '/api/projects', '/api/projects/<int:project_id>')
api.add_resource(TaskAPI, '/api/projects/<int:project_id>/tasks', '/api/tasks/<int:task_id>')
