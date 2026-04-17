from django.db import models
from django.conf import settings

class LibraryEntry(models.Model):
    STATUS_WISHLIST = "wishlist"
    STATUS_PLAYING = "playing"
    STATUS_COMPLETED = "completed"
    STATUS_DROPPED = "dropped"

    ALLOWED_STATUSES = (
        STATUS_WISHLIST,
        STATUS_PLAYING,
        STATUS_COMPLETED,
        STATUS_DROPPED,
    )

    external_game_id = models.CharField(max_length=100)
    status = models.CharField(max_length=20)
    hours_played = models.IntegerField(default=0)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, # IMPORTANTE: usar el modelo de usuario configurado en settings
        on_delete=models.CASCADE,
        null=True, # para no romper datos existentes, aunque en producción debería ser False
        blank=True, # para permitir que el campo sea opcional en formularios
        related_name="library_entries"
    )

    # --- Simple methods for easy unit tests (not used by the exercises) ---

    def external_id_length(self) -> int:
        return len(self.external_game_id or "")

    def external_id_upper(self) -> str:
        return (self.external_game_id or "").upper()

    def hours_played_label(self) -> str:
        if self.hours_played == 0:
            return "none"
        elif self.hours_played < 10:
            return "low"
        else:
            return "high"

    def status_value(self) -> int:
        if self.status == self.STATUS_WISHLIST:
            return 0
        elif self.status == self.STATUS_PLAYING:
            return 1
        elif self.status == self.STATUS_COMPLETED:
            return 2
        elif self.status == self.STATUS_DROPPED:
            return 3
        else:
            return -1
