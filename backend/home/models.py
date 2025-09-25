from django.db import models
from django.utils.translation import gettext_lazy as _
from datetime import datetime
from django.contrib.auth.models import User
import re

class Azienda(models.Model):
    def set_path(self,filename):
            #c = Cantiere.objects.get(pk=self.cantiere_id)
            #a = c.cliente.azienda.codcf

            #albumname= re.sub('[^a-zA-Z0-9]+', '', an.nome)
            return str(self.codcf) +'/'+ filename # +albumname +'/'+filename

    nome = models.CharField(max_length=60, blank=True, null=True)
    logo = models.FileField(upload_to=set_path,null=True,blank=True)
    avatar = models.ImageField(upload_to=set_path,null=True,blank=True)
    codcf = models.CharField(max_length=60, blank=True, null=True)#,unique=True)
    #current = models.BooleanField(null=True,default=False)
    ragione_sociale = models.TextField( blank=True, null=True)
    indirizzo = models.CharField(max_length=100,blank=True, null=True)
    cap = models.CharField(max_length=20,blank=True, null=True)
    local = models.CharField(max_length=40,blank=True, null=True)
    prov = models.CharField(max_length=40,blank=True, null=True)
    codfisc = models.CharField(max_length=40,blank=True, null=True)
    partiva = models.CharField(max_length=40,blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    cellulare = models.CharField(max_length=40, blank=True, null=True)
    pec = models.CharField(max_length=60, blank=True, null=True)
    fax = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=60, blank=True, null=True)
    resprap = models.CharField(max_length=60, blank=True, null=True)
    fmemo = models.TextField( blank=True, null=True)
    nome_pf = models.CharField(max_length=40, blank=True, null=True)
    cogn_pf = models.CharField(max_length=40, blank=True, null=True)
    idfornitore = models.IntegerField(blank=True,null=True)

    def __str__(self):
        return self.nome

    class Meta:
        managed = True
        db_table = 'azienda'
    
    def get_avatar_path(self):
        return self.avatar.path
    def get_avatar_url(self):
        return self.avatar.url

class  ClientiGestioneCantieri(models.Model):
    nome = models.CharField(max_length=40, blank=True, null=True)
    cognome = models.CharField(max_length=40, blank=True, null=True)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    cellulare = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=40, blank=True, null=True)
   
    aziende =  models.ManyToManyField(Azienda,related_name="cgc_aziende")
    def __str__(self):
        return self.cognome
    class Meta:
        managed = True
        db_table = 'clientigestionecantieri'
    
    @property
    def getusers(self):
        a = self.aziende.all()
        user=set()
        for one in a:
            au = one.aziendauser.all()
            for two in au:
                user.add(two.user.username)
        #return user = Users.objects.create_user(username=username, password=password)
        return user

class AvatarUser(models.Model):
    def set_path(self,filename):
        #a=self.user.userazienda.all()

        return str(self.user.username) +'/'+ filename # +albumname +'/'+filename

    avatar = models.ImageField(upload_to=set_path,null=True,blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE,related_name='avatar_user')

    class Meta:
        managed = True
        db_table = 'avataruser'
    def __str__(self):
        return self.user.username
    def get_url(self):
        return self.avatar.url
    def get_path(self):
        return self.avatar.path
    def get_user(self): 
        return self.user.username

class UsersAzienda(models.Model):
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE,related_name='userazienda')
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='aziendauser')

    class Meta:
        managed = True
        db_table = 'usersazienda'
    

class TipologiaLavori(models.Model):
    descrizione = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.descrizione

    class Meta:
        managed = True
        db_table = 'tipologia_lavori'





#CODPAG;DESC;RATAIVA;TIPORATE;GGSCDFIX;TIPOPAG;NUMRATE;GG1RATA;GGRATE;TIPOSCAD;GGFIXANT;GGDOPOFM
class CondizioniPagamento(models.Model):
   
    codpag = models.CharField(max_length=10,unique=True)
    desc = models.CharField(max_length=70, blank=True, null=True)
    rataiva = models.IntegerField(blank=True, null=True)
    tiporate = models.CharField(max_length=2,blank=True, null=True)
    ggscdfix = models.IntegerField(blank=True, null=True)
    tipopag = models.IntegerField(blank=True, null=True)
    numrate = models.IntegerField(blank=True, null=True)
    gg1rata = models.IntegerField(blank=True, null=True)
    ggrate = models.IntegerField(blank=True, null=True)
    tiposcad = models.CharField(max_length=3, blank=True, null=True)
    ggfixant = models.CharField(max_length=3, blank=True, null=True)
    ggdopofm = models.IntegerField(blank=True, null=True)
    desc_payment_type = models.CharField(max_length=60, blank=True, null=True)
    #azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_condizionipagamento')

    def __str__(self):
        return self.desc


    class Meta:
        managed = True
        db_table = 'condizionipagamento'
    
#CLFR;CODCF;RAGSOC;RAGSOC1;INDR;CAP;LOCAL;PROV;CODFISC;PARTIVA;CODPAG;PERSOC;TEL;TEL2;FAX;EMAIL;RESPRAP;FMEMO;NOME_PF;COGN_PF;SESSO;PEC_FE;BANCA


class Fornitori(models.Model):
    
    class ClienteFornitore(models.TextChoices):
        CLIENTE = "C"
        FORNITORE = "F"
    class Sesso(models.TextChoices):
        MASCHIO='M'
        FEMMINA='F'
    class PersonaSocieta(models.TextChoices):
        Persona='P'
        Societa='S'

#    clfr = models.CharField(max_length=2, choices=ClienteFornitore.choices,
#        default=ClienteFornitore.CLIENTE, blank=True, null=True)
    codcf = models.CharField(max_length=60, blank=True, null=True)#,unique=True)
    sdi = models.CharField(max_length=20, blank=True, null=True)
    ragione_sociale = models.TextField( blank=True, null=True)
    indirizzo = models.CharField(max_length=100,blank=True, null=True)
    cap = models.CharField(max_length=20,blank=True, null=True)
    local = models.CharField(max_length=40,blank=True, null=True)
    prov = models.CharField(max_length=40,blank=True, null=True)
    codfisc = models.CharField(max_length=40,blank=True, null=True)
    partiva = models.CharField(max_length=40,blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    codpag = models.ForeignKey(CondizioniPagamento,null=True,on_delete=models.CASCADE,related_name='pppp',to_field='codpag')
    persoc = models.CharField(max_length=2,blank=True, null=True,choices=PersonaSocieta.choices)
    telefono = models.CharField(max_length=40, blank=True, null=True)
    cellulare = models.CharField(max_length=40, blank=True, null=True)
    pec_fe = models.CharField(max_length=80, blank=True, null=True)
    fax = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    resprap = models.CharField(max_length=40, blank=True, null=True)
    fmemo = models.TextField( blank=True, null=True)
    nome_pf = models.CharField(max_length=40, blank=True, null=True)
    cogn_pf = models.CharField(max_length=40, blank=True, null=True)
    sesso = models.CharField(max_length=2, blank=True, null=True,choices=Sesso.choices)
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_fornitore')

    def __str__(self):
        return self.codcf
    class Meta:
        managed = True
        db_table = 'fornitori'

#class AziendaFornitori(models.Model):

#    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='aziendafornitore')
#    fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitoriazienda')

#    class Meta:
#        managed = True
#        db_table = 'aziendafornitori'

class Sesso(models.TextChoices):
        MASCHIO='M'
        FEMMINA='F'

class BancaFornitori(models.Model):
    codfor = models.CharField(max_length=20, blank=True, null=True)
    intestat = models.CharField(max_length=80, blank=True, null=True)
    abi=  models.CharField(max_length=10, blank=True, null=True)
    cab=  models.CharField(max_length=10, blank=True, null=True)
    conto=  models.CharField(max_length=30, blank=True, null=True)
    cin=  models.CharField(max_length=10, blank=True, null=True)
    iban=  models.CharField(max_length=40, blank=True, null=True)
    indir=  models.CharField(max_length=60, blank=True, null=True)
    prov=  models.CharField(max_length=10, blank=True, null=True)
    swift=  models.CharField(max_length=30, blank=True, null=True)
    desban1=  models.CharField(max_length=40, blank=True, null=True)
    desban2=  models.CharField(max_length=30, blank=True, null=True)
    localita=  models.CharField(max_length=30, blank=True, null=True)
    cap=  models.CharField(max_length=10, blank=True, null=True)
    fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_banca')

    def __str__(self):
        return self.codfor

    class Meta:
        managed = True
        db_table = 'bancafornitori'




class Cliente(models.Model):
    class ClienteFornitore(models.TextChoices):
        CLIENTE = "C"
        FORNITORE = "F"
    
    class PersonaSocieta(models.TextChoices):
        Persona='P'
        Societa='S'

    codcf = models.CharField(max_length=60, blank=True, null=True)#,unique=True)
    sdi = models.CharField(max_length=20, blank=True, null=True)
    ragione_sociale = models.TextField( blank=True, null=True)
    indirizzo = models.CharField(max_length=100,blank=True, null=True)
    cap = models.CharField(max_length=20,blank=True, null=True)
    local = models.CharField(max_length=40,blank=True, null=True)
    prov = models.CharField(max_length=40,blank=True, null=True)
    codfisc = models.CharField(max_length=40,blank=True, null=True)
    partiva = models.CharField(max_length=40,blank=True, null=True)
    persoc = models.CharField(max_length=2,blank=True, null=True,choices=PersonaSocieta.choices)
    codpag = models.ForeignKey(CondizioniPagamento,null=True,on_delete=models.CASCADE,related_name='codpagcliente',to_field='codpag')
    telefono = models.CharField(max_length=40, blank=True, null=True)
    cellulare = models.CharField(max_length=40, blank=True, null=True)
    pec_fe = models.CharField(max_length=80, blank=True, null=True)
    fax = models.CharField(max_length=40, blank=True, null=True)
    email = models.CharField(max_length=80, blank=True, null=True)
    fmemo = models.TextField( blank=True, null=True)
    nome_pf = models.CharField(max_length=40, blank=True, null=True)
    cogn_pf = models.CharField(max_length=40, blank=True, null=True)
    sesso = models.CharField(max_length=2, blank=True, null=True,choices=Sesso.choices)
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_cliente')

    def __str__(self):
        return self.codcf

    class Meta:
        managed = True
        db_table = 'cliente'

    def getSesso(self):
        
        return getattr(self.Countries, self.name)


class BancaClienti(models.Model):
    codcli = models.CharField(max_length=20, blank=True, null=True)
    intestat = models.CharField(max_length=80, blank=True, null=True)
    abi=  models.CharField(max_length=10, blank=True, null=True)
    cab=  models.CharField(max_length=10, blank=True, null=True)
    conto=  models.CharField(max_length=30, blank=True, null=True)
    cin=  models.CharField(max_length=10, blank=True, null=True)
    iban=  models.CharField(max_length=40, blank=True, null=True)
    indir=  models.CharField(max_length=60, blank=True, null=True)
    prov=  models.CharField(max_length=10, blank=True, null=True)
    swift=  models.CharField(max_length=30, blank=True, null=True)
    desban1=  models.CharField(max_length=40, blank=True, null=True)
    desban2=  models.CharField(max_length=30, blank=True, null=True)
    localita=  models.CharField(max_length=30, blank=True, null=True)
    cap=  models.CharField(max_length=10, blank=True, null=True)
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE,related_name='clienti_banca')

    def __str__(self):
        return self.codfor

    class Meta:
        managed = True
        db_table = 'bancaclienti'

#class AziendeClienti(models.Model):
#    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda')
#    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE,related_name='cliente')

#    class Meta:
##        managed = True
#        db_table = 'aziendeclienti'

class Cantiere(models.Model):

    def set_path(self,filename):
            #c = Cantiere.objects.get(pk=self.cantiere_id)
            #a = c.cliente.azienda.codcf
            ac = self.cliente.azienda.codcf
            id = str(self.id)

            #albumname= re.sub('[^a-zA-Z0-9]+', '', an.nome)
            return ac +'/cantiere_'+ id+'/'+filename # +albumname +'/'+filename


    avatar = models.ImageField(upload_to=set_path,null=True,blank=True)
    
    nome   = models.CharField(max_length=40, blank=True, null=True)
    descrizione = models.TextField(blank=True, null=True)
    ubicazione = models.CharField(max_length=100, blank=True, null=True)
    status = models.BooleanField(null=True)
    valore_commessa =  models.FloatField(blank=True,null=True) #MoneyField( decimal_places=2, default_currency='EUR')
    data_inizio_lavori = models.DateField(blank=True, null=True)
    data_fine_lavori = models.DateField(blank=True, null=True)
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE,related_name='cliente_cantiere')

    def __str__(self):
        return self.nome
    class Meta:
        managed = True
        db_table = 'cantiere'

    def GetOrdini(self):
        ordini = self.cantiere_ordine.all()
        return ordini
    
    
    
    def GetPersonale(self):

        pers_ass = self.cantiere_assegnato.all()
        pers = []
        for one in pers_ass:
            pers.append(one.personale)
        return pers
    
    def getResponsabile(self):
        pers_ass = self.cantiere_assegnato.all()
        pers = []
        for one in pers_ass:
            if one.responsabile:
                return one.personale
            #pers.append(one.personale)
        return None

class Personale(models.Model):
    
    nome = models.CharField(max_length=40, blank=True, null=True)
    cognome = models.CharField(max_length=40, blank=True, null=True)
    tipologia_lavoro = models.ForeignKey(TipologiaLavori,null=True,on_delete=models.CASCADE,related_name='tipolavoro_personale')
    responsabile = models.BooleanField(null=False,default=False)
    
    wage_lordo =  models.FloatField(blank=True,null=True) 
    wage_netto =  models.FloatField(blank=True,null=True) 

    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_personale')
    
    def __str__(self):
        return self.cognome
    
    class Meta:
        managed = True
        db_table = 'personale'

class TipologiaDocumenti(models.Model):
    descrizione = models.CharField(max_length=220, blank=True, null=True)
    def __str__(self):
            return self.descrizione
    
    class Meta:
        managed = True
        db_table = 'tipologiadocumenti'

class Documenti(models.Model):
        """
        class TipologiaDocumento(models.TextChoices):
            SERVIZIO = "SE",_("Servizio")
            MATERIALE = "MA",_("Materiale")
            MACCHINARI = "NO",_("Noleggio")
            ALTRO = "AL",_("Altro")
        """
        def set_path(self,filename):
            c = Cantiere.objects.get(pk=self.cantiere_id)
            
            a = c.cliente.azienda.codcf
        
            nome = re.sub(r'\W+', '', c.nome)

            #albumname= re.sub('[^a-zA-Z0-9]+', '', an.nome)
            return str(a) +'/'+ nome +'/'+ filename # +albumname +'/'+filename
        
        data_inserimento = models.DateField(blank=True, null=True,auto_now_add=True)
        cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_documenti')
        #tipologia = models.CharField(max_length=80, blank=True, null=True)
        media = models.FileField(upload_to=set_path,null=True,blank=True)
        caricato_da =  models.CharField(max_length=80, blank=True, null=True)
        tipologia = models.ForeignKey(TipologiaDocumenti,null=True,on_delete=models.CASCADE,related_name='tipologia_documento')
        
        #def __str__(self):
        #    return self.media.path
    
        class Meta:
            managed = True
            db_table = 'documenti'
        @property
        def get_media_path(self):
            return self.media.path
        def get_media_url(self):
            return self.media.url
        def get_cantiere(self):
            return self.cantiere.nome
        def get_azienda(self):
            return self.cantiere.cliente.azienda.codcf
        

class DocumentiFornitori(models.Model):
        
        def set_path(self,filename):
            c = Cantiere.objects.get(pk=self.cantiere_id)
            
            a = c.cliente.azienda.codcf
        
            nome = re.sub(r'\W+', '', c.nome)
            nome_fornitore = self.fornitore.codcf

            #albumname= re.sub('[^a-zA-Z0-9]+', '', an.nome)
            return str(a) +'/'+ nome +'/'+ nome_fornitore + "/"+ filename # +albumname +'/'+filename
        
        data_inserimento = models.DateField(blank=True, null=True,auto_now_add=True)
        cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_documentifornitori')
        #tipologia = models.CharField(max_length=80, blank=True, null=True)
        media = models.FileField(upload_to=set_path,null=True,blank=True)
        caricato_da =  models.CharField(max_length=80, blank=True, null=True)
        #tipologia =  models.CharField(max_length=220, blank=True, null=True)
        tipologia = models.ForeignKey(TipologiaDocumenti,null=True,on_delete=models.CASCADE,related_name='tipologia_documentofornitore')

        note  =  models.CharField(max_length=200, blank=True, null=True)

        fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitore_documentofornitore')
        
        #def __str__(self):
        #    return self.media.path
    
        class Meta:
            managed = True
            db_table = 'documentifornitori'
        @property
        def get_media_path(self):
            return self.media.path
        def get_media_url(self):
            return self.media.url
        def get_cantiere(self):
            return self.cantiere.nome
        def get_azienda(self):
            return self.cantiere.cliente.azienda.codcf
 


class Assegnato_Cantiere(models.Model):
        personale = models.ForeignKey(Personale,null=True,on_delete=models.CASCADE,related_name='personale_assegnato')
        cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_assegnato')
        responsabile = models.BooleanField(null=False,default=False)
        ore_lavorate =  models.FloatField(blank=True,null=True) 

        class Meta:
            unique_together = ('personale', 'cantiere')
            managed = True
            db_table = 'assegnato_cantiere'


class Ordine(models.Model):
    class TipologiaFornitore(models.TextChoices):
        SERVIZIO = "SE",_("Servizio")
        MATERIALE = "MA",_("Materiale")
        MACCHINARI = "NO",_("Noleggio")
        ALTRO = "AL",_("Altro")
    completato = models.BooleanField(null=False,default=False)
    data_ordine = models.DateField(blank=True, null=True)
    data_consegna= models.DateField(blank=True, null=True)
    importo = models.FloatField(blank=True,null=True,default=0.0) 
    fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitori_ordine')
    cantiere = models.ForeignKey(Cantiere,null=True,on_delete=models.CASCADE,related_name='cantiere_ordine')
    damagazzino = models.BooleanField(null=False,default=False)
    permagazzino = models.BooleanField(null=False,default=False)
    tipologia = models.CharField(max_length=2, choices=TipologiaFornitore.choices,default=TipologiaFornitore.MATERIALE, blank=True, null=True)
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_ordine')

    def __str__(self):
        return "aaa"
    
    class Meta:
        managed = True
        db_table = 'ordine'




class Articoli(models.Model):
    descrizione = models.TextField(blank=True, null=True)
    quantita = models.IntegerField(blank=True, null=True,default=0)

    prezzo_unitario =  models.FloatField(blank=True,null=True,default=0.0)
    importo_totale = models.FloatField(blank=True,null=True,default=0.0) #MoneyField( decimal_places=2, default_currency='EUR')
    ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_articoli')
    #magazzino = models.BooleanField(null=False,default=False)

    def __str__(self):
        return self.descrizione
    
    class Meta:
        managed = True
        db_table = 'articoli'

class Magazzino(models.Model):
    quantita_impegnata = models.IntegerField(blank=True, null=True,default=0)
    quantita_inarrivo = models.IntegerField(blank=True, null=True,default=0)
    quantita = models.IntegerField(blank=True, null=True,default=0)
    descrizione = models.TextField(blank=True, null=True)
    prezzo_unitario = models.FloatField(blank=True,null=True,default=0.0)
    importo_totale = models.FloatField(blank=True,null=True,default=0.0) 
    #ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_magazzino')
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_magazzino')

    class Meta:
        managed = True
        db_table = 'magazzino'
    
    
    
class TipologiaFattura(models.TextChoices):
        SERVIZIO = "SE",_("Servizio")
        MATERIALE = "MA",_("Materiale")
        MACCHINARI = "NO",_("Noleggio")
        ALTRO = "AL",_("Altro")

class Fatture(models.Model):
    #ragione_sociale = models.CharField(max_length=100, blank=True, null=True)
    n_fattura = models.CharField(db_column='n_fattura', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_fattura = models.DateField(blank=True, null=True)
    importo =  models.FloatField(blank=True,null=True)#MoneyField( decimal_places=2, default_currency='EUR')
    pagato =   models.FloatField(blank=True,null=True)#MoneyField( decimal_places=2, default_currency='EUR')
    data_scadenza = models.DateField(blank=True, null=True)
    #ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_fatture')
    fornitore = models.ForeignKey(Fornitori,null=True,on_delete=models.CASCADE,related_name='fornitore_fatture')
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_fatture')
    tipologiapagamento =  models.IntegerField(blank=True, null=True) 
    codpag = models.ForeignKey(CondizioniPagamento,null=True,on_delete=models.CASCADE,related_name='condizionipagamento_fattura')


    def __str__(self):
        return self.fornitore.ragione_sociale

    class Meta:
        managed = True
        db_table = 'fatture'


class FattureCliente(models.Model):
    #ragione_sociale = models.CharField(max_length=100, blank=True, null=True)
    n_fattura = models.CharField(db_column='n_fattura', max_length=40, blank=True, null=True)  # Field renamed to remove unsuitable characters.
    data_fattura = models.DateField(blank=True, null=True)
    importo =  models.FloatField(blank=True,null=True)#MoneyField( decimal_places=2, default_currency='EUR')
    pagato =   models.FloatField(blank=True,null=True)#MoneyField( decimal_places=2, default_currency='EUR')
    data_scadenza = models.DateField(blank=True, null=True)
    #ordine = models.ForeignKey(Ordine,null=True,on_delete=models.CASCADE,related_name='ordine_fatture')
    cliente = models.ForeignKey(Cliente,null=True,on_delete=models.CASCADE,related_name='cliente_fatturecliente')
    azienda = models.ForeignKey(Azienda,null=True,on_delete=models.CASCADE,related_name='azienda_fatturecliente')
    tipologiapagamento =  models.IntegerField(blank=True, null=True) 
    codpag = models.ForeignKey(CondizioniPagamento,null=True,on_delete=models.CASCADE,related_name='condizionipagamento_fatturacliente')


    def __str__(self):
        return self.cliente.ragione_sociale

    class Meta:
        managed = True
        db_table = 'fatturecliente'


class ScadenzarioFattureCliente(models.Model):
    importo_rata =models.FloatField(blank=True,null=True) 
    scadenza_rata = models.DateField(blank=True, null=True)
    importo_pagato = models.FloatField(blank=True,null=True) 
    data_pagamento = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False,blank=True,null=True)
    fatturacliente = models.ForeignKey(FattureCliente,null=True,on_delete=models.CASCADE,related_name='fatturecliente_scadenzario')

    class Meta:
        managed = True
        db_table = 'scadenzariofatturecliente'

class ScadenzarioFatture(models.Model):
    importo_rata =models.FloatField(blank=True,null=True) 
    scadenza_rata = models.DateField(blank=True, null=True)
    importo_pagato = models.FloatField(blank=True,null=True) 
    data_pagamento = models.DateField(blank=True, null=True)
    status = models.BooleanField(default=False,blank=True,null=True)
    fattura = models.ForeignKey(Fatture,null=True,on_delete=models.CASCADE,related_name='fatture_scadenzario')

    class Meta:
        managed = True
        db_table = 'scadenzariofatture'
#tabella scadenze
#importo rata scadenza 

class SyncLog(models.Model):
        data = models.DateTimeField(blank=True, null=True,default=datetime.now )#auto_now_add=True)
        tabella = models.CharField(db_column='tabella', max_length=40, blank=True, null=True)  
        operazione = models.CharField( max_length=40, blank=True, null=True)  
        uniquefield = models.CharField( max_length=40, blank=True, null=True)  
        fieldvalue =  models.CharField( max_length=40, blank=True, null=True)  
        azienda =  models.IntegerField(blank=True, null=True) 
        
        class Meta:
            managed = True
            db_table = 'synclog'

class SyncDataFiles(models.Model):
        data = models.DateTimeField(blank=True, null=True,default=datetime.now )#auto_now_add=True)
        json_delete = models.JSONField(blank=True, null=True)
        json_add = models.JSONField(blank=True, null=True)
        json_update = models.JSONField(blank=True, null=True)
        tabella = models.CharField(db_column='tabella', max_length=40, blank=True, null=True)  

        class Meta:
            managed = True
            db_table = 'syncdatafiles'





