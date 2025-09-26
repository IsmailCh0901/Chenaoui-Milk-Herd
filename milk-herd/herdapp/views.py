from rest_framework import viewsets
from .models import Animal, MilkRecord
from .serializers import AnimalSerializer, MilkRecordSerializer
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from django.db.models import Q, Sum, Count
from datetime import date, timedelta





class AnimalViewSet(viewsets.ModelViewSet):
    queryset = Animal.objects.all().select_related("sire","dam")
    serializer_class = AnimalSerializer

class MilkRecordViewSet(viewsets.ModelViewSet):
    queryset = MilkRecord.objects.select_related("animal").all()
    serializer_class = MilkRecordSerializer



def animal_list(request):
    qs = Animal.objects.select_related('sire', 'dam')
    q = request.GET.get('q', '').strip()
    sex = request.GET.get('sex', '')
    order = request.GET.get('order', 'ear_tag')
    view_mode = request.GET.get('view', 'table')

    if q:
        qs = qs.filter(Q(ear_tag__icontains=q) | Q(name__icontains=q) | Q(breed__icontains=q))
    if sex in ('M','F','U'):
        qs = qs.filter(sex=sex)
    if order not in {'ear_tag','name','breed','date_of_birth','-date_of_birth'}:
        order = 'ear_tag'
    qs = qs.order_by(order)

    # existing pagination stuff ...
    from django.core.paginator import Paginator
    paginator = Paginator(qs, 10)
    page_obj = paginator.get_page(request.GET.get('page', 1))

    # Stats already used
    females = Animal.objects.filter(sex=Animal.Sex.FEMALE).count()
    males   = Animal.objects.filter(sex=Animal.Sex.MALE).count()
    total   = Animal.objects.count()
    unknown = total - females - males

    # Milk last 7 days (fill zeros)
    today = date.today()
    start = today - timedelta(days=6)
    labels = [(start + timedelta(days=i)).isoformat() for i in range(7)]
    rows = (MilkRecord.objects
            .filter(date__range=[start, today])
            .values('date').annotate(total=Sum('liters')).order_by('date'))
    m = {r['date'].isoformat(): float(r['total']) for r in rows}
    milk_series = [m.get(d, 0) for d in labels]

    # Top breeds
    breed_qs = (Animal.objects.exclude(breed="")
                .values('breed').annotate(c=Count('id')).order_by('-c')[:5])
    breed_labels = [b['breed'] for b in breed_qs]
    breed_series = [b['c'] for b in breed_qs]

    ctx = {
        'animals': page_obj.object_list, 'page_obj': page_obj, 'paginator': paginator,
        'q': q, 'sex': sex, 'order': order, 'view_mode': 'cards' if view_mode == 'cards' else 'table',
        'stats': {'total': total, 'females': females, 'males': males},

        # charts
        'milk_labels': labels,
        'milk_series': milk_series,
        'sex_series': [females, males, unknown],
        'breed_labels': breed_labels,
        'breed_series': breed_series,
    }
    return render(request, 'herdapp/animal_list.html', ctx)

def animal_detail(request, pk: int):
    animal = get_object_or_404(Animal.objects.select_related('sire', 'dam'), pk=pk)
    children = animal.children().order_by('date_of_birth', 'ear_tag')


    # Milk data for chart
    milk = list(animal.milk_records.order_by('date').values('date', 'liters'))
    for m in milk:
        m['date'] = m['date'].isoformat()
        m['liters'] = float(m['liters'])

    # Pedigree depth (levels): default 3, clamp 1..6
    try:
        depth = int(request.GET.get('depth', 3))
    except ValueError:
        depth = 3
    depth = max(1, min(depth, 6))
    pedigree = build_pedigree_data(animal, depth)

    ctx = {
        'animal': animal,
        'children': children,
        'milk': milk,
        'pedigree': pedigree,
        'pedigree_depth': depth,
    }
    return render(request, 'herdapp/animal_detail.html', ctx)

def build_pedigree_data(animal: Animal | None, depth: int, share: float = 100.0):
    """
    Returns a nested dict: {'id','ear_tag','name','breed','share','sire','dam'}
    share = genetic contribution %, 100 for the root, then halves each generation.
    """
    if not animal or depth <= 0:
        return None
    return {
        "id": animal.id,
        "ear_tag": animal.ear_tag,
        "name": animal.name,
        "breed": animal.breed,
        "share": round(share, 1),
        "sire": build_pedigree_data(animal.sire, depth - 1, share / 2) if animal.sire else None,
        "dam": build_pedigree_data(animal.dam, depth - 1, share / 2) if animal.dam else None,
    }



