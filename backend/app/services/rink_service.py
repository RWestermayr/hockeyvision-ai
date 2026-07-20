import math

import cv2
import numpy as np

from app.models.rink import (
    RinkGeometry,
    RinkLine,
    RinkPoint,
)


class RinkService:
    """
    Service zur Erkennung und Klassifizierung
    von Spielfeldlinien eines Hockeyfeldes.
    """

    def create_ice_mask(
        self,
        image,
    ):
        """
        Erstellt eine Binärmaske der Eisfläche.
        """

        hsv = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2HSV,
        )

        lower = np.array(
            [
                0,
                0,
                150,
            ],
            dtype=np.uint8,
        )

        upper = np.array(
            [
                180,
                70,
                255,
            ],
            dtype=np.uint8,
        )

        mask = cv2.inRange(
            hsv,
            lower,
            upper,
        )

        kernel = np.ones(
            (7, 7),
            np.uint8,
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            kernel,
        )

        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            kernel,
        )

        return mask

    def detect_lines(
        self,
        mask,
    ):
        """
        Führt die Kantenerkennung und
        Hough-Transformation aus.
        """

        edges = cv2.Canny(
            mask,
            50,
            150,
        )

        return cv2.HoughLinesP(
            edges,
            rho=1,
            theta=math.pi / 180,
            threshold=100,
            minLineLength=150,
            maxLineGap=25,
        )

    def line_length(
        self,
        x1,
        y1,
        x2,
        y2,
    ) -> float:

        return math.sqrt(
            (x2 - x1) ** 2 +
            (y2 - y1) ** 2
        )

    def line_angle(
        self,
        x1,
        y1,
        x2,
        y2,
    ) -> float:

        return math.degrees(
            math.atan2(
                y2 - y1,
                x2 - x1,
            )
        )

    def line_midpoint(
        self,
        x1,
        y1,
        x2,
        y2,
    ) -> RinkPoint:

        return RinkPoint(
            x=float((x1 + x2) / 2),
            y=float((y1 + y2) / 2),
        )

    def build_lines(
        self,
        raw_lines,
    ) -> list[RinkLine]:
        """
        Wandelt die Hough-Ausgabe in
        RinkLine-Objekte um.
        """

        result: list[RinkLine] = []

        if raw_lines is None:
            return result

        for line in raw_lines:

            x1, y1, x2, y2 = line

            length = self.line_length(
                x1,
                y1,
                x2,
                y2,
            )

            #
            # sehr kurze Linien ignorieren
            #

            if length < 150:
                continue

            angle = self.line_angle(
                x1,
                y1,
                x2,
                y2,
            )

            midpoint = self.line_midpoint(
                x1,
                y1,
                x2,
                y2,
            )

            result.append(
                RinkLine(
                    start=RinkPoint(
                        x=float(x1),
                        y=float(y1),
                    ),
                    end=RinkPoint(
                        x=float(x2),
                        y=float(y2),
                    ),
                    length=float(length),
                    angle=float(angle),
                    midpoint=midpoint,
                    classification="unknown",
                )
            )

        return result

    def line_distance(
        self,
        line1: RinkLine,
        line2: RinkLine,
    ) -> float:
        """
        Abstand zweier Linien über
        ihre Mittelpunkte.
        """

        dx = (
            line1.midpoint.x -
            line2.midpoint.x
        )

        dy = (
            line1.midpoint.y -
            line2.midpoint.y
        )

        return math.sqrt(
            dx * dx +
            dy * dy
        )
    
    def merge_lines(
        self,
        lines: list[RinkLine],
    ) -> list[RinkLine]:
        """
        Fasst nahezu identische Linien zusammen.
        """

        merged: list[RinkLine] = []

        for line in lines:

            duplicate = False

            for existing in merged:

                angle_difference = abs(
                    line.angle - existing.angle
                )

                distance = self.line_distance(
                    line,
                    existing,
                )

                #
                # ähnliche Linie gefunden
                #

                if (
                    angle_difference < 5
                    and distance < 40
                ):

                    duplicate = True

                    #
                    # längere Linie behalten
                    #

                    if line.length > existing.length:

                        merged.remove(
                            existing,
                        )

                        merged.append(
                            line,
                        )

                    break

            if not duplicate:

                merged.append(
                    line,
                )

        return merged

    def classify_lines(
        self,
        lines: list[RinkLine],
        width: int,
        height: int,
    ) -> RinkGeometry:
        """
        Erste einfache Klassifizierung
        der Linien.
        """

        geometry = RinkGeometry(
            image_width=width,
            image_height=height,
        )

        for line in lines:

            #
            # horizontale Linien
            #

            if abs(line.angle) < 10:

                #
                # sehr lange horizontale
                # Linie → Bande
                #

                if line.length > width * 0.60:

                    line.classification = "board"

                    geometry.board_lines.append(
                        line,
                    )

                #
                # übrige horizontale Linien
                # zunächst als blaue Linie
                #

                else:

                    line.classification = "blue"

                    geometry.blue_lines.append(
                        line,
                    )

            #
            # nahezu vertikale Linien
            #

            elif (
                abs(abs(line.angle) - 90)
                < 10
            ):

                line.classification = "goal"

                geometry.goal_lines.append(
                    line,
                )

            #
            # unbekannt
            #

            else:

                line.classification = "unknown"

            geometry.lines.append(
                line,
            )

        return geometry

    def detect_geometry(
        self,
        image,
    ) -> RinkGeometry:
        """
        Führt die komplette
        Spielfeldanalyse aus.
        """

        mask = self.create_ice_mask(
            image,
        )

        raw_lines = self.detect_lines(
            mask,
        )

        lines = self.build_lines(
            raw_lines,
        )

        lines = self.merge_lines(
            lines,
        )

        height, width = image.shape[:2]

        return self.classify_lines(
            lines,
            width,
            height,
        )

    def draw_geometry(
        self,
        image,
        geometry: RinkGeometry,
    ):
        """
        Zeichnet die klassifizierten Linien.
        """

        output = image.copy()

        colors = {
            "board": (0, 255, 0),
            "blue": (255, 0, 0),
            "red": (0, 0, 255),
            "goal": (255, 0, 255),
            "unknown": (0, 255, 255),
        }

        for line in geometry.lines:

            color = colors.get(
                line.classification,
                (255, 255, 255),
            )

            cv2.line(
                output,
                (
                    int(line.start.x),
                    int(line.start.y),
                ),
                (
                    int(line.end.x),
                    int(line.end.y),
                ),
                color,
                2,
            )

            cv2.circle(
                output,
                (
                    int(line.midpoint.x),
                    int(line.midpoint.y),
                ),
                4,
                (0, 0, 255),
                -1,
            )

            cv2.putText(
                output,
                line.classification,
                (
                    int(line.midpoint.x) + 6,
                    int(line.midpoint.y) - 6,
                ),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.45,
                color,
                1,
                cv2.LINE_AA,
            )

        return output    