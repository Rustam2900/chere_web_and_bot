from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.translation import gettext_lazy as _


class Media(models.Model):
    class MediaType(models.TextChoices):
        IMAGE = 'image', _('Image')
        VIDEO = 'video', _('Video')
        AUDIO = 'audio', _('Audio')
        OTHER = 'other', _('Other')

    FILE_EXTENSION_MAP = {
        MediaType.IMAGE: ['jpg', 'jpeg', 'png'],
        MediaType.VIDEO: ['mp4'],
        MediaType.AUDIO: ['mp3', 'wav', 'ogg'],
        MediaType.OTHER: ['pdf', 'txt', 'zip'],
    }

    file = models.FileField(_('file'), upload_to='all_media_files/',
                            validators=[FileExtensionValidator(
                                allowed_extensions=[ext for exts in FILE_EXTENSION_MAP.values() for ext in exts])]
                            )
    type = models.CharField(_('type'), max_length=20, choices=MediaType.choices, default=MediaType.IMAGE)

    class Meta:
        verbose_name = _("Media")
        verbose_name_plural = _("Medias")

    def clean(self):
        allowed_extensions = self.FILE_EXTENSION_MAP.get(self.type, [])
        if not allowed_extensions:
            return
        if not self.file.name.split('.')[-1] in allowed_extensions:
            raise ValidationError(
                _('Invalid file extension for {}. Allowed: {}').format(self.type, ', '.join(allowed_extensions)))

    def __str__(self):
        return self.file.name
