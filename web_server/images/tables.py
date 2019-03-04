#!/usr/bin/env python

import django_tables2 as tables
from .models import Image, Sumssnomatch, Largeratio, Goodmatch, Askapnotseen
from django_tables2.utils import A
from templatetags import units

class RAColumn(tables.Column):
    def render(self, value):
        return units.deg_to_hms(value)

class DecColumn(tables.Column):
    def render(self, value):
        return units.deg_to_dms(value)

class ImageTable(tables.Table):
    image_id = tables.Column(verbose_name= 'ID')
    name = tables.LinkColumn('image_detail', args=[A('pk')], orderable=True,)
    ra = RAColumn(attrs={"td":{"style":"white-space:nowrap;"}}, verbose_name= 'RA' )
    dec = DecColumn(attrs={"td":{"style":"white-space:nowrap;"}}, verbose_name= 'Dec')
    number_askap_sources = tables.Column(verbose_name= '# ASKAP Sources')
    number_sumss_sources = tables.Column(verbose_name= '# SUMSS Sources')
    runby = tables.Column(verbose_name= 'Run By')
    class Meta:
        model = Image
        template_name = 'django_tables2/bootstrap-responsive.html'
        fields = ("image_id", "name", "description", "ra", "dec", "number_askap_sources", "number_sumss_sources", "runtime", "runby" )
        attrs = {"th":{"bgcolor":"#EBEDEF"}}
        
        
class SumssNoMatchListTable(tables.Table):
    match_id = tables.Column(verbose_name= 'ID')
    sumss_name = tables.LinkColumn('crossmatch_detail', args=[A('image_id'), "noaskapmatchtosumss", A('match_id')], orderable=True, verbose_name= 'SUMSS Name')
    ra = RAColumn(attrs={"td":{"style":"white-space:nowrap;"}}, verbose_name= 'RA' )
    dec = DecColumn(attrs={"td":{"style":"white-space:nowrap;"}}, verbose_name= 'Dec')
    sumss_snr = tables.Column(verbose_name= 'SUMSS SNR')
    pipelinetag = tables.Column(verbose_name= 'Pipeline Tag')
    usertag = tables.Column(verbose_name= 'User Tag')
    userreason = tables.Column(verbose_name= 'User Reason')
    checkedby = tables.Column(verbose_name= 'Checked By')
    class Meta:
        model = Sumssnomatch
        template_name = 'django_tables2/bootstrap4.html'
        fields = ("match_id", "sumss_name", "ra", "dec", "sumss_snr", "pipelinetag", "usertag", "userreason", "checkedby")
        attrs = {"th":{"bgcolor":"#EBEDEF"}}
    
class LargeRatioListTable(tables.Table):
    match_id = tables.Column(verbose_name= 'ID')
    sumss_name = tables.LinkColumn('crossmatch_detail', args=[A('image_id'), "largeratio", A('match_id')], orderable=True, verbose_name= 'SUMSS Name')
    ra = RAColumn(attrs={"td":{"style":"white-space:nowrap;"}}, verbose_name= 'RA' )
    dec = DecColumn(attrs={"td":{"style":"white-space:nowrap;"}}, verbose_name= 'Dec')
    sumss_snr = tables.Column(verbose_name= 'SUMSS SNR')
    pipelinetag = tables.Column(verbose_name= 'Pipeline Tag')
    usertag = tables.Column(verbose_name= 'User Tag')
    userreason = tables.Column(verbose_name= 'User Reason')
    checkedby = tables.Column(verbose_name= 'Checked By')
    class Meta:
        model = Largeratio
        template_name = 'django_tables2/bootstrap4.html'
        fields = ("match_id", "sumss_name", "ra", "dec", "sumss_snr", "pipelinetag", "usertag", "userreason", "checkedby")
        attrs = {"th":{"bgcolor":"#EBEDEF"}}   
        
class GoodMatchListTable(tables.Table):
    match_id = tables.Column(verbose_name= 'ID')
    sumss_name = tables.LinkColumn('crossmatch_detail', args=[A('image_id'), "goodmatch", A('match_id')], orderable=True, verbose_name= 'SUMSS Name')
    ra = RAColumn(attrs={"td":{"style":"white-space:nowrap;"}}, verbose_name= 'RA' )
    dec = DecColumn(attrs={"td":{"style":"white-space:nowrap;"}}, verbose_name= 'Dec')
    sumss_snr = tables.Column(verbose_name= 'SUMSS SNR')
    pipelinetag = tables.Column(verbose_name= 'Pipeline Tag')
    usertag = tables.Column(verbose_name= 'User Tag')
    userreason = tables.Column(verbose_name= 'User Reason')
    checkedby = tables.Column(verbose_name= 'Checked By')
    class Meta:
        model = Goodmatch
        template_name = 'django_tables2/bootstrap4.html'
        fields = ("match_id", "sumss_name", "ra", "dec", "sumss_snr", "pipelinetag", "usertag", "userreason", "checkedby")
        attrs = {"th":{"bgcolor":"#EBEDEF"}}   
        
class AskapNotSeenListTable(tables.Table):
    match_id = tables.Column(verbose_name= 'ID')
    askap_name = tables.LinkColumn('crossmatch_detail', args=[A('image_id'), "nosumssmatchtoaskap", A('match_id')], orderable=True, verbose_name= 'ASKAP Name')
    ra = RAColumn(attrs={"td":{"style":"white-space:nowrap;"}}, verbose_name= 'RA' )
    dec = DecColumn(attrs={"td":{"style":"white-space:nowrap;"}}, verbose_name= 'Dec')
    sumss_snr = tables.Column(verbose_name= 'SUMSS SNR')
    pipelinetag = tables.Column(verbose_name= 'Pipeline Tag')
    usertag = tables.Column(verbose_name= 'User Tag')
    userreason = tables.Column(verbose_name= 'User Reason')
    checkedby = tables.Column(verbose_name= 'Checked By')
    class Meta:
        model = Askapnotseen
        template_name = 'django_tables2/bootstrap4.html'
        fields = ("match_id", "askap_name", "ra", "dec", "sumss_snr", "pipelinetag", "usertag", "userreason", "checkedby")
        attrs = {"th":{"bgcolor":"#EBEDEF"}}   
    
    
    
    
    
    # image_id = models.IntegerField()
    # match_id = models.IntegerField()
    # sumss_name = models.CharField(max_length=50, unique=False, default="sumss source")
    # ra = models.DecimalField(max_digits=10, decimal_places=7)
    # dec = models.DecimalField(max_digits=10, decimal_places=7)
    # sumss_iflux = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    # sumss_iflux_e = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    # askap_iflux = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    # askap_iflux_e = models.DecimalField(max_digits=20, decimal_places=3, default=0)
    # sumss_snr = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    # ploturl = models.CharField(max_length=200, unique=False, default="plot")
    # pipelinetag = models.CharField(max_length=30, unique=False, default="N/A")
    # usertag = models.CharField(max_length=30, unique=False, default="N/A")
    # checkedby = models.CharField(max_length=20, unique=False, default="N/A")

