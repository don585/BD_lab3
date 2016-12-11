from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from lab3.database import DB
from bson.objectid import ObjectId
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
import time

database = DB()
# Create your views here.
def index(request):
    return render(request, 'adminpage.html',{'message': request.GET.get('message', None)})


def initializeDatabase(request):
    database.initialization()
    return redirect(reverse('index')+ '?message=Database initialized')


def listView(request):
    msgs = ""
    status = ""
    if 'idBuyer' in request.GET and request.GET['idBuyer'] != '0':
        print (request.GET['idBuyer'])
        if database.status(request.GET['idBuyer']) == 0:
            status = "using cash"
        else: status = "without cash"
        start_time = time.time()
        purchaseList = database.search(request.GET['idBuyer'])
        time_res = time.time() - start_time
        msgs = str(time_res)
        print(database.status(request.GET['idBuyer']))
    else:
        purchaseList = database.getPurchaseList()

    buyers = database.getBuyer()

    paginator = Paginator(purchaseList, 25)  # Show per page
    page = request.GET.get('page')
    try:
        purchase = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        purchase = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        purchase = paginator.page(paginator.num_pages)
    return render(request, 'listpage.html', {'status': status, 'msgs': msgs, 'list': purchase,
                                              'buyers': buyers, 'total': str(len(purchaseList))})


def removePurchase(request, id):
    database.removePurchase(id)
    return redirect(reverse('index') + '?message=Removed record')


def editPurchase(request, id):
    if request.method == 'POST':
        print('asdsada')
        database.updatePurchase(id, request.POST['buyDate'], request.POST['price'], request.POST['idBook'],
                          request.POST['idJournal'], request.POST['idBuyer'])
        return redirect(reverse('index') + '?message=Changed purchase')
    journal = database.getJournal()
    book = database.getBooks()
    buyer = database.getBuyer()
    purchase = database.getPurchase(id)
    print (purchase)
    return render(request, 'editSale.html', {'buyers': buyer, 'books': book, 'journals': journal, 'purchase':
        purchase})


def addPurchase(request):
    if request.method == 'GET':
        buyers = database.getBuyer()
        books = database.getBooks()
        journals = database.getJournal()
        return render(request,'addSale.html', {'buyers': buyers, 'books':books, 'journals':journals})
    elif request.method == 'POST':
        database.savePurchase(request.POST['buyDate'], request.POST['price'], request.POST['idBook'], request.POST[
            'idJournal'], request.POST['idBuyer'])
        return redirect(reverse('index') + '?message=Added Sale')