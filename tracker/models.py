# tracker/models.py
from django.db import models

class Entry(models.Model):
    PERIOD_CHOICES = [
        ('01 Petit Déjeuner', 'Petit Déjeuner'),
        ('02 Collation AM', 'Collation AM'),
        ('03 Déjeuner', 'Déjeuner'),
        ('04 Collation PM', 'Collation PM'),
        ('05 Dîner', 'Dîner'),
        ('06 Activité Physique', 'Activité Physique'),
        ('07 Hydratation', 'Hydratation'),
    ]
    
    ACTIVITY_CHOICES = [
        ('Nourriture', 'Nourriture'),
        ('Complément', 'Complément'),
        ('None', 'Aucune'),
    ]

    date = models.DateField()
    time = models.TimeField()
    period = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    activity = models.CharField(max_length=20, choices=ACTIVITY_CHOICES)
    data = models.CharField(max_length=255)
    kcal = models.FloatField(null=True, blank=True)

    def __str__(self):
        return f"{self.date} {self.time} - {self.period} - {self.data}"