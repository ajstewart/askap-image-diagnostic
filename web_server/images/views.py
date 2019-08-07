# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import redirect, reverse
from django_tables2 import RequestConfig
# from django_tables2.config import RequestConfig
from django_tables2.export.export import TableExport

# Create your views here.
from django.http import HttpResponse

from .models import Image, Processingsettings, Query, Transients
from .tables import ImageTable, CrossmatchDetailFluxTable, NearestSourceDetailFluxTable, TransientTable, TransientTableAll, CrossmatchDetailTable
from .forms import TagForm
from .filters import TransientFilter

def home(request):
    images = Image.objects.all().order_by("id")
    table = ImageTable(images)
    RequestConfig(request).configure(table)
    export_format = request.GET.get('_export', None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('images.{}'.format(export_format))
        
    try:
        hotkeys_off = request.GET["hotkeys_off"]
        request.session["hotkeys"]="false"
    except:
        pass
        
    return render(request, 'home.html', {'images': images, 'table':table})
    
def image_detail(request, pk):
    image = Image.objects.get(pk=pk)
    processing_options = Processingsettings.objects.get(image_id=pk)
    return render(request, 'image_detail.html', {'image':image, "processing_options":processing_options, "claimed_success":False, "claim_attempt":False})

def image_detail_claim(request, pk):
    user = request.user
    username = user.get_username()
    image = Image.objects.get(pk=pk)
    processing_options = Processingsettings.objects.get(image_id=pk)
    # username = request.GET['username']
    if image.claimed_by == "Unclaimed":
        image.claimed_by = username
        image.save()
        claimed_success = True
    else:
        claimed_success = False
        
    return render(request, 'image_detail.html', {'image':image, "processing_options":processing_options, "claimed_success":claimed_success, "claim_attempt":True})
    
def image_detail_reset(request, pk):
    user = request.user
    username = user.get_username()
    image = Image.objects.get(pk=pk)
    processing_options = Processingsettings.objects.get(image_id=pk)
    # username = request.GET['username']
    if user.is_staff or username == image.claimed_by:
        image.claimed_by = "Unclaimed"
        image.save()
        
    return render(request, 'image_detail.html', {'image':image, "processing_options":processing_options, "claimed_success":False, "claim_attempt":False})
    

def transients(request,pk,transient_filter):
    image = Image.objects.get(pk=pk)
    if transient_filter == "all":
        transient_sources = Transients.objects.all().filter(image_id=pk).order_by("id")
        table = TransientTableAll(transient_sources)
        total = image.transients_master_total
    elif transient_filter == "flagged":
        transient_sources = Transients.objects.all().filter(image_id=pk).exclude(pipelinetag="Candidate").filter(ratio__gte=2.0).order_by("id")
        table = TransientTable(transient_sources)
        total = image.transients_master_flagged_total
    else:
        transient_sources = Transients.objects.all().filter(image_id=pk).filter(pipelinetag="Candidate").filter(ratio__gte=2.0).order_by("id")
        table = TransientTable(transient_sources)
        total = image.transients_master_candidates_total
    RequestConfig(request, paginate={'per_page': 100}).configure(table)
    export_format = request.GET.get('_export', None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('transients_image{}.{}'.format(pk, export_format))
    return render(request, 'transients.html', {'transient_sources':transient_sources, 'image':image, "table":table, "querytype":"transients", "total":total, "view_type":transient_filter})
    
def query_queries(request):
    if request.method == "POST":
        form = TagForm(request.POST or None)
        if form.is_valid():
            data={
            "transient_type":form.cleaned_data["transient_type"],
            "user_tag":form.cleaned_data["user_tag"],
            "user":form.cleaned_data["user"]
            }
            # return render(request, 'search_results', context)
            return redirect("search_results", transient_type=data["transient_type"], user_tag=data["user_tag"], user=data["user"])
    else:
        form = TagForm(initial={'user': 'all'})
        context={"form":form}

    return render(request, 'search.html', context)
    
def search_results(request, transient_type, user_tag, user):
    transient_sources = Transients.objects.all().filter(usertag=user_tag).order_by("id")
    if user != "all":
        transient_sources = transient_sources.filter(checkedby=user)
    table = TransientTable(transient_sources)
    RequestConfig(request, paginate={'per_page': 100}).configure(table)
    friendly_type = "Transients"

    export_format = request.GET.get('_export', None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('search_results_{}_{}_{}.{}'.format(friendly_type.lower().replace(" ", "-"), user_tag, user, export_format))
        
    return render(request, "search_results.html", {"transient_type":friendly_type, "user_tag":user_tag, "table":table, "user":user})

def crossmatch_detail(request,pk,querytype,cross_id):
    object_from_query={"transients":Transients,}
    title ={"transients":"Transients",}
    html ={"transients":"transients",}
    
    allsources = object_from_query[querytype].objects.all().filter(image_id=pk)
    min_id = min(list(allsources.values_list('id', flat=True)))
    max_id = max(list(allsources.values_list('id', flat=True)))
    
    total=max_id-min_id+1
    
    prev_id = int(cross_id) - 1
    if prev_id < min_id:
        prev_id = cross_id
        
    next_id = int(cross_id) + 1
    if next_id > max_id:
        next_id = cross_id
    
    #See if we are turning on hotkeys
    try:
        hotkeys_on = request.GET["hotkeys_on"]
        request.session["hotkeys"]="true"
        return render(request, 'crossmatch_quickview.html', {"crossmatch_sources":allsources,"image":image, "querytype":querytype, "title":title_to_use, "total":total, "html":html[querytype], 
            "subquery_type":subquery_type, "transient_filter":transient_filter})
    except:
        pass
        
    try:
        hotkeys_off = request.GET["hotkeys_off"]
        request.session["hotkeys"]="false"
        return render(request, 'crossmatch_quickview.html', {"crossmatch_sources":allsources,"image":image, "querytype":querytype, "title":title_to_use, "total":total, "html":html[querytype], 
            "subquery_type":subquery_type, "transient_filter":transient_filter})
    except:
        pass
    
    #Check if a navigation hotkey has been used
    try:
        go_to = request.GET['go_to']
        the_url = request.build_absolute_uri()
        image_id = the_url.split("/")[-5]
        if go_to == "next":
            next_id = int(the_url.split("/")[-2])+1
            if next_id > max_id:
                next_id-=1
        elif go_to == "previous":
            next_id = int(the_url.split("/")[-2])-1
            if next_id < min_id:
                next_id += 1
        return redirect('crossmatch_detail', pk=image_id, querytype="transients", cross_id=next_id)
    except:
        go_to = False
    
    crossmatch_source = object_from_query[querytype].objects.get(image_id=pk, id=cross_id)
    detail_table = CrossmatchDetailTable(allsources.filter(id=cross_id))
    ratio_table = CrossmatchDetailFluxTable(allsources.filter(id=cross_id))
    image = Image.objects.get(pk=pk)
    #Also as large ratio we can fetch the nearest sources table
    nearest_sources = crossmatch_source.nearest_sources
    nearest_sources = nearest_sources.split(",")
    nearest_sources = Transients.objects.all().filter(image_id=pk, master_name__in=nearest_sources)
    nearest_sources_table = NearestSourceDetailFluxTable(nearest_sources)
    title_to_use = title[querytype]
    url_to_use = html[querytype]
    simbad_query="http://simbad.u-strasbg.fr/simbad/sim-coo?CooEpoch=2000&Coord={}d{}d&Radius.unit=arcmin&CooEqui=2000&CooFrame=FK5&Radius=10".format(crossmatch_source.ra, crossmatch_source.dec)
    ned_query="https://ned.ipac.caltech.edu/conesearch?search_type=Near%20Position%20Search&coordinates={}d%20{}d&radius=2.0&in_csys=Equatorial&in_equinox=J2000.0&out_csys=Equatorial&out_equinox=J2000.0&hconst=67.8&omegam=0.308&omegav=0.692&wmap=4&corr_z=1".format(crossmatch_source.ra, crossmatch_source.dec)
    
    #Check if an assign button has been used.
    try:
        assign = request.GET['assign']
        usertag = request.GET['usertag']
        userreason = request.GET['userreason']
        hotkey = request.GET['hotkey']
    
        user = request.user
        username = user.get_username()
    
        #Have to be logged in to submit a category and to own the image
        if not user.is_authenticated():
            return render(request, 'crossmatch_detail.html', {'crossmatch_source':crossmatch_source, 'image':image, 'type':querytype, 
                                                                'title':title_to_use, 'type_url':url_to_use, 'max_id':max_id, 'min_id':min_id, 'total':total, "saved":False, "updated":False, "conflict":False,
                                                            'simbad_query':simbad_query, 'ned_query':ned_query, 'detail_table':detail_table, "ratio_table":ratio_table, 'nearest_sources_table':nearest_sources_table},)
        else: 
            if username!=image.claimed_by:
                if user.is_staff:
                    pass
                else:
                    return render(request, 'crossmatch_detail.html', {'crossmatch_source':crossmatch_source, 'image':image, 'type':querytype, 
                                                                    'title':title_to_use, 'type_url':url_to_use, 'max_id':max_id, 'min_id':min_id, 'total':total, "saved":False, "updated":False, "conflict":False,
                                                                'simbad_query':simbad_query, 'ned_query':ned_query, 'detail_table':detail_table, "ratio_table":ratio_table, 'nearest_sources_table':nearest_sources_table},)
            
            if crossmatch_source.checkedby.lower()=="n/a":
                crossmatch_source.checkedby=username
                crossmatch_source.usertag=usertag
                crossmatch_source.userreason=userreason
                crossmatch_source.save()
                saved=True
                updated=False
                conflict=False
                image = Image.objects.get(pk=pk)
                #update image checked:
                transient_sources = Transients.objects.all().filter(image_id=pk).filter(pipelinetag="Candidate").filter(ratio__gte=2.0).exclude(checkedby="N/A")
                total_checked = len(list(transient_sources.values_list('id', flat=True)))
                image.number_candidates_checked = total_checked
                image.save()
                if hotkey=="true":
                    return redirect(reverse('crossmatch_detail', kwargs={"pk":pk, "querytype":"transients", "cross_id":next_id}) + '?hotkeyassign=true&update=false')
            elif crossmatch_source.checkedby == username:
                crossmatch_source.checkedby=username
                crossmatch_source.usertag=usertag
                crossmatch_source.userreason=userreason
                crossmatch_source.save()
                updated=True
                saved=False
                conflict = False
                image = Image.objects.get(pk=pk)
                #update image checked:
                transient_sources = Transients.objects.all().filter(image_id=pk).filter(pipelinetag="Candidate").filter(ratio__gte=2.0).exclude(checkedby="N/A")
                total_checked = len(list(transient_sources.values_list('id', flat=True)))
                image.number_candidates_checked = total_checked
                image.save()
                if hotkey=="true":
                    return redirect(reverse('crossmatch_detail', kwargs={"pk":pk, "querytype":"transients", "cross_id":next_id}) + '?hotkeyassign=true&update=true')
            else:
                if user.is_staff:
                    crossmatch_source.checkedby=username
                    crossmatch_source.usertag=usertag
                    crossmatch_source.userreason=userreason
                    crossmatch_source.save()
                    image = Image.objects.get(pk=pk)
                    #update image checked:
                    transient_sources = Transients.objects.all().filter(image_id=pk).filter(pipelinetag="Candidate").filter(ratio__gte=2.0).exclude(checkedby="N/A")
                    total_checked = len(list(transient_sources.values_list('id', flat=True)))
                    image.number_candidates_checked = total_checked
                    image.save()
                    updated=True
                    saved=False
                    conflict = False
                    if hotkey=="true":
                        return redirect(reverse('crossmatch_detail', kwargs={"pk":pk, "querytype":"transients", "cross_id":next_id}) + '?hotkeyassign=true&update=true')
                else:
                    saved=False
                    updated=False
                    conflict=True
        
    except:
        assign = False
        saved=False
        updated=False
        conflict=False
        hotkey=False

    #See if we are coming from a hotkey assign
    try:
        hotkeyassign = request.GET['hotkeyassign']
        update = request.GET["update"]
        if hotkeyassign == "true":
            if update == "true":
                hotkey_updated=True
            else:
                hotkey_updated=False
            prev_crossmatch_source = object_from_query[querytype].objects.get(image_id=pk, id=prev_id)
            hotkey_usertag = prev_crossmatch_source.usertag
            hotkey_userreason = prev_crossmatch_source.userreason
            return render(request, 'crossmatch_detail.html', {'crossmatch_source':crossmatch_source, 'image':image, 'type':querytype, 
                                                                'title':title_to_use, 'type_url':url_to_use, 'max_id':max_id, 'min_id':min_id, 'total':total, "saved":saved, "updated":updated, "conflict":conflict,
                                                            'simbad_query':simbad_query, 'ned_query':ned_query, 'detail_table':detail_table, "ratio_table":ratio_table, 'nearest_sources_table':nearest_sources_table, 
                                                            "hotkey_assign":True, "hotkey_prev_id":prev_id, "hotkey_usertag":hotkey_usertag, "hotkey_userreason":hotkey_userreason, "hotkey_updated":hotkey_updated},)
    except:
        pass


    return render(request, 'crossmatch_detail.html', {'crossmatch_source':crossmatch_source, 'image':image, 'type':querytype, 
                                                        'title':title_to_use, 'type_url':url_to_use, 'max_id':max_id, 'min_id':min_id, 'total':total, "saved":saved, "updated":updated, "conflict":conflict,
                                                    'simbad_query':simbad_query, 'ned_query':ned_query, 'detail_table':detail_table, "ratio_table":ratio_table, 'nearest_sources_table':nearest_sources_table},)


def crossmatch_quickview(request,pk,querytype,transient_filter):
    # try:
    #     type = request.GET['type']
    # except:
    #     type = "all"
    object_from_query={"transients":Transients,}
    title ={"transients":"Transient",}
    html ={"transients":"transients",}
    if querytype=="transients":
        if transient_filter=="candidates":
            allsources = object_from_query[querytype].objects.all().filter(image_id=pk).filter(ratio__gte=2.0).filter(pipelinetag="Candidate").order_by("id")
            subquery_type = "Candidate"
        elif transient_filter=="flagged":
            allsources = object_from_query[querytype].objects.all().filter(image_id=pk).filter(ratio__gte=2.0).exclude(pipelinetag="Candidate").order_by("id")
            subquery_type = "Flagged"
        else:
            allsources = object_from_query[querytype].objects.all().filter(image_id=pk).order_by("id")
            subquery_type = "All"
    image = Image.objects.get(pk=pk)
    title_to_use = title[querytype]
    total = len(list(allsources.values_list('id', flat=True)))
    return render(request, 'crossmatch_quickview.html', {"crossmatch_sources":allsources,"image":image, "querytype":querytype, "title":title_to_use, "total":total, "html":html[querytype], 
        "subquery_type":subquery_type, "transient_filter":transient_filter})

def turn_on_hotkeys(request):
    request.session['hotkeys']='true'
    
def turn_off_hotkeys(request):
    request.session['hotkeys']='false'  
    
def transient_query(request):
    transients = Transients.objects.all()
    transients_filter = TransientFilter(request.GET, queryset=transients)
    table = TransientTable(transients_filter.qs)
    
    RequestConfig(request).configure(table)
    export_format = request.GET.get('_export', None)

    if TableExport.is_valid_format(export_format):
        exporter = TableExport(export_format, table)
        return exporter.response('query_result.{}'.format(export_format))
    
    return render(request, 'transients_list.html', {'filter': transients_filter, 'table':table})
