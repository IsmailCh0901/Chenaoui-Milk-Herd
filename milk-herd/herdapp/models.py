from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import date
from django.db.models import Q

class Animal(models.Model):
    class Sex(models.TextChoices):
        FEMALE = "F", "Female"
        MALE = "M", "Male"
        UNKNOWN = "U", "Unknown"

    ear_tag       = models.CharField(max_length=50, unique=True)
    name          = models.CharField(max_length=100, blank=True)
    sex           = models.CharField(max_length=1, choices=Sex.choices, default=Sex.UNKNOWN)
    breed         = models.CharField(max_length=100, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)

    # Parents (self-references)
    sire = models.ForeignKey('self', null=True, blank=True,
                             related_name='sired_offspring',
                             on_delete=models.SET_NULL)
    dam  = models.ForeignKey('self', null=True, blank=True,
                             related_name='dam_offspring',
                             on_delete=models.SET_NULL)

    is_alive = models.BooleanField(default=True)
    notes    = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.display_name

    @property
    def display_name(self):
        return f"{self.name} ({self.ear_tag})" if self.name else self.ear_tag

    @property
    def age_days(self):
        if not self.date_of_birth:
            return None
        return (date.today() - self.date_of_birth).days

    def full_siblings(self):
        if not self.sire_id and not self.dam_id:
            return Animal.objects.none()
        return Animal.objects.filter(sire_id=self.sire_id, dam_id=self.dam_id).exclude(pk=self.pk)

    def half_siblings(self):
        q = Q()
        if self.sire_id:
            q |= Q(sire_id=self.sire_id)
        if self.dam_id:
            q |= Q(dam_id=self.dam_id)
        if not q:
            return Animal.objects.none()
        return Animal.objects.filter(q)\
            .exclude(pk=self.pk)\
            .exclude(Q(sire_id=self.sire_id, dam_id=self.dam_id))

    def children(self):
        return Animal.objects.filter(Q(sire=self) | Q(dam=self))

    def clean(self):
        # cannot be own parent
        if self.pk and (self.sire_id == self.pk or self.dam_id == self.pk):
            raise ValidationError("An animal cannot be its own parent.")
        # simple cycle guard (walk a few generations)
        if self._creates_cycle(self.sire_id) or self._creates_cycle(self.dam_id):
            raise ValidationError("Parent link would create an ancestry cycle.")
        # Enforce sex consistency for parents (optional but useful)
        if self.sire_id:
            sire = Animal.objects.filter(pk=self.sire_id).only('sex').first()
            if sire and sire.sex != Animal.Sex.MALE:
                raise ValidationError("Sire must be Male.")
        if self.dam_id:
            dam = Animal.objects.filter(pk=self.dam_id).only('sex').first()
            if dam and dam.sex != Animal.Sex.FEMALE:
                raise ValidationError("Dam must be Female.")


    def _creates_cycle(self, parent_id, max_depth=6):
        if not self.pk or not parent_id:
            return False
        seen = set()
        current = [parent_id]
        depth = 0
        while current and depth < max_depth:
            nxt = []
            for pid in current:
                if pid == self.pk:
                    return True
                if pid in seen:
                    continue
                seen.add(pid)
                p = Animal.objects.filter(pk=pid).values_list('sire_id', 'dam_id').first()
                if p:
                    s, d = p
                    if s: nxt.append(s)
                    if d: nxt.append(d)
            current = nxt
            depth += 1
        return False

class MilkRecord(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='milk_records')
    date   = models.DateField(default=timezone.now)
    liters = models.DecimalField(max_digits=6, decimal_places=2)
    notes  = models.CharField(max_length=255, blank=True)

    class Meta:
        unique_together = ('animal', 'date')
        ordering = ['-date']

    def __str__(self):
        return f"{self.animal.display_name} - {self.date} - {self.liters} L"
