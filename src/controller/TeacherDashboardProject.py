# TeacherDashboardProject.py
from typing import List, Dict, Tuple
import random
from ..dao.DAO import DAO
from ..model.Teacher import Teacher
from ..model.Project import Project
from ..model.Student import Student
from ..model.StudentForm import StudentForm
from ..utils.Result import Result

from datetime import datetime

class TeacherDashboardProject:
    def __init__(self, teacher: Teacher, dao: DAO, project: Project):
        self.teacher = teacher
        self.dao = dao
        students_result = self.dao.get_students_by_project(project.id)
        if students_result.success:
            project.students = students_result.data
        else:
            project.students = []

        self.project = project

    def set_project_num_points(self, num_points: int):
        self.project.num_points = num_points
        self.dao.update_project(self.project)


    def add_student(self, student_username: str) -> Result[Student]:
        result = self.dao.get_student_by_username(student_username)
        if not result.success:
            return Result(False, result.message)

        student = result.data
        if any(s.username == student.username for s in self.project.students):
            return Result(False, f"Student '{student_username}' is already in the project.")
        
        self.project.students.append(student)
        print(f"Adding student {student} to project {self.project.name}")
        print(f"Project students after addition: {[s.username for s in self.project.students]}")
        self.dao.update_project(self.project)
        return Result(True, f"Student '{student_username}' added successfully.", data=student)

    def remove_student(self, student_username: str) -> Result[Student]:
        for student in self.project.students:
            if student.username == student_username:
                self.project.students.remove(student)
                self.dao.update_project(self.project)
                return Result(True, f"Student '{student_username}' removed successfully.", data=student)
        
        return Result(False, f"Student '{student_username}' is not in the project.")

    def close_votes_manually(self) -> Result[None]:
        if self.project.closed_vote:
            return Result(False, "Votes are already closed for this project.")
        
        self.project.closed_vote = True
        self.project.vote_close_time = None
        self.dao.update_project(self.project)
        return Result(True, f"Votes for project '{self.project.name}' have been manually closed.")

    def set_vote_close_time(self, close_time: datetime) -> Result[None]:
        if self.project.closed_vote:
            return Result(False, "Cannot set vote close time because votes are already closed.")
        
        if close_time < datetime.now():
            return Result(False, "Cannot set vote close time that comes before the current date.")

        self.project.vote_close_time = close_time
        self.dao.update_project(self.project) 
        return Result(True, f"Vote close time set to {close_time.isoformat()} for project '{self.project.name}'.")


    def reopen_votes(self) -> Result[None]:
        if not self.project.closed_vote:
            return Result(False, "Votes are already open.")
        
        self.project.closed_vote = False
        self.project.vote_close_time = None
        self.dao.update_project(self.project)
        return Result(True, f"Votes reopened for project '{self.project.name}'.")


    def cluster_students(self, k: int, total_iterations: int = 5000) -> Result[None]:
        """
        Cluster students based on their project preferences.
        This is a placeholder for the actual clustering logic.
        """

        def create_affinity_matrix(usernames: List[str], votes_par_index: Dict[str, Dict[str, int]]) -> Tuple[List[List[int]], Dict[int, str]]:
            """
            Crée la matrice d'affinité pondérée à partir des usernames.
            
            Args:
                usernames: liste ordonnée des usernames
                votes_par_index: dictionnaire {votant: {voté: points}}
            
            Returns:
                Matrice A[n][n] avec les points d'affinité pondérés.
            """
            n = len(usernames)
            name_to_index = {username: i for i, username in enumerate(usernames)}
            index_to_name = {i: username for username, i in name_to_index.items()}
            A = [[0] * n for _ in range(n)]

            for voter, voted_dict in votes_par_index.items():
                i = name_to_index.get(voter)
                if i is None:
                    continue
                for voted, points in voted_dict.items():
                    j = name_to_index.get(voted)
                    if j is not None and i != j:
                        A[i][j] = points  # Use points instead of binary vote

            print(f"Created affinity matrix of size {n}x{n} based on weighted votes.")
            print(A)
            return A, index_to_name


        def compute_group_score(group: List[int], A: List[List[int]]) -> int:
            """Calcule le score total d'affinité d'un groupe."""
            if len(group) <= 1:
                return 0
            
            score = 0
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    idx1, idx2 = group[i], group[j]
                    # On compte les affinités dans les deux sens
                    score += A[idx1][idx2] + A[idx2][idx1]
            
            return score

        def compute_individual_score(group: List[int], new_idx: int, A: List[List[int]]) -> int:
            """Calcule le score qu'apporterait l'ajout d'une personne à un groupe."""
            return sum(A[new_idx][i] + A[i][new_idx] for i in group)

        def count_satisfied_individuals(groups: List[List[int]], A: List[List[int]]) -> int:
            """Compte le nombre d'individus ayant au moins une affinité dans leur groupe."""
            satisfied = 0
            for group in groups:
                for person in group:
                    # Une personne est satisfaite si elle a une affinité (vote) avec au moins une autre personne du groupe
                    has_affinity = any(A[person][other] > 0 for other in group if other != person)
                    if has_affinity:
                        satisfied += 1
            return satisfied

        def assign_groups_with_constraints(n: int, k: int, A: List[List[int]],  min_affinity_per_person: int) -> Tuple[List[List[int]], List[int], bool]:
            """
            Assigne les étudiants aux groupes en respectant les contraintes d'affinité.
            
            Retourne:
                - groups: Liste des groupes
                - group_scores: Scores de chaque groupe
                - constraint_satisfied: True si la contrainte minimale est respectée
            """
            # Taille visée pour chaque groupe
            group_sizes = [n // k + (1 if i < n % k else 0) for i in range(k)] # Taille variable pour équilibrer les groupes
            groups = [[] for _ in range(k)] # Liste des groupes
            group_scores = [0 for _ in range(k)] # Scores initiaux des groupes
            
            # Liste des étudiants à assigner
            remaining = list(range(n))
            random.shuffle(remaining)  # Mélanger pour une distribution aléatoire initiale

            # Fonction pour vérifier si une personne a au moins une affinité dans le groupe
            def has_affinity_in_group(group: List[int], idx: int) -> bool:
                return any(A[idx][peer] > 0 or A[peer][idx] > 0 for peer in group)
            
            # Phase 1: Essayer d'assigner en respectant les contraintes d'affinité
            while remaining:
                idx = remaining.pop(0)
                candidates = []
                
                for g_id in range(k):
                    if len(groups[g_id]) < group_sizes[g_id]:
                        # Calculer le score potentiel
                        score = compute_individual_score(groups[g_id], idx, A)
                        
                        # Vérifier si la contrainte d'affinité serait respectée
                        will_have_affinity = (not groups[g_id] or 
                                            has_affinity_in_group(groups[g_id], idx))
                        
                        # Priorité aux groupes où la contrainte est respectée
                        priority = 1 if will_have_affinity else 0
                        candidates.append((priority, score, random.random(), g_id))
                
                if candidates:
                    # Trier par priorité (contrainte respectée), puis par score
                    candidates.sort(reverse=True)
                    _, _, _, best_group = candidates[0]
                    groups[best_group].append(idx)
                    group_scores[best_group] = compute_group_score(groups[best_group], A)
            
            # Vérifier si la contrainte globale est respectée
            satisfied_count = count_satisfied_individuals(groups, A)
            constraint_satisfied = satisfied_count >= (n - min_affinity_per_person)
            
            return groups, group_scores, constraint_satisfied

        def debug_group_affinity(group: List[int], A: List[List[int]], names: List[str]) -> None:
            """Affiche en détail les affinités dans un groupe pour debug."""
            
            for i, person in enumerate(group): # Pour chaque personne dans le groupe
                person_affinities = []
                for j, other in enumerate(group): #
                    if i != j:
                        if A[person][other] > 0:
                            person_affinities.append(f"vote pour {names[other]} ({A[person][other]})")
                        if A[other][person] > 0:
                            person_affinities.append(f"reçoit vote de {names[other]} ({A[other][person]})")
                
                if person_affinities:
                    print(f"    {names[person]}: {', '.join(person_affinities)}")
                else:
                    print(f"    {names[person]}: aucune affinité")
            
            # Calculer et afficher toutes les paires
            print(f"  Paires d'affinité:")
            total = 0
            for i in range(len(group)):
                for j in range(i + 1, len(group)):
                    idx1, idx2 = group[i], group[j]
                    pair_score = A[idx1][idx2] + A[idx2][idx1]
                    if pair_score > 0:
                        print(f"    {names[idx1]} ↔ {names[idx2]}: {pair_score}")
                        total += pair_score
            print(f"  Score total calculé: {total}")

        def optimize_groups(k: int, votes_par_index, n, total_iterations: int = 5000) -> None:
            """
            Fonction principale d'optimisation des groupes.
            Elle utilise l'approche d'un algorithme glouton pour assigner les étudiants
            à des groupes en respectant les contraintes d'affinité.
            """

            print(f"Nombre d'étudiants: {n}")
            print(f"Nombre de groupes souhaités: {k}")
            print(f"Nombre total d'itérations: {total_iterations}")

            # Créer la matrice d'affinité
            A, index_to_name = create_affinity_matrix(etudiants, votes_par_index)

            # Initialisation de la meilleure solution
            global_best_groups = None
            global_best_scores = None
            global_best_total_score = -1
            global_best_satisfied_count = 0
            global_best_iteration = 0

            # Boucle d'optimisation gloutonne
            for iteration in range(total_iterations):
                groups, group_scores, constraint_satisfied = assign_groups_with_constraints(
                    n, k, A, min_affinity_per_person=0
                )
                total_score = sum(group_scores)
                satisfied_count = count_satisfied_individuals(groups, A)

                is_better = (
                    satisfied_count > global_best_satisfied_count or
                    (satisfied_count == global_best_satisfied_count and total_score > global_best_total_score)
                )
                if is_better:
                    global_best_groups = [group.copy() for group in groups]
                    global_best_scores = group_scores.copy()
                    global_best_total_score = total_score
                    global_best_satisfied_count = satisfied_count
                    global_best_iteration = iteration + 1


            if not constraint_satisfied:
                print("Attention : Certaines personnes n'ont aucune affinité dans leur groupe.")

            
            print(f"\nOptimisation terminée !")
            print(f"Meilleure solution trouvée à l'itération {global_best_iteration}")

            groups = global_best_groups
            group_scores = global_best_scores
            total_score = global_best_total_score
            satisfied_count = global_best_satisfied_count

            # Affichage des résultats finaux
            print(f"\n{'='*70}")
            print("RÉSULTATS FINAUX")
            print(f"{'='*70}")
            print(f"Score total d'affinité: {total_score}")
            print(f"Personnes avec au moins une affinité dans leur groupe: {satisfied_count}/{n}")
            print(f"Taux de satisfaction: {satisfied_count/n*100:.1f}%")

            print(f"\nRépartition finale:\n")
            for i, group in enumerate(groups):
                
                score = group_scores[i]
                satisfied_in_group = sum(
                    1 for person in group if any(A[person][other] > 0 for other in group if other != person)
                )

                names = [index_to_name[idx] for idx in group]
                print(f"Groupe {i+1} ({len(group)} personnes, score: {score}, {satisfied_in_group}/{len(group)} satisfaites):")
                print(f"  {', '.join(names)}")


                if score < len(group):
                    print(f"Analyse détaillée (score {score} semble faible pour {satisfied_in_group} satisfaites):")
                 #   debug_group_affinity(group, A, names)
        
        students = self.dao.get_students_by_project(self.project.id).data
        etudiants = [s.username for s in students]
        student_forms = self.dao.get_student_forms_by_project(self.project.id).data
        votes_par_index = {
            sf.student.username: {vote.username: points for vote, points in sf.votes}
            for sf in student_forms
        }
        n = len(etudiants)
        optimize_groups(k, votes_par_index, n, total_iterations)
        return Result(True, "Clustering students based on project preferences is not yet implemented.")

    def __str__(self):
        return f"Project Dashboard for {self.teacher.username}.\nProject: {self.project}\n"
