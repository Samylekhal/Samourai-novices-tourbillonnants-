import tkinter as tk
from tkinter import ttk, messagebox

class TeacherDashboardHomeView(tk.Toplevel):
    def __init__(self, root, teacher_dashboard):
        super().__init__(root)
        self.title("Teacher Dashboard")
        self.geometry("500x400")
        self.teacher_dashboard = teacher_dashboard
        self._build_interface()

    def _build_interface(self):
        tk.Label(self, text=f"Welcome {self.teacher_dashboard.teacher}", font=("Arial", 14)).pack(pady=10)

        self.project_listbox = tk.Listbox(self)
        self.project_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        for project in self.teacher_dashboard.projects:
            self.project_listbox.insert(tk.END, f"{project.id}: {project.name}")

        add_btn = ttk.Button(self, text="New Project", command=self._create_project)
        add_btn.pack(pady=5)
        view_btn = ttk.Button(self, text="View Project", command=self._view_project)
        view_btn.pack(pady=5)

    def _create_project(self):
        def submit():
            name = name_entry.get()
            try:
                points = int(points_entry.get())
            except ValueError:
                messagebox.showerror("Invalid Input", "Points must be a number.")
                return
            if not name:
                messagebox.showerror("Invalid Input", "Project name is required.")
                return
            dialog.destroy()
            new_project = self.teacher_dashboard.new_project(name, points)
            self.project_listbox.insert(tk.END, f"{new_project.id}: {new_project.name}")

        dialog = tk.Toplevel(self)
        dialog.title("New Project")
        tk.Label(dialog, text="Project Name:").pack()
        name_entry = ttk.Entry(dialog)
        name_entry.pack()

        tk.Label(dialog, text="Number of Points:").pack()
        points_entry = ttk.Entry(dialog)
        points_entry.insert(0, "100")
        points_entry.pack()

        ttk.Button(dialog, text="Create", command=submit).pack(pady=10)


    def _view_project(self):
        selection = self.project_listbox.curselection()
        if not selection:
            messagebox.showwarning("No selection", "Please select a project.")
            return

        selected_text = self.project_listbox.get(selection)
        project_id = int(selected_text.split(":")[0])

        try:
            project_controller = self.teacher_dashboard.get_project_dashboard_by_id(project_id)
            from .TeacherDashboardProjectView import TeacherDashboardProjectView
            TeacherDashboardProjectView(self, project_controller)
        except ValueError as e:
            messagebox.showerror("Error", str(e))


