from src import *
from datetime import datetime

# TeacherDashboardHome usages:

# Create a TeacherDashboardHome instance for a teacher with a DAO implementation
print("== Create a TeacherDashboardHome instance for a teacher with a DAO implementation ==\n")
dao = DAOImplJson("data")  # DAO implementation using JSON file
teacher = Teacher("anthony.query", "Anthony", "Query")  # (dummy teach until we do connection_manager.login)
teacher_dashboard_home = TeacherDashboardHome(teacher, dao)  # Logged in. Homepage
print(teacher_dashboard_home)  # Print teacher dashboard with projects
# Create a new project
print("== Create a new project ==\n")
teacher_dashboard_home.new_project(name="Mega Pattern", num_points=50)  # When writing a new project name and hitting create project button
print(teacher_dashboard_home)  # Print teacher dashboard with a new project for anthony.query named "Design Pattern"
# Access a specific project
project_id = teacher_dashboard_home.projects[-1].id  # Most recently created project

# TeacherDashboardProject usages:

# Get the project dashboard for the specific project by ID
print("== Get the project dashboard for the specific project by ID ==\n")
teacher_dashboard_project = teacher_dashboard_home.get_project_dashboard_by_id(project_id)  
print(teacher_dashboard_project)
# Set the number of votes for the project
print("== Set the number of votes for the project ==\n")
teacher_dashboard_project.set_project_num_points(10)  # Set number of votes to 10
print(teacher_dashboard_project)  # Print updated project dashboard with new number of votes
# Add students to the project
print("== Add students to the project ==\n")
operation_result = teacher_dashboard_project.add_student("marion.dupont")  # Attempt to add a student
print(operation_result)  # Print the result of the operation (success or failure message)
operation_result = teacher_dashboard_project.add_student("pierre.martin")  # Attempt to add a student
print(operation_result)  # Print the result of the operation (success or failure message)
# Add a student that does not exist
operation_result = teacher_dashboard_project.add_student("nonexistent.student")  # Attempt to add a non-existent student
print(operation_result)  # Print the result of the operation (should indicate failure)
# Add a student that is already in the project
operation_result = teacher_dashboard_project.add_student("marion.dupont")  # Attempt to add an already existing student
print(operation_result)  # Print the result of the operation (should indicate failure)
# Print the final state of the project dashboard
print(teacher_dashboard_project)  # Print final state of the project dashboard with all students added
# Set the vote close time for the project
print("== Set the vote close time for the project ==\n")
close_time = datetime(2025, 5, 29, 23, 59, 59)  # Set a close time for the votes
operation_result = teacher_dashboard_project.set_vote_close_time(close_time)  # Set the vote close time
print(operation_result)  # Print the result of setting the vote close time
# print the final state of the project dashboard after setting the vote close time
print(teacher_dashboard_project)  # Print final state of the project dashboard with vote close time set
# Set the vote close time before current date
print("== Set the vote close time before current date for the project ==\n")
close_time = datetime(2024, 5, 29, 23, 59, 59)  # Set a close time for the votes
operation_result = teacher_dashboard_project.set_vote_close_time(close_time)  # Set the vote close time
print(operation_result)  # Print the result of setting the vote close time
# print the final state of the project dashboard after setting the vote close time
print(teacher_dashboard_project)  # Print final state of the project dashboard with vote close time set
# Close votes manually for the project
print("== Close votes manually for the project ==\n")
operation_result = teacher_dashboard_project.close_votes_manually()  # Close votes manually
print(operation_result)  # Print the result of closing votes manually
# Print the final state of the project dashboard after closing votes
print(teacher_dashboard_project)  # Print final state of the project dashboard after closing votes

# Test get_student_forms_by_project from DAO using project id 1
print("== Test get_student_forms_by_project from DAO using project id 1 ==\n")
project_id = 1  # Assuming project ID 1 exists
result = dao.get_student_forms_by_project(project_id)
if result.success:
    print(f"Student forms for project ID {project_id}:")
    for form in result.data:
        print(form)