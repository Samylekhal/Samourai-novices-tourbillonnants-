import unittest
from src.Algo import  compute_group_score, compute_individual_score, count_satisfied_individuals


class TestAlgoAffinite(unittest.TestCase):
    """Tests pour les fonctions d'affinité avec des données réelles du JSON."""

    def setUp(self):
        # Matrice d'affinité pour 6 étudiants
        self.A = [
            [0, 1, 1, 0, 1, 0],  # Étudiant 0
            [1, 0, 1, 0, 0, 0],  # Étudiant 1
            [1, 1, 0, 0, 0, 0],  # Étudiant 2
            [0, 0, 0, 0, 1, 1],  # Étudiant 3
            [0, 0, 0, 1, 0, 1],  # Étudiant 4
            [0, 0, 0, 1, 1, 0]   # Étudiant 5
        ]
        # Groupes d'étudiants. les tables représentent les indices des étudiants dans la matrice d'affinité
        self.group_1 = [0, 1]
        self.group_2 = [0, 3]
        self.group_3 = [0, 4]


    # Affiche 2 si les éudiant d'un groupe ont voté l'un pour l'autre
    def test_compute_group_score_mutual(self):
        score = compute_group_score(self.group_1, self.A)
        self.assertGreaterEqual(score, 2)

    # Affiche 0 si les étudiants d'un groupe n'ont pas d'affinités
    def test_compute_group_score_none(self):
        score = compute_group_score(self.group_2, self.A)
        self.assertEqual(score, 0)
        

    # Affiche 1 si les étudiants d'un groupe ont voté l'un pour l'autre mais pas mutuellement
    def test_compute_group_score_unilateral(self):
        score = compute_group_score(self.group_3, self.A)
        self.assertEqual(score, 1)  


    def test_compute_individual_score(self):
        # Vérifie que l'étudiant 2 placé avec 0 et 1 donne un score cohérent
        score = compute_individual_score([0, 1], 2, self.A)
        self.assertEqual(score, 4)


    def test_count_satisfied_individuals(self):
        groups = [self.group_1, self.group_3]  # groupe avec affinités + sans affinités
        count = count_satisfied_individuals(groups, self.A)
        # self.assertGreaterEqual(count, 1)
        self.assertEqual(count, 3)


if __name__ == '__main__':
    unittest.main()
