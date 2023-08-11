from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from django.core.exceptions import ValidationError

from django.core.exceptions import ValidationError

class Challenge(models.Model):

    challenger = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges_as_challenger')
    player = models.ForeignKey(User, on_delete=models.CASCADE, related_name='challenges_as_player')
    title = models.CharField(max_length=100)
    description = models.TextField()
    accepted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.challenger.username} vs {self.player.username}"

    def clean(self):
        if self.challenger_id and self.player_id and self.challenger == self.player:
            raise ValidationError("Challenger and player cannot be the same user.")


class Task(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    player_comment = models.TextField(blank=True)
    challenger_comment = models.TextField(blank=True)
    sent_by_player = models.BooleanField(default=False)
    proof = models.FileField(upload_to='task_proofs/', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png'])], blank=True)
    completed = models.BooleanField(default=False)
    limit_date = models.DateField(null=True, blank=True)
    last_sent_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.limit_date and self.limit_date < timezone.now().date():
            raise ValidationError("Limit date cannot be in the past.")
