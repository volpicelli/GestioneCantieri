from django.shortcuts import render,redirect
from django.views.generic  import View,CreateView,DetailView,ListView
from django.views.generic.edit import UpdateView
from django.core.exceptions import ObjectDoesNotExist

from django.db.models import Sum

from django.template import loader
from django.template import Template, Context
from django.http import HttpResponse,HttpResponseRedirect
from home.models import Azienda
from .form_azienda import FormAzienda
# Create your views here.

class CreateAzienda(View):
    model=Azienda
    form_class = FormAzienda
    success_url = '/'
        #template_name='cantiere_nuovo.html'
        #create_form = Form.create(auto__model=Cantiere)
        #a_table = Table(auto__model=Cantiere)
    def get(self,request):
        context ={}
        context['form']= FormAzienda()
        #az = Azienda.objects.get(pk=request.session['azienda'])
        #context['clienti'] = az.azienda_cliente.all()
        return render(request, "createazienda_inc.html", context)


