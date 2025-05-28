import tkinter as tk
from tkinter import ttk, messagebox

class StudentDashboardProjectView(tk.Toplevel):
    def __init__(self, root, project_dashboard):
        super().__init__(root)
        self.title("Student Project View")
        self.geometry("500x500")
        self.project_dashboard = project_dashboard
        self._build_interface()

    def _build_interface(self):
        tk.Label(self, text=f"Project: {self.project_dashboard.project.name}", font=("Arial", 14)).pack(pady=10)
        self.points_var = tk.StringVar(value=f"Points remaining: {self.project_dashboard.points}")
        tk.Label(self, textvariable=self.points_var).pack(pady=5)

        # Dropdown to choose recipient
        self.recipient_var = tk.StringVar()
        student_usernames = [
            s.username for s in self.project_dashboard.project.students
            if s.username != self.project_dashboard.student.username
        ]
        self.recipient_menu = ttk.Combobox(self, textvariable=self.recipient_var, values=student_usernames, state="readonly")
        self.recipient_menu.pack(pady=5)

        # Entry for points
        self.points_entry = ttk.Entry(self)
        self.points_entry.pack(pady=5)
        self.points_entry.insert(0, "1")

        # Submit button
        submit_btn = ttk.Button(self, text="Give Points", command=self._give_points)
        submit_btn.pack(pady=5)

        # List of current votes
        self.votes_listbox = tk.Listbox(self)
        self.votes_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self._refresh_votes()

    def _give_points(self):
        username = self.recipient_var.get()
        if not username:
            messagebox.showwarning("Missing Selection", "Please choose a student.")
            return

        try:
            points = int(self.points_entry.get())
        except ValueError:
            messagebox.showerror("Invalid Input", "Points must be a number.")
            return

        recipient = next((s for s in self.project_dashboard.project.students if s.username == username), None)
        if not recipient:
            messagebox.showerror("Error", "Selected student not found.")
            return

        result = self.project_dashboard.attribute_points_to_student(recipient, points)
        messagebox.showinfo("Result", result)
        self._refresh_votes()

    def _refresh_votes(self):
        self.votes_listbox.delete(0, tk.END)
        for recipient, pts in self.project_dashboard.student_form.votes:
            self.votes_listbox.insert(tk.END, f"{recipient.name} - {pts} pts")
        self.points_var.set(f"Points remaining: {self.project_dashboard.points}")
