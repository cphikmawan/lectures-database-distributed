from django.shortcuts import render, redirect
from myapp.models import Quotes
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@csrf_exempt
def index(request):
    if request.method == 'POST':
        Auther = request.POST['Auther']
        textquote = request.POST['quote'] 
        quote = Quotes(Auther=Auther)
        quote.quote = textquote
        quote.save()
    quotes = Quotes.objects
    page = request.GET.get('page', 1)

    paginator = Paginator(quotes, 5)
    try:
        quotes = paginator.page(page)
    except PageNotAnInteger:
        quotes = paginator.page(1)
    except EmptyPage:
        quotes = paginator.page(paginator.num_pages)

    return render(request, 'index.html', {'quotes': quotes})

def add(request):
    return render(request, 'add.html')

def edit(request, id):
    quote = Quotes.objects.get(pk=id)

    if request.method == "POST":
        quote.Auther = request.POST['Auther']
        quote.quote = request.POST['quote']
        quote.save()
        return redirect('/')

    return render(request, 'edit.html', {'quote': quote})

def delete(request, id):
    quote = Quotes.objects.get(pk=id)
    quote.delete()
    return redirect('/')