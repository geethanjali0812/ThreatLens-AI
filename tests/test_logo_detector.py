
import unittest
from pathlib import Path
from PIL import Image

from logo_detector import compare_logos


class LogoDetectorTests(unittest.TestCase):
    def setUp(self):
        self.project_folder = Path(__file__).resolve().parents[1]
        self.logo_folder = self.project_folder / "data" / "logos"

    def test_identical_logo_has_100_percent_similarity(self):
        logo_files = list(self.logo_folder.glob("*.png"))
        self.assertTrue(logo_files, "No saved PNG logo was found")

        logo_path = str(logo_files[0])
        similarity = compare_logos(logo_path, logo_path)

        self.assertEqual(similarity, 100.0)

    def test_different_logo_has_lower_similarity(self):
        logo_files = list(self.logo_folder.glob("*.png"))
        self.assertTrue(logo_files, "No saved PNG logo was found")

        official_logo = str(logo_files[0])
        candidate_logo = self.project_folder / "tests" / "different_logo.png"

        Image.new("RGB", (128, 128), (255, 0, 0)).save(candidate_logo)

        try:
            similarity = compare_logos(
                official_logo, str(candidate_logo)
            )
            self.assertLess(similarity, 100.0)
        finally:
            if candidate_logo.exists():
                candidate_logo.unlink()

    def test_missing_logo_file_returns_zero(self):
        similarity = compare_logos(
            "missing_official_logo.png",
            "missing_candidate_logo.png"
        )
        self.assertEqual(similarity, 0.0)

    def test_invalid_image_file_returns_zero(self):
        invalid_logo = self.project_folder / "tests" / "invalid_logo.png"

        try:
            with invalid_logo.open("w") as file:
                file.write("This is not a valid image")

            similarity = compare_logos(
                str(invalid_logo),
                str(invalid_logo)
            )
            self.assertEqual(similarity, 0.0)
        finally:
            if invalid_logo.exists():
                invalid_logo.unlink()


if __name__ == "__main__":
    unittest.main()
