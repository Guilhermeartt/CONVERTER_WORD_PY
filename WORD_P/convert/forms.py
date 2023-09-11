from django import forms
from .models import MsgModel
#from .models import Card

class MsgFormulario(forms.ModelForm):
    class Meta:
        model = MsgModel
        fields = ['messaging_product', 'recipient_type', 'to', 'type_msg', 'audio_id', 'document_id', 'document_filename', 'image_id', 'header_text', 'body_text', 'footer_text', 'longitude', 'latitude', 'location_name', 'location_address', 'reaction_message_id', 'reaction_emoji', 'video_link', 'video_provider_name']  # Adicionando os campos relacionados a video ao formulário
        
        #fields = '__all__'
        


#class CardForm(forms.ModelForm):
#    class Meta:
#        model = Card
#        fields = ['title', 'content']