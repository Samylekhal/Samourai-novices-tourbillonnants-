import json
import random
from typing import List, Dict, Tuple

def load_data(filename: str) -> Tuple[List[Dict], List[str], Dict[int, List[int]]]:
    """Charge les données et prépare les structures nécessaires."""
    with open(filename, "r") as f:
        data = json.load(f)
    
    etudiants = data["formulaire"]["data"]
    
    # Mapping des IDs vers les indices
    id_to_index = {etu["id"]: i for i, etu in enumerate(etudiants)}
    names = [f"{etu['firstname']} {etu['lastname']}" for etu in etudiants]
    
    # Liste des votes par index
    votes_par_index = {
        id_to_index[etu["id"]]: [id_to_index[v] for v in etu["Votes"].values() if v in id_to_index]
        for etu in etudiants
    }
    
    return etudiants, names, votes_par_index

def create_affinity_matrix(n: int, votes_par_index: Dict[int, List[int]]) -> List[List[int]]:
    """Crée la matrice d'affinité (0 = aucun vote, 1 = vote unilatéral, 2 = mutuel)."""
    A = [[0] * n for _ in range(n)]
    
    # Remplir avec les votes unilatéraux
    for i in range(n):
        for j in votes_par_index[i]:
            A[i][j] = 1
    
    return A

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

def optimize_groups(filename: str, k: int, total_iterations: int = 5000) -> None:
    """
    Fonction principale d'optimisation des groupes.
    Elle utilise l'approche d'un algorithme glouton pour assigner les étudiants
    à des groupes en respectant les contraintes d'affinité.
    """
    # Charger les données
    print("Chargement des données...")
    etudiants, names, votes_par_index = load_data(filename)
    n = len(etudiants)

    print(f"Nombre d'étudiants: {n}")
    print(f"Nombre de groupes souhaités: {k}")
    print(f"Nombre total d'itérations: {total_iterations}")

    # Créer la matrice d'affinité
    A = create_affinity_matrix(n, votes_par_index)

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
        noms = [names[idx] for idx in group]
        score = group_scores[i]
        satisfied_in_group = sum(
            1 for person in group if any(A[person][other] > 0 for other in group if other != person)
        )

        print(f"Groupe {i+1} ({len(group)} personnes, score: {score}, {satisfied_in_group}/{len(group)} satisfaites):")
        print(f"  {', '.join(noms)}")

        if score < len(group):
            print(f"Analyse détaillée (score {score} semble faible pour {satisfied_in_group} satisfaites):")
            debug_group_affinity(group, A, names)


# Utilisation
if __name__ == "__main__":
    # Paramètres
    filename = "data/etudiants_30_votes5.json"
    k = 6  # nombre de groupes souhaités    
    optimize_groups(filename, k, total_iterations=10000)