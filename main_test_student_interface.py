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
    project_dashboard = student_dashboard_home.get_project_dashboard_by_id(5)  # Using dummy project ID 1
    print(project_dashboard)
except Exception as e:
    print(f"Error: {e}")

# StudentDashboardProject dummy usage
print("== Attribute points to another student ==\n")
try:
    # Get project dashboard
    project_dashboard = student_dashboard_home.get_project_dashboard_by_id(5)

    # Get recipient student from DAO
    recipient_result = dao.get_student_by_username("pierre.martin")
    if not recipient_result.success:
        print(f"Could not load recipient: {recipient_result.message}")
    else:
        recipient = recipient_result.data
        # Attribute points
        result_message = project_dashboard.attribute_points_to_student(recipient, 25)
        print(result_message)
        print(f"Remaining points for {student.username}: {project_dashboard.points}")
except Exception as e:
    print(f"Error during point attribution: {e}")
