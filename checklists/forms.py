from django import forms
from .models import Area, ChecklistItem


class AreaForm(forms.ModelForm):
    class Meta:
        model = Area
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: Inglês"}),
        }


class ChecklistItemForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop("user", None)
        super().__init__(*args, **kwargs)

        if self.user:
            self.fields["area"].queryset = Area.objects.filter(user=self.user).order_by("name")

    class Meta:
        model = ChecklistItem
        fields = ["area", "title"]
        widgets = {
            "area": forms.Select(attrs={"class": "form-select"}),
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "Ex: Fazer exercício 1"}),
        }
