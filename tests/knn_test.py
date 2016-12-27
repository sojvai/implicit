from __future__ import print_function
import unittest

import numpy as np
from scipy.sparse import csr_matrix

import implicit


class NearestNeighboursTest(unittest.TestCase):

    def testNearestNeighbours(self):
        counts = csr_matrix([[5, 1, 0, 9, 0, 0],
                             [0, 2, 1, 1, 0, 0],
                             [7, 0, 3, 0, 0, 0],
                             [1, 8, 0, 0, 0, 0],
                             [0, 0, 4, 4, 0, 0],
                             [0, 3, 0, 0, 0, 2],
                             [0, 0, 0, 0, 6, 0]], dtype=np.float64)
        counts = implicit.nearest_neighbours.tfidf_weight(counts).tocsr()

        # compute all neighbours usiong matrix dot product
        all_neighbours = counts.dot(counts.T).tocsr()
        K = 3
        knn = implicit.nearest_neighbours.all_pairs_knn(counts, K).tocsr()

        for rowid in range(counts.shape[0]):
            # make sure values match
            for colid, data in zip(knn[rowid].indices, knn[rowid].data):
                self.assertAlmostEqual(all_neighbours[rowid, colid], data)

            # make sure top K selected
            row = all_neighbours[rowid]
            self.assertEqual(set(knn[rowid].indices),
                             set(colid for colid, _ in
                                 sorted(zip(row.indices, row.data), key=lambda x: -x[1])[:K]))


if __name__ == "__main__":
    unittest.main()
