from django import forms


class AddImageForm(forms.Form):
    course = forms.CharField(max_length=200, required=False)
    image = forms.ImageField(required=False)
    exam_details = forms.JSONField(required=False)
