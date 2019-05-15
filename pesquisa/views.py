from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum, Max, Min, Avg

from pesquisa.models import Ata

# Create your views here.

def relatorio(request):
    q = request.POST.get('q')
    v = request.POST.get('v')
    p = request.POST.get('p')
    e = request.POST.get('e')

    ckbitens = request.session('listaitens')

    atas = Ata.objects.filter(id__in=ckbitens)
    #for indice, valor in enumerate(ckbitens):
    #    atas = atas.objects.filter(id=ckbitens[indice])

    try:
        pagina = int(request.GET.get('pagina'))
    except:
        pagina = 1

    if atas.count() == 0:
        paginador = Paginator(atas, 1)
    elif atas.count() > 200:
        paginador = Paginator(atas, 200)
    else:
        paginador = Paginator(atas, atas.count())

    pagina_atas = paginador.page(pagina)

    totalregistros = atas.count()

    valortotalunitario = atas.aggregate(q=Sum('valor_unitario'))
    valortotalunitario = valortotalunitario['q']

    menorvalor = atas.aggregate(q=Min('valor_unitario'))
    menorvalor = menorvalor['q']

    maiorvalor = atas.aggregate(q=Max('valor_unitario'))
    maiorvalor = maiorvalor['q']

    mediavalor = atas.aggregate(q=Avg('valor_unitario'))
    mediavalor = mediavalor['q']

    contexto = {
        'titulo': 'Pesquisa ATAS',
        'pagina_atas': pagina_atas,
        'paginador': paginador,
        'totalregistros': totalregistros,
        'valortotalunitario': valortotalunitario,
        'menorvalor': menorvalor,
        'maiorvalor': maiorvalor,
        'mediavalor': mediavalor,
    }
    #contexto['cursos'] = cursos
    return render(
        request, 'relatorio.html', contexto
    )

def busca(request):
    q = request.GET.get('q')
    qc = request.GET.get('qc')
    v = request.GET.get('v')
    p = request.GET.get('p')
    e = request.GET.get('e')
    additem = request.GET.get('additem')
    atas = Ata.objects.all()

    #itemsessao = request.session.get('listaitens', additem)
    #request.session['listaitens'] = additem

    itemsessao = request.session.get('listaitens')

    if itemsessao == None:
        itemsessao = []

    if additem:
        itemsessao.append(additem)
        request.session['listaitens'] = itemsessao


    if qc:
        qc = qc.split(' ')
        for x in qc:
            desc_catalogo = Q(desc_catalogo__icontains=x)
            atas = atas.filter(desc_catalogo)

    if q:
        q = q.split(' ')
        for x in q:
            descricao = Q(descricao_complementar_p1__icontains=x)
            descricao2 = Q(descricao_complementar_p2__icontains=x)
            atas = atas.filter(descricao | descricao2)
        # cursos = watson.filter(Curso, q)

    if v:
        if p:
            linhabaixa = float(v) - (float(v) * (float(p)/100))
            linhaalta = (float(v) * ((float(p)/100)+1))
        else:
            linhabaixa = float(v) - (float(v) * 0.3)
            linhaalta = float(v) * 1.3

        valormenor = Q(valor_unitario__gte=linhabaixa)
        valoralta = Q(valor_unitario__lte=linhaalta)
        atas = atas.filter(valormenor)
        atas = atas.filter(valoralta)

        #atas = atas.filter(valor_unitario__gte=linhabaixa, valor_unitario__lte=linhaalta)

    if e:
        atas = atas.filter(uf=e)

    try:
        pagina = int(request.GET.get('pagina'))
    except:
        pagina = 1

    if atas.count() == 0:
        paginador = Paginator(atas, 1)
    elif atas.count() > 200:
        paginador = Paginator(atas, 200)
    else:
        paginador = Paginator(atas, atas.count())

    pagina_atas = paginador.page(pagina)

    totalregistros = atas.count()

    valortotalunitario = atas.aggregate(q=Sum('valor_unitario'))
    valortotalunitario = valortotalunitario['q']

    menorvalor = atas.aggregate(q=Min('valor_unitario'))
    menorvalor = menorvalor['q']

    maiorvalor = atas.aggregate(q=Max('valor_unitario'))
    maiorvalor = maiorvalor['q']

    mediavalor = atas.aggregate(q=Avg('valor_unitario'))
    mediavalor = mediavalor['q']

    contexto = {
        'titulo': 'Pesquisa ATAS',
        'pagina_atas': pagina_atas,
        'paginador': paginador,
        'totalregistros': totalregistros,
        'valortotalunitario': valortotalunitario,
        'menorvalor': menorvalor,
        'maiorvalor': maiorvalor,
        'mediavalor': mediavalor,
        'listaitens': itemsessao,
    }
    #contexto['cursos'] = cursos
    return render(
        request, 'inicio.html', contexto
    )