import tkinter as tk
from tkinter import ttk, messagebox
from .StudentDashboardProjectView import StudentDashboardProjectView

class StudentDashboardHomeView(tk.Toplevel):
    def __init__(self, root, student_dashboard):
        super().__init__(root)
        self.title("Student Dashboard")
        self.geometry("500x400")
        self.student_dashboard = student_dashboard
        self._build_interface()

    def _build_interface(self):
        tk.Label(self, text=f"Hello {self.student_dashboard.student.name}", font=("Arial", 14)).pack(pady=10)

        self.project_listbox = tk.Listbox(self)
        self.project_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        for project in self.student_dashboard.projects:
            self.project_listbox.insert(tk.END, f"{project.id}: {project.name}")

        view_btn = ttk.Button(self, text="View Project", command=self._view_project)
        view_btn.pack(pady=5)

    def _view_project(self):
        selected_index = self.project_listbox.curselection()
        if not selected_index:
            messagebox.showwarning("No selection", "Please select a project to view.")
            return

        selected_text = self.project_listbox.get(selected_index)
        project_id = int(selected_text.split(":")[0])

        try:
            project_controller = self.student_dashboard.get_project_dashboard_by_id(project_id)
            StudentDashboardProjectView(self, project_controller)
        except ValueError as e:
            messagebox.showerror("Error", str(e))
