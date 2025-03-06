# import_csv.py
import csv
import os
from datetime import datetime
import django

# Configurer l'environnement Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diettracker.settings')
django.setup()

# Importer le modèle après la configuration
from tracker.models import Entry

def import_data():
    with open('data/diet-tracker-log.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            try:
                date = datetime.strptime(row['Date'], '%d/%m/%Y').date()
                time = datetime.strptime(row['Heure'], '%H:%M').time()
                Entry.objects.create(
                    date=date,
                    time=time,
                    period=row['Période'],
                    activity=row['Activité'],
                    data=row['Data'],
                    kcal=float(row['Kcal']) if row['Kcal'] else None
                )
            except:
                pass
    print("Importation terminée avec succès !")

if __name__ == '__main__':
    import_data()