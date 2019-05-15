from django.shortcuts import render
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.db.models import Q
from django.db.models import Sum, Max, Min, Avg

from pesquisa.models import Ata
from datetime import datetime

# Create your views here.

def relatorio(request):

    ckbitens = request.session.get('listaitens')

    atas = Ata.objects.filter(id__in=ckbitens)

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
        'datahora' : datetime.today(),
        'relatorio': True,
    }

    return render(
        request, 'relatorio.html', contexto
    )

def busca(request):
    q = request.GET.get('q')
    qc = request.GET.get('qc')
    v = request.GET.get('v')
    p = request.GET.get('p')
    e = request.GET.get('e')
    qa = request.GET.get('qa')
    resetasessao = request.GET.get('resetasessao')
    additem = request.GET.get('additem')
    delitem = request.GET.get('delitem')
    atas = Ata.objects.all()

    # Apaga os itens selecionados
    if resetasessao:
        try:
            del request.session['listaitens']
        except:
            pass

    # Recebe a sessão dos itens selecionados
    itens_selecionados_sessao = request.session.get('listaitens')

    # Caso não exista a sessão cria uma lista ou filtra os itens selecionados
    if itens_selecionados_sessao == None:
        itens_selecionados_sessao = []
        itens_selecionados = []


    # Adiciona um item a sessão
    if additem:
        if not additem in itens_selecionados_sessao:
            itens_selecionados_sessao.append(additem)
            request.session['listaitens'] = itens_selecionados_sessao

    if delitem:
        if delitem in itens_selecionados_sessao:
            nx = []
            for x in itens_selecionados_sessao:
                if not x == delitem:
                    nx.append(x)
            itens_selecionados_sessao = nx
            request.session['listaitens'] = itens_selecionados_sessao

    if request.session.has_key('listaitens'):
        itens_selecionados = Ata.objects.filter(id__in=itens_selecionados_sessao)

    # Se for solicitado filtro por tipo de ATA ('RO','T','IFRO')
    if qa:
        if qa == 'RO':
            atas = atas.filter(uf=qa)
        if qa == 'IFRO':
            atas = atas.filter(gerenciador='26421')

    # Se for solicitado filtro por descrição do catalogo
    if qc:
        qc = qc.split(' ')
        for x in qc:
            desc_catalogo = Q(desc_catalogo__icontains=x)
            atas = atas.filter(desc_catalogo)

    # Se for solicitado filtro por descrição complementar
    if q:
        q = q.split(' ')
        for x in q:
            descricao = Q(descricao_complementar_p1__icontains=x)
            descricao2 = Q(descricao_complementar_p2__icontains=x)
            atas = atas.filter(descricao | descricao2)
        # cursos = watson.filter(Curso, q)

    # Se for solicitado filtro por valor
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

    # Se for solicitado filtro por estado
    if e:
        atas = atas.filter(uf=e)

    # Tenta fazer paginação ou retorna um caso não tenha registros suficientes
    try:
        pagina = int(request.GET.get('pagina'))
    except:
        pagina = 1

    # Conta os registros e organiza a paginação
    if atas.count() == 0:
        paginador = Paginator(atas, 1)
    elif atas.count() > 200:
        paginador = Paginator(atas, 200)
    else:
        paginador = Paginator(atas, atas.count())

    pagina_atas = paginador.page(pagina)

    totalregistros = atas.count()

    # Retorna a soma dos itens unitarios
    valortotalunitario = atas.aggregate(q=Sum('valor_unitario'))
    valortotalunitario = valortotalunitario['q']

    # Retorna o menor valor entre os itens pesquisados
    menorvalor = atas.aggregate(q=Min('valor_unitario'))
    menorvalor = menorvalor['q']

    # Retorna o maior valor entre os itens pesquisados
    maiorvalor = atas.aggregate(q=Max('valor_unitario'))
    maiorvalor = maiorvalor['q']

    # Retorna a media dos valores entre os itens pesquisados
    mediavalor = atas.aggregate(q=Avg('valor_unitario'))
    mediavalor = mediavalor['q']

    contexto = {
        'titulo': 'Pesquisa ATAS',
        'pagina_atas': pagina_atas,
        'paginador': paginador,
        'totalregistros': totalregistros,
        'valortotalunitario': round(valortotalunitario,2) if valortotalunitario != None else 0,
        'menorvalor': round(menorvalor,2) if menorvalor != None else 0,
        'maiorvalor': round(maiorvalor,2) if maiorvalor != None else 0,
        'mediavalor': round(mediavalor,2) if mediavalor != None else 0,
        'itensselecionados': itens_selecionados,
        'tesitem': itens_selecionados_sessao,
        'relatorio': False,
    }

    return render(
        request, 'inicio.html', contexto
    )