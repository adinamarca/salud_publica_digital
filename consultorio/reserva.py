# forms.py
from django import forms
from datetime import date, datetime

class Reserva(forms.Form):
    region      = forms.ChoiceField(label='Región', choices=[], required=True)
    comuna      = forms.ChoiceField(label='Comuna', choices=[], required=True)
    consultorio = forms.ChoiceField(label='Consultorio', choices=[], required=True)
    motivo      = forms.CharField(label='Motivo de Consulta', max_length=100, required=True)
    fecha       = forms.DateTimeField(label='Fecha de Consulta', widget=forms.SelectDateWidget, required=True)
    
    def is_valid(self):
        
        valid = False
        
        for field in ["region", "comuna", "consultorio", "motivo", "fecha"]:

            if field in self.data:
                valid = True
            else:
                valid = False
                break

            if (self.data[field] == "") or (self.data[field] is None):
                valid = False
                break
            
        return valid