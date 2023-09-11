from django.db import models


#class Card(models.Model):
#    title = models.CharField(max_length=100)
#   content = models.TextField()

#    def __str__(self):
#        return self.title

class Card_conect(models.Model):
    title = models.CharField(max_length=100)
    x = models.FloatField()
    y = models.FloatField()

    def __str__(self):
        return self.title


class MsgModel(models.Model):
    messaging_product = models.CharField(max_length=100)
    recipient_type = models.CharField(max_length=100)
    to = models.CharField(max_length=100)
    type_msg = models.CharField(
        max_length=20,
        choices=[
            ('interactive', 'Interactive'),
            ('text', 'Text'),
            ('reaction', 'Reaction'),
            ('image', 'Image'),
            ('audio', 'Audio'),
            ('video', 'Video'),
            ('document', 'Document'),
            ('template', 'Template'),
            ('location', 'Location'),
        ]
    )
    audio_id = models.CharField(max_length=100, blank=True, null=True)
    document_id = models.CharField(max_length=100, blank=True, null=True)
    document_filename = models.CharField(max_length=255, blank=True, null=True)
    image_id = models.CharField(max_length=100, blank=True, null=True)
    header_text = models.CharField(max_length=255, blank=True, null=True)
    body_text = models.TextField(blank=True, null=True)
    footer_text = models.CharField(max_length=255, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    location_name = models.CharField(max_length=255, blank=True, null=True)
    location_address = models.CharField(max_length=255, blank=True, null=True)
    reaction_message_id = models.CharField(max_length=100, blank=True, null=True)
    reaction_emoji = models.CharField(max_length=10, blank=True, null=True)
    video_link = models.CharField(max_length=255, blank=True, null=True)  
    video_provider_name = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return f"Message to {self.to}"

