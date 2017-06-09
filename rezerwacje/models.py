from django.db import models


class Auditorium(models.Model):

    name = models.CharField(max_length=128)
    capacity = models.IntegerField()
    projector = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Reservation(models.Model):

    date = models.DateField()
    auditorium = models.ForeignKey(to=Auditorium, related_name='reservations', null=True)
    comment = models.TextField(null=True)

    class Meta:
        unique_together = ("date", "auditorium")

    def __str__(self):
        return f'{self.pk}, {self.date}, {self.auditorium}'
