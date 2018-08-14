from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError


from app.validators import FileSizeValidator


# Status definition for ticket model.
PENDING_TICKET = 1
COMPLETED_TICKET = 2

TICKET_STATUS_CHOICES = (
    (PENDING_TICKET, 'Pendiente'),
    (COMPLETED_TICKET, 'Completado'),
)


class Ticket(models.Model):
    images_quantity = models.PositiveSmallIntegerField(
        verbose_name='cantidad de imágenes',
    )

    status = models.PositiveSmallIntegerField(
        choices=TICKET_STATUS_CHOICES,
        default=PENDING_TICKET,
        verbose_name='estado',
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='creado por',
    )

    created_at = models.DateField(
        auto_now_add=True,
        verbose_name='fecha de creación',
    )

    def __str__(self):
        return '{0} - {1} - {2}'.format(
            self.id,
            self.get_status_display(),
            self.created_by,
        )

    class Meta:
        ordering = ('created_by',)

    def clean(self):
        if self.ticketimage_set.count() >= self.images_quantity:
            raise ValidationError('No puede agregar mas de {} imagenes'.format(
                self.images_quantity,
            ))


class TicketImage(models.Model):
    image = models.ImageField(
        max_length=255,
        validators=[FileSizeValidator(4000)],
    )

    ticket = models.ForeignKey(
        'api.Ticket',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return 'Img id:{0} - Ticket: {1}'.format(
            self.id,
            self.ticket,
        )

    class Meta:
        ordering = ('ticket',)
