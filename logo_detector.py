
from PIL import Image, ImageChops, ImageStat, ImageOps
import os


def compare_logos(official_logo_path, candidate_logo_path):
    """Compare two logo images and return a pixel similarity percentage."""

    if not official_logo_path or not candidate_logo_path:
        return 0.0

    if not os.path.isfile(official_logo_path):
        return 0.0

    if not os.path.isfile(candidate_logo_path):
        return 0.0

    try:
        def prepare_image(path):
            with Image.open(path) as image:
                # Convert transparency to a consistent white background.
                image = image.convert("RGBA")
                background = Image.new("RGBA", image.size, "white")
                image = Image.alpha_composite(background, image)
                image = image.convert("RGB")

                # Resize and crop to a common size for comparison.
                image = ImageOps.fit(
                    image,
                    (128, 128),
                    method=Image.Resampling.LANCZOS
                )
                return image.copy()

        official = prepare_image(official_logo_path)
        candidate = prepare_image(candidate_logo_path)

        difference = ImageChops.difference(official, candidate)
        average_difference = sum(
            ImageStat.Stat(difference).mean
        ) / 3

        similarity = max(
            0.0,
            100.0 - (average_difference / 255.0 * 100.0)
        )

        return round(similarity, 2)

    except (OSError, ValueError):
        return 0.0
