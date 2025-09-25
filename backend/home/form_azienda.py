# import form class from django
from django import forms
 
# import GeeksModel from models.py
from home.models import Ordine,Fornitori,Cantiere,Azienda
 
# create a ModelForm
class FormAzienda(forms.ModelForm):
    # specify the name of model to use
    
    class Meta:
        model = Azienda
        fields = "__all__"
        #exclude = ('mestesso','magazzino',)
    
    def __init__(self,*args,**kwargs):
        
        #self.azienda = azienda
        #az = Azienda.objects.get(pk=azienda)
        #super().__init__(*args, **kwargs)
        super(FormAzienda, self).__init__(*args, **kwargs)
        #if instance is None:
        #self.fields['data_ordine'] = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
        
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

        #fa=Fornitori.objects.filter(azienda=self.azienda)
        #self.fields['fornitore'] = forms.ModelChoiceField(label="Fornitore", required=False,queryset=fa,
        #                                         widget=forms.Select(choices=fa,
        #                                                             attrs={'style': 'max-width: 100%'}))

        #ca = az.getCantieri()
        #self.fields['cantiere'] = forms.ModelChoiceField(label="Cantiere", required=False,queryset=ca,
        #                                         widget=forms.Select(choices=ca,
        #                                                            attrs={'style': 'max-width: 100%'}))

        #self.fields['mestesso'] = forms.ChoiceField(widget=forms.CheckboxInput(attrs={'class':'form-control form-check-input'}))
        #self.fields['magazzino'] = forms.ChoiceField(widget=forms.CheckboxInput(attrs={'class':'form-control form-check-input'}))

            #cz = Cliente.objects.filter(azienda_id=self.azienda).values_list('id', 'codcf')
            #self.fields['cliente'] = forms.CharField(label="Cliente", required=True,
            #                                        widget=forms.Select(choices=cz,
            #                                                            attrs={'style': 'width: 300px;'}))
        #self.fields['data_ordine'] =  forms.CharField(label="Descrizione", required=True,
            #                                             widget=forms.Textarea(attrs={'rows': 2}))
        #else:
    """
    def clean_cliente_id(self):
        cliente_id = self.cleaned_data.get('cliente')
        try:
            self.cliente = Cliente.objects.get(pk=cliente_id)
        except Cliente.DoesNotExist:
            raise forms.ValidationError('Sorry, that course id is not valid.')

        return cliente_id
    
    
    def save(self, commit=True):

        instance = super(FormCantiere, self).save(commit=commit)
        #cl = Cliente.objects.get(pk=1) #instance.cliente)
        #instance.cliente = cl
        
        instance.save()
        return instance
    
    """