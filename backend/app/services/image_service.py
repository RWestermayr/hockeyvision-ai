from pathlib import Path

import cv2


class ImageService:
    def load_image(self, image_path: Path):
        image = cv2.imread(str(image_path))

        if image is None:
            raise FileNotFoundError(
                f"Could not load image: {image_path}"
            )

        return image

    def save_image(self, image, output_path: Path):
        output_path.parent.mkdir(parents=True, exist_ok=True)

        cv2.imwrite(str(output_path), image)

    def get_image_size(self, image):
        height, width = image.shape[:2]

        return {
            "width": width,
            "height": height,
        }

    def draw_rectangle(
        self,
        image,
        top_left,
        bottom_right,
        color=(0, 255, 0),
        thickness=3,
    ):
        cv2.rectangle(
            image,
            top_left,
            bottom_right,
            color,
            thickness,
        )

        return image

    def draw_text(
        self,
        image,
        text,
        position,
        color=(0, 255, 0),
        scale=1.0,
        thickness=2,
    ):
        cv2.putText(
            image,
            text,
            position,
            cv2.FONT_HERSHEY_SIMPLEX,
            scale,
            color,
            thickness,
        )

        return image