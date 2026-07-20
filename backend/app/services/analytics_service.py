from math import sqrt

from app.models.analytics import (
    AnalyticsResult,
    PlayerAnalytics,
)
from app.models.player import Player
from app.models.tracking import TrackPoint


class AnalyticsService:
    """
    Berechnet Statistiken für Spieler.
    """

    def _distance_between(
        self,
        previous: TrackPoint,
        current: TrackPoint,
    ) -> float:
        """
        Berechnet die Distanz zwischen zwei Trackpunkten.
        """

        dx = current.center_x - previous.center_x
        dy = current.center_y - previous.center_y

        return sqrt(dx * dx + dy * dy)

    def calculate_distance(self, player: Player) -> float:
        """
        Berechnet die zurückgelegte Distanz in Pixeln.
        """

        history = player.track.history

        if len(history) < 2:
            return 0.0

        distance = 0.0

        for previous, current in zip(history[:-1], history[1:]):
            distance += self._distance_between(previous, current)

        return distance

    def calculate_average_speed(
        self,
        player: Player,
        fps: float = 25.0,
    ) -> float:
        """
        Durchschnittsgeschwindigkeit in Pixel pro Sekunde.
        """

        history = player.track.history

        if len(history) < 2:
            return 0.0

        distance = self.calculate_distance(player)

        duration = (len(history) - 1) / fps

        if duration == 0:
            return 0.0

        return distance / duration

    def calculate_max_speed(
        self,
        player: Player,
        fps: float = 25.0,
    ) -> float:
        """
        Berechnet die maximale Geschwindigkeit
        zwischen zwei aufeinanderfolgenden Frames.
        """

        history = player.track.history

        if len(history) < 2:
            return 0.0

        max_speed = 0.0

        for previous, current in zip(history[:-1], history[1:]):

            speed = self._distance_between(previous, current) * fps

            if speed > max_speed:
                max_speed = speed

        return max_speed

    def calculate_time_on_ice(
        self,
        player: Player,
        fps: float = 25.0,
    ) -> float:
        """
        Berechnet die Zeit, die der Spieler sichtbar war.
        """

        history = player.track.history

        if len(history) < 2:
            return 0.0

        return (len(history) - 1) / fps

    def analyze_players(
        self,
        players: list[Player],
        video_id: str,
        fps: float = 25.0,
    ) -> AnalyticsResult:
        """
        Erstellt Analytics für alle Spieler.
        """

        analytics: list[PlayerAnalytics] = []

        for player in players:

            distance = self.calculate_distance(player)
            average_speed = self.calculate_average_speed(
                player,
                fps=fps,
            )
            max_speed = self.calculate_max_speed(
                player,
                fps=fps,
            )
            time_on_ice = self.calculate_time_on_ice(
                player,
                fps=fps,
            )

            analytics.append(
                PlayerAnalytics(
                    track_id=player.track_id,
                    distance=round(distance, 2),
                    average_speed=round(average_speed, 2),
                    max_speed=round(max_speed, 2),
                    time_on_ice=round(time_on_ice, 2),
                    track_points=len(player.track.history),
                )
            )

        analytics.sort(
            key=lambda player: player.distance,
            reverse=True,
        )

        return AnalyticsResult(
            video_id=video_id,
            player_count=len(analytics),
            players=analytics,
        )