from src import *

dao = DAOImplJson("data")  # DAO implementation using JSON file
teacher = Teacher("anthony.query", "Anthony", "Query")  # (dummy teach until we do connection_manager.login)
students = dao.get_students_by_project(2).data
teacher_dashboard_project = TeacherDashboardProject(teacher, dao, Project(id=2, name="Mega Pattern", num_points=10, students=students))
teacher_dashboard_project.cluster_students(2)