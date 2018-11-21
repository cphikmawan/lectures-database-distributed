from django.shortcuts import render, redirect
from humans.models import Humans
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@csrf_exempt
def index(request):
    if request.method == 'POST':
        sr_no = request.POST['sr_no']
        refund = request.POST['refund']
        m_status = request.POST['m_status']
        income = request.POST['income']
        cheat = request.POST['cheat']

        human = Humans(sr_no=sr_no)
        human.refund = refund
        human.m_status = m_status
        human.income = income
        human.cheat = cheat
        human.save()

    humans = Humans.objects.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(humans, 5)
    try:
        humans = paginator.page(page)
    except PageNotAnInteger:
        humans = paginator.page(1)
    except EmptyPage:
        humans = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'humans': humans})

def add(request):
    return render(request, 'add.html')

def edit(request, sr_no):
    human = Humans.objects.get(pk=sr_no)

    if request.method == "POST":
        human.refund = request.POST['refund']
        human.m_status = request.POST['m_status']
        human.income = request.POST['income']
        human.cheat = request.POST['cheat']
        human.save()
        return redirect('/')

    return render(request, 'edit.html', {'human': human})

def delete(request, sr_no):
    human = Humans.objects.get(pk=sr_no)
    human.delete()
    return redirect('/')