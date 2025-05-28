import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class TeacherDashboardProjectView(tk.Toplevel):
    def __init__(self, root, project_dashboard):
        super().__init__(root)
        self.title("Teacher Project View")
        self.geometry("600x500")
        self.project_dashboard = project_dashboard
        self._build_interface()

    def _build_interface(self):
        tk.Label(self, text=f"Project: {self.project_dashboard.project.name}", font=("Arial", 14)).pack(pady=10)
        # Voting status label
        self.voting_status_var = tk.StringVar()
        self.voting_status_label = tk.Label(self, textvariable=self.voting_status_var, font=("Arial", 10, "italic"))
        self.voting_status_label.pack(pady=(0, 10))

        self._update_voting_status()

        # Students list
        self.students_listbox = tk.Listbox(self)
        self.students_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=5)
        self.refresh_student_list()

        # Add student entry
        frame = tk.Frame(self)
        frame.pack(pady=5)
        tk.Label(frame, text="Add student (username):").pack(side=tk.LEFT)
        self.add_entry = ttk.Entry(frame)
        self.add_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame, text="Add", command=self._add_student).pack(side=tk.LEFT)

        # Remove selected student
        ttk.Button(self, text="Remove Selected", command=self._remove_student).pack(pady=5)

        # Reopen voting button
        ttk.Button(self, text="Reopen Voting", command=self._reopen_votes).pack(pady=5)

        # Set number of points
        frame2 = tk.Frame(self)
        frame2.pack(pady=10)
        tk.Label(frame2, text="Set points per student:").pack(side=tk.LEFT)
        self.points_entry = ttk.Entry(frame2)
        self.points_entry.insert(0, str(self.project_dashboard.project.num_points))
        self.points_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(frame2, text="Set", command=self._set_points).pack(side=tk.LEFT)

        # Close votes manually
        ttk.Button(self, text="Close Votes Now", command=self._close_votes).pack(pady=10)

        # Cluster students
        cluster_frame = tk.Frame(self)
        cluster_frame.pack(pady=10)
        tk.Label(cluster_frame, text="Number of groups (k):").pack(side=tk.LEFT)
        self.k_entry = ttk.Entry(cluster_frame)
        self.k_entry.insert(0, "2")
        self.k_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(cluster_frame, text="Cluster Students", command=self._cluster_students).pack(side=tk.LEFT)

        # --- Vote close time setting ---
        vote_frame = tk.Frame(self)
        vote_frame.pack(pady=10)

        tk.Label(vote_frame, text="Set vote close time (YYYY-MM-DD HH:MM):").pack(side=tk.LEFT)
        self.vote_time_entry = ttk.Entry(vote_frame, width=20)
        self.vote_time_entry.pack(side=tk.LEFT, padx=5)
        ttk.Button(vote_frame, text="Schedule", command=self._set_vote_close_time).pack(side=tk.LEFT)

        # Autofill vote close time if it's defined
        if self.project_dashboard.project.vote_close_time:
            formatted = self.project_dashboard.project.vote_close_time.strftime("%Y-%m-%d %H:%M")
            self.vote_time_entry.insert(0, formatted)

    def refresh_student_list(self):
        self.students_listbox.delete(0, tk.END)
        for s in self.project_dashboard.project.students:
            self.students_listbox.insert(tk.END, f"{s.username} - {s.name} {s.surname}")

    def _add_student(self):
        username = self.add_entry.get()
        if not username:
            messagebox.showwarning("Missing", "Please enter a username.")
            return
        result = self.project_dashboard.add_student(username)
        messagebox.showinfo("Add Student", result.message)
        if result.success:
            self.refresh_student_list()

    def _remove_student(self):
        selected = self.students_listbox.curselection()
        if not selected:
            messagebox.showwarning("Missing", "Select a student to remove.")
            return
        line = self.students_listbox.get(selected[0])
        username = line.split(" - ")[0]
        print("Calling controller with username:", username)
        result = self.project_dashboard.remove_student(username)
        messagebox.showinfo("Remove Student", result.message)
        if result.success:
            self.refresh_student_list()

    def _set_points(self):
        try:
            pts = int(self.points_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid number.")
            return
        self.project_dashboard.set_project_num_points(pts)
        messagebox.showinfo("Points Set", "Points per student updated.")

    def _close_votes(self):
        result = self.project_dashboard.close_votes_manually()
        messagebox.showinfo("Close Votes", result.message)
        if result.success:
            self._update_voting_status()

    def _cluster_students(self):
        try:
            k = int(self.k_entry.get())
        except ValueError:
            messagebox.showerror("Invalid", "Enter a valid group count.")
            return
        result = self.project_dashboard.cluster_students(k)
        messagebox.showinfo("Cluster Students", result.message)

    def _set_vote_close_time(self):
        text = self.vote_time_entry.get()
        try:
            close_time = datetime.strptime(text, "%Y-%m-%d %H:%M")
        except ValueError:
            messagebox.showerror("Invalid Format", "Use format YYYY-MM-DD HH:MM")
            return

        result = self.project_dashboard.set_vote_close_time(close_time)
        messagebox.showinfo("Set Close Time", result.message)

    def _reopen_votes(self):
        result = self.project_dashboard.reopen_votes()
        messagebox.showinfo("Reopen Voting", result.message)
        if result.success:
            self._update_voting_status()

    def _update_voting_status(self):
        # Clear old buttons if they exist
        if hasattr(self, 'close_button'):
            self.close_button.destroy()
        if hasattr(self, 'reopen_button'):
            self.reopen_button.destroy()

        if self.project_dashboard.project.closed_vote:
            self.voting_status_var.set("🔒 Voting is CLOSED")
            self.reopen_button = ttk.Button(self, text="Reopen Voting", command=self._reopen_votes)
            self.reopen_button.pack(pady=5)
        else:
            self.voting_status_var.set("🟢 Voting is OPEN")
            self.close_button = ttk.Button(self, text="Close Votes Now", command=self._close_votes)
            self.close_button.pack(pady=5)
