# update_calories.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'diettracker.settings')
django.setup()

from tracker.models import Entry

def update_calories():
    # Exemple d'estimations simples (à personnaliser selon vos besoins)
    calorie_map = {
        "Steak de soja": 150,
        "100 gr muesli avec lait de soja": 200,
        "1 café avec lait de soja": 50,
        "Pamplemousse": 60,
        "1 Yaourt": 80,
    }
    
    entries = Entry.objects.filter(activity='Nourriture', kcal__isnull=True)
    for entry in entries:
        for food, kcal in calorie_map.items():
            if food.lower() in entry.data.lower():
                entry.kcal = kcal
                entry.save()
                print(f"Updated {entry.data} with {kcal} kcal")
                break
    
    print("Mise à jour des calories terminée !")

if __name__ == '__main__':
    update_calories()