# forms.py
from django import forms

class CsvUploadForm(forms.Form):
    file = forms.FileField()

class CssUploadForm(forms.Form):
    file = forms.FileField()

    def clean_file(self):
        uploaded_file = self.cleaned_data['file']
        if not uploaded_file.name.endswith('.csv'):
            raise forms.ValidationError("El archivo no es un CSV.")
        return uploaded_file