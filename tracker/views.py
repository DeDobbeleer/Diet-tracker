# tracker/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Entry
from .forms import EntryForm, ImportCSVForm
from django.db.models import Sum
from django.core.paginator import Paginator
from django.http import HttpResponse
import csv
from datetime import datetime
from io import TextIOWrapper

def entry_list(request):
    period_filter = request.GET.get('period', '')
    entries = Entry.objects.all().order_by('date', 'time')
    if period_filter:
        entries = entries.filter(period=period_filter)
    
    paginator = Paginator(entries, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Calories brûlées (activités physiques)
    daily_calories_burned_qs = (
        Entry.objects
        .filter(period='06 Activité Physique', kcal__isnull=False)
        .values('date')
        .annotate(total_kcal=Sum('kcal'))
        .order_by('date')
    )
    daily_calories_burned = list(daily_calories_burned_qs)  # Convertir en liste
    
    # Calories consommées (nourriture)
    daily_calories_consumed_qs = (
        Entry.objects
        .filter(activity='Nourriture', kcal__isnull=False)
        .values('date')
        .annotate(total_kcal=Sum('kcal'))
        .order_by('date')
    )
    daily_calories_consumed = list(daily_calories_consumed_qs)  # Convertir en liste
    
    periods = [choice[0] for choice in Entry.PERIOD_CHOICES]
    
    return render(request, 'tracker/entry_list.html', {
        'page_obj': page_obj,
        'daily_calories_burned': daily_calories_burned,
        'daily_calories_consumed': daily_calories_consumed,
        'periods': periods,
        'selected_period': period_filter,
    })

def add_entry(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('entry_list')
    else:
        form = EntryForm()
    return render(request, 'tracker/add_entry.html', {'form': form})

def edit_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'POST':
        form = EntryForm(request.POST, instance=entry)
        if form.is_valid():
            form.save()
            return redirect('entry_list')
    else:
        form = EntryForm(instance=entry)
    return render(request, 'tracker/edit_entry.html', {'form': form, 'entry': entry})

def delete_entry(request, entry_id):
    entry = get_object_or_404(Entry, id=entry_id)
    if request.method == 'POST':
        entry.delete()
        return redirect('entry_list')
    return render(request, 'tracker/delete_entry.html', {'entry': entry})

def export_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="diet-tracker-export.csv"'
    writer = csv.writer(response)
    writer.writerow(['Date', 'Heure', 'Période', 'Activité', 'Data', 'Kcal'])
    entries = Entry.objects.all().order_by('date', 'time')
    for entry in entries:
        writer.writerow([
            entry.date.strftime('%d/%m/%Y'),
            entry.time.strftime('%H:%M'),
            entry.period,
            entry.activity,
            entry.data,
            entry.kcal if entry.kcal is not None else ''
        ])
    return response

def import_csv(request):
    if request.method == 'POST':
        form = ImportCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = TextIOWrapper(request.FILES['csv_file'].file, encoding='utf-8')
            reader = csv.DictReader(csv_file)
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
                except (ValueError, KeyError) as e:
                    # En cas d'erreur (format invalide), passer à la ligne suivante
                    continue
            return redirect('entry_list')
    else:
        form = ImportCSVForm()
    return render(request, 'tracker/import_csv.html', {'form': form})