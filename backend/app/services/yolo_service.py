from ultralytics import YOLO


class YOLOService:
    def __init__(self):
        self.model = YOLO("yolo11n.pt")

    def detect(self, image):
        return self.model(image)

    def detect_people(self, image):
        results = self.model(
            image,
            imgsz=1280,
            verbose=False,
        )

        detections = []

        for result in results:
            names = result.names

            for box in result.boxes:
                class_id = int(box.cls[0])

                if names[class_id] != "person":
                    continue

                confidence = float(box.conf[0])

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                detections.append(
                    {
                        "class_id": class_id,
                        "class_name": names[class_id],
                        "confidence": round(confidence, 3),
                        "x1": int(x1),
                        "y1": int(y1),
                        "x2": int(x2),
                        "y2": int(y2),
                    }
                )

        return detections

    def detect_and_draw(self, image):
        results = self.model(
            image,
            imgsz=1280,
            verbose=False,
        )

        return results[0].plot()

    def track_people(self, image):
        results = self.model.track(
            image,
            persist=True,
            tracker="bytetrack.yaml",
            imgsz=1280,
            verbose=False,
        )

        detections = []

        for result in results:

            if result.boxes is None:
                continue

            names = result.names

            for box in result.boxes:

                class_id = int(box.cls[0])

                if names[class_id] != "person":
                    continue

                confidence = float(box.conf[0])

                x1, y1, x2, y2 = box.xyxy[0].tolist()

                track_id = None

                if box.id is not None:
                    track_id = int(box.id.item())

                detections.append(
                    {
                        "track_id": track_id,
                        "class_id": class_id,
                        "class_name": names[class_id],
                        "confidence": round(confidence, 3),
                        "x1": int(x1),
                        "y1": int(y1),
                        "x2": int(x2),
                        "y2": int(y2),
                    }
                )

        return detections

    def track_and_draw(self, image):
        results = self.model.track(
            image,
            persist=True,
            tracker="bytetrack.yaml",
            imgsz=1280,
            verbose=False,
        )

        return results[0].plot()