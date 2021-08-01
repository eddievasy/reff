from django.utils import timezone
from django.db import models

date_generated = models.DateTimeField(default=timezone.now)
print(str(date_generated))