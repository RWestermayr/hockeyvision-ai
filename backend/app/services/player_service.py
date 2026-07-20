from app.models.player import Player
from app.models.tracking import TrackHistory


class PlayerService:
    """
    Erstellt Player-Objekte aus einer TrackHistory.
    """

    def create_players(
        self,
        history: TrackHistory,
    ) -> list[Player]:

        players: list[Player] = []

        for track in history.tracks:

            players.append(
                Player(
                    track_id=track.track_id,
                    track=track,
                )
            )

        return players