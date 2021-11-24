import unittest

import torch
torch.set_num_threads(1)

from sentence_transformers import SentenceTransformer

class TestScores(unittest.TestCase):
    def test_text_encodes(self):
        model = SentenceTransformer('paraphrase-albert-small-v2', device="cpu")
        _test = model.encode(["warmup test"])

    def test_scores_match(self):
        model = SentenceTransformer('paraphrase-albert-small-v2', device="cpu")
        _test = model.encode(["warmup test"])
        self.assertEqual(_test.shape, (1, 768))
        self.assertAlmostEqual(_test.sum(), -3.0101223, 3, "Warmup test encoding not as expected")

