from src import *

# StudentDashboardHome dummy usage
print("== Create a StudentDashboardHome instance with a dummy student and DAO ==\n")
dao = DAOImplJson("data")
student = Student("marion.dupont", "Marion", "Dupont")
student_dashboard_home = StudentDashboardHome(student, dao)
print(student_dashboard_home)

# Dummy call to get_project_dashboard_by_id (should fail gracefully if not implemented yet)
print("== Try to get project dashboard by ID ==\n")
try:
    project_dashboard = student_dashboard_home.get_project_dashboard_by_id(1)  # Using dummy project ID 1
    print(project_dashboard)
except Exception as e:
    print(f"Error: {e}")