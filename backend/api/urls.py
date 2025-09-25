
from django.urls import path,re_path
from api.view_azienda import *
from api.view_tipologia_lavori import *
from api.view_articoli import *
from api.view_assegnato_cantiere import *
from api.view_cliente import *
from api.view_cantiere import *
from api.view_documenti import *
from api.view_documentifornitori import *
from api.view_bancafornitore import *
from api.view_ordini import *
from api.view_fatture import *
from api.view_fatturecliente import *
from api.view_condizionipagamento import *
from api.bancafornitore_seriallizer import BancaFornitoriserializer
from api.scadenzariofatture_serializer import ScadenzarioFattureSerializer
from api.fatture_serializer import Fattureserializer
from api.condizioni_pagamento_serializer import CondizioniPagamentoserializer
from api.syncFornitori import *
from api.syncClienti import *
from api.syncBanche import *
from api.syncCondizioniPagamento import *
from rest_framework.authtoken.views import obtain_auth_token  

from api.views import   ResponsabileCantiere,AddOreLavoro,\
                        FornitoriDetail,FornitoriList,\
                        PersonaleDetail,PersonaleList,\
                        PersonaleSuCantiere,MagazzinoList,MagazzinoDetail,MagazzinoDelete,MagazzinoArticoli,CantieriPersonale,\
                        GroupMagazzino,LoginView,CustomAuthToken
from api.uploadUserAvatar import UploadUserAvatar
from api.uploadCantiereAvatar import UploadCantiereAvatar
from api.uploadAziendaAvatar import UploadAziendaAvatar
                
                        #ResponsabileDetail,ResponsabileList,ResponsabileCantiere,\

urlpatterns = [ 

        path('uploadAziendaAvatar/<int:azienda_id>', UploadAziendaAvatar.as_view(), name='uploadAvatar'),  # <-- And here
        path('uploadUserAvatar/<int:user_id>', UploadUserAvatar.as_view(), name='uploadAvatar'),  # <-- And here
        path('uploadCantiereAvatar/<int:cantiere_id>', UploadCantiereAvatar.as_view(), name='uploadCantiereAvatar'),  # <-- And here
       
        path('azienda/<int:azienda>/banche/sync', BancaFornitoriSync.as_view(), name='sync_banche'),  # <-- And here
        path('azienda/<int:azienda>/bancheclienti/sync', BancaClientiSync.as_view(), name='sync_bancheclienti'),  # <-- And here
        path('codpag/sync', CondizioniPagamentoSync.as_view(), name='sync_codpag'),  # <-- And here
  
        #path('fornitori/banca/sync', BancaFornitoriSync.as_view(), name='sync_bancafornitori'),  # <-- And here
        #path('fornitori/condpag/sync', FornitoriCondPagamentoSync.as_view(), name='sync_codpagfornitori'),  # <-- And here
        path('azienda/<int:azienda>/fornitori/sync', FornitoriSync.as_view(), name='sync_fornitori'),  # <-- And here
        
        #path('clienti/banca/sync', BancaClientiSync.as_view(), name='sync_bancaclienti'),  # <-- And here
        #path('clienti/condpag/sync', ClientiCondPagamentoSync.as_view(), name='sync_codpagclienti'),  # <-- And here
        #path('clienti/sync', ClientiSync.as_view(), name='sync_clienti'),  # <-- And here
        path('azienda/<int:azienda>/clienti/sync', ClientiSync.as_view(), name='sync_clienti'),  # <-- And here
        
        
        path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),  # <-- And here
        path('get-token-auth/', obtain_auth_token),
        path('docupload/<int:doc_id>',UploadDocumento.as_view()),
        path('docupload/fornitore/<int:doc_id>',UploadDocumentoFornitore.as_view()),
        path('login',LoginView.as_view()),
        #path('ordinedamagazzino',OrdineDaMagazzino.as_view()),
        path('ordinecreate',OrdineCreate.as_view()),
        path('ordineupdate/<int:ordine_id>',OrdineUpdate.as_view()),
        path('ordineclose/<int:ordine_id>',CloseOrdineCreate.as_view()),


        path('azienda/<int:azienda_id>/clienti',ClientiAzienda.as_view()),
        path('azienda/<int:azienda_id>/fornitori',FornitoriAzienda.as_view()),
        path('azienda2/<int:azienda_id>/fornitori',FornitoriAzienda2.as_view()),
        path('azienda/<int:azienda_id>/cantieri',CantieriAzienda.as_view()),
        path('azienda/<int:azienda_id>/personale',PersonaleAzienda.as_view()),
        path('azienda/<int:azienda_id>/magazzino',MagazzinoAzienda.as_view()),
        path('azienda/<int:azienda_id>/ordini',OrdiniAzienda.as_view()),
        path('azienda/<int:azienda_id>/fatture',FattureAzienda.as_view()),
        path('azienda2/<int:azienda_id>/fatture',FattureAzienda2.as_view()),
        
        path('azienda/<int:azienda_id>/personale/cantiere/<int:cantiere_id>',PersonaleAziendaCantiere.as_view()),
        path('azienda/<int:azienda_id>/personale/cantieri',PersonaleAziendaAssegnatiCantieri.as_view()),
        

        path('addorelavoro/cantiere/<int:cantiere_id>/personale/<int:personale_id>/<int:ore>',AddOreLavoro.as_view()),

        path('personale/cantiere/<int:id_cantiere>',PersonaleSuCantiere.as_view()),
        path('responsabile/cantiere/<int:id_cantiere>',ResponsabileCantiere.as_view()),
        path('cantieri/personale/<int:id_personale>',CantieriPersonale.as_view()),
        path('assegnatocantiere/list', Assegnato_CantiereList.as_view()),
        path('assegnatocantiere/create', Assegnato_CantiereList.as_view()),
        path('assegnatocantiere/detail/<int:pk>', Assegnato_CantiereDetail.as_view()),
        path('assegnatocantiere/delete/<int:pk>', Assegnato_CantiereDetail.as_view()),
        path('assegnatocantiere/update/<int:pk>', Assegnato_CantiereDetail.as_view()),

        path('documentifornitoricreate/<int:cantiere_id>', DocumentiFornitoriCreate.as_view()),
        path('documentifornitori/list', DocumentiFornitoriList.as_view()),
        path('documentifornitori/cantiere/<int:cantiere_id>', DocumentiFornitoriCantiere.as_view()),

        path('documentifornitori/delete/<int:pk>', DocumentiFornitoriDelete.as_view()),
        path('documentifornitori/detail/<int:pk>', DocumentiFornitoriDetail.as_view()),



        path('documenticreate/<int:cantiere_id>', DocumentiCreate.as_view()),
        path('documenti/list', DocumentiList.as_view()),
        path('documenti/create', DocumentiList.as_view()),
        path('documenti/detail/<int:pk>', DocumentiDetail.as_view()),
        path('documenti/delete/<int:pk>', DocumentiDetail.as_view()),
        path('documenti/update/<int:pk>', DocumentiDetail.as_view()),
        path('documenti/cantiere/<int:cantiere_id>', DocumentiCantiere.as_view()),
        path('documenti/azienda/<int:azienda_id>', DocumentiAzienda.as_view()),

        path('tipologialavori/list', TipologiaLavoriList.as_view()),
        path('tipologialavori/create', TipologiaLavoriList.as_view()),
        path('tipologialavori/detail/<int:pk>', TipologiaLavoriDetail.as_view()),
        path('tipologialavori/delete/<int:pk>', TipologiaLavoriDetail.as_view()),
        path('tipologialavori/update/<int:pk>', TipologiaLavoriDetail.as_view()),

        path('fornitori/list', FornitoriList.as_view()),
        path('fornitori/create', FornitoriList.as_view()),
        path('fornitori/detail/<int:pk>', FornitoriDetail.as_view()),
        path('fornitori/delete/<int:pk>', FornitoriDetail.as_view()),
        path('fornitori/update/<int:pk>', FornitoriDetail.as_view()),

        path('condizionipagamento/list', CondizioniPagamentoList.as_view()),


        path('bancafornitori/list', BancaFornitoriList.as_view()),
        path('bancafornitori/create', BancaFornitoriList.as_view()),
        path('bancafornitori/detail/<int:pk>', BancaFornitoriDetail.as_view()),
        path('bancafornitori/delete/<int:pk>', BancaFornitoriDetail.as_view()),
        path('bancafornitori/update/<int:pk>', BancaFornitoriDetail.as_view()),

        path('personale/list', PersonaleList.as_view()),
        path('personale/create', PersonaleList.as_view()),
        path('personale/detail/<int:pk>', PersonaleDetail.as_view()),
        path('personale/delete/<int:pk>', PersonaleDetail.as_view()),
        path('personale/update/<int:pk>', PersonaleDetail.as_view()),



        path('groupmagazzino/azienda/<int:azienda_id>', GroupMagazzino.as_view()),

        path('magazzino/list', MagazzinoList.as_view()),
        path('magazzino/create', MagazzinoList.as_view()),
        path('magazzino/detail/<int:pk>', MagazzinoDetail.as_view()),
        path('magazzino/delete/<int:pk>', MagazzinoDelete.as_view()),
        path('magazzino/update/<int:pk>', MagazzinoDetail.as_view()),
        path('magazzino/articoli', MagazzinoArticoli.as_view()),


        path('cantieri/list', CantiereList.as_view()),
        ### path('cantieri/azienda/<int:azienda_id>', CantieriAzienda.as_view()),
        path('cantiere/create', CantiereList.as_view()),
        path('cantiere/detail/<int:pk>',CantiereDetail.as_view()),
        path('cantiere/delete/<int:pk>', CantiereDetail.as_view()),
        path('cantiere/update/<int:pk>',CantiereDetail.as_view()),
        path('cantiere/<int:id_cantiere>/ordini',OrdiniCantiere.as_view()),
        path('cantiere/<int:id_cantiere>/documenti',CantiereDocumenti.as_view()),
        path('cantiere/<int:id_cantiere>/documentifornitori/<int:id_fornitore>',CantiereDocumentiFornitori.as_view()),

        
        path('cantiere/<int:id_cantiere>/fornitori',CantiereFornitori.as_view()),
        #path('cantiere/<int:id_cantiere>/uploadfornitori',CantiereFornitori.as_view()),

        

        path('cantiere/<int:id_cantiere>/costo',CantiereCosto.as_view()),



        path('grouparticoli', GroupArticoli.as_view()),

        path('articoli/list', ArticoliList.as_view()),
        path('articoli/create',ArticoliList.as_view()),
        path('articoli/detail/<int:pk>',ArticoliDetail.as_view()),
        path('articoli/delete/<int:pk>', ArticoliDetail.as_view()),
        path('articoli/update/<int:pk>',ArticoliDetail.as_view()),

        path('articoli/ordine/<int:id_ordine>',ArticoliOrdine.as_view()),

        path('azienda/setcurrent/<int:id_azienda>', SetCurrentAzienda.as_view()),
        path('azienda/getcurrent', CurrentAzienda.as_view()),
        path('azienda/reset', ResetAzienda.as_view()),
        path('azienda/list', AziendaList.as_view()),
        path('azienda/create',AziendaList.as_view()),
        path('azienda/detail/<int:pk>',AziendaDetail.as_view()),
        path('azienda/delete/<int:pk>', AziendaDetail.as_view()),
        path('azienda/update/<int:pk>',AziendaDetail.as_view()),

        path('cliente/getpersoc', ClientePersoc.as_view()),
        #path('cliente/listall', ClienteListAll.as_view()),
        path('cliente/list', ClienteListAll.as_view()),

        path('cliente/create',ClienteList.as_view()),
        path('cliente/detail/<int:pk>',ClienteDetail.as_view()),
        path('cliente/delete/<int:pk>', ClienteDetail.as_view()),
        path('cliente/update/<int:pk>',ClienteDetail.as_view()),

#       FATTURE CLIENTI
        path('fatturaclienticreate',ClienteFatturaCreate.as_view()),
        path('fatturaclienteupdate/<int:pk>',ClienteFatturaUpdate.as_view()),
        path('fatturecliente/list', ClienteFattureList.as_view()),
        path('fatturecliente/detail/<int:pk>',ClienteFattureDetail.as_view()),
        path('fatturecliente/delete/<int:pk>', ClienteFattureDetail.as_view()),


        #path('fatture/ordine/<int:ordine_id>', FattureOrdine.as_view()),
        #path('fatture/getTipologia', FattureGetTipologia.as_view()),
        path('fatture/list', FattureList.as_view()),
        path('fatture/create',FattureList.as_view()),
        path('fatturacreate',FatturaCreate.as_view()),
        path('fatturaupdate/<int:pk>',FatturaUpdate.as_view()),

        path('fatture/detail/<int:pk>',FattureDetail.as_view()),
        path('fatture/delete/<int:pk>', FattureDetail.as_view()),
        path('fatture/update/<int:pk>',FattureDetail.as_view()),

        path('scadenzariofatture/list', ScadenzarioFattureList.as_view()),
        path('scadenzariofatture/create',ScadenzarioFattureList.as_view()),
        path('scadenzariofatture/detail/<int:pk>',ScadenzarioFattureDetail.as_view()),
        path('scadenzariofatture/delete/<int:pk>', ScadenzarioFattureDetail.as_view()),
        path('scadenzariofatture/update/<int:pk>',ScadenzarioFattureDetail.as_view()),



        path('ordine/getTipologia', OrdineGetTipologia.as_view()),
        path('ordine/list', OrdineList.as_view()),
        path('ordine/create',OrdineList.as_view()),
        path('ordine/detail/<int:pk>',OrdineDetail.as_view()),
        path('ordine/delete/<int:pk>', OrdineDetail.as_view()),
        path('ordine/update/<int:pk>',OrdineDetail.as_view()),
        #path('ordineupdate/<int:ordine_id>',OrdineUpdate.as_view()),
        

        #path('ordine/<int:ordine_id>/articoli',ArticoliOrdine.as_view()),
        
        path('ordini/cantiere/<int:id_cantiere>',OrdiniCantiere.as_view()),
        #path('fatture/cantiere/<int:id_cantiere>',FattureCantiere.as_view()),


        

]
    
