from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect
from django.shortcuts import render_to_response
from django.template import loader
from django.core import mail
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.db import connection
from django.db.models import Count
from webshop.models import ROLES_DICT, ROLE_PLAYER, ROLE_DEVELOPER
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ObjectDoesNotExist
from webshop.models import Game, Gamestate, Transaction, Score, Profile
from django.shortcuts import get_object_or_404
from django.utils.timezone import datetime

from webshop.forms import SignUpForm, AddGameForm, UpdateGameForm

from hashlib import md5

# This page formats and sends a payment request to
# the payment service
@login_required(login_url='/login')
def transactionredirect(request, id):
    game = get_object_or_404(Game, id=id)
    customer = request.user
    # developers cannot buy own games
    if customer == game.developer:
        return redirect('product', id=id)
    # customers who already bought game cannot buy it again
    owned = request.user.game_purchases.filter(game=id)
    if owned:
        return redirect('product', id=id)
    if request.method == 'POST':
        # Create new transaction as pending. Transaction is verified if
        # payment service directs to the success page
        new_transaction = Transaction.objects.create(customer=customer, game=game, price=request.POST.__getitem__('price'), status='pending', developer=game.developer)
        new_transaction.trID = "pay{}".format(new_transaction.id) # format transaction id
        new_transaction.save()
        return render(request, 'transactionredirect.html',{'transact':new_transaction})
    else:
        return redirect('product', id=id)


# Payment service redirects here if payment was successful
@login_required(login_url='/login')
def transactionsuccess(request):
    # Check validity of the return
    if request.method == 'GET':
		secret_key = "" # Not shown in a public git repository
        check = "pid={}&ref={}&result={}&token={}".format(request.GET.__getitem__('pid'), request.GET.__getitem__('ref'), 'success', secret_key)
        m = md5(check.encode(encoding='ascii', errors='strict'))
        calcdchecksum = m.hexdigest()
        if calcdchecksum == request.GET.__getitem__('checksum'):
            # Checksum is a match
            transact = get_object_or_404(Transaction, trID=request.GET.__getitem__('pid'))
            if transact.status == 'pending':
                # Mark transaction completed
                transact.status = 'accepted'
                transact.bankreference = request.GET.__getitem__('ref')
                transact.save()

                return render(request,'transaction_success.html')
            else:
                # Return is invalid, removing transaction
                transact.delete()
                return render(request, 'error.html',{'error':'Possible request forgery blocked'})
        else:
            # return request is invalid, transaction gets removed
            transact = get_object_or_404(Transaction, trID=request.GET.__getitem__('pid'))
            transact.delete()
            return render(request, 'error.html',{'error':'Request verification failed'})
    # return request is invalid, transaction gets removed
    transact = get_object_or_404(Transaction, trID=request.GET.__getitem__('pid'))
    transact.delete()
    return render(request, 'error.html',{'error':'Invalid request'})


# Payment service redirects here if payment failed
@login_required(login_url='/login')        
def transactionfailure(request):
    # Find transaction and remove it
    transact = get_object_or_404(Transaction, trID=request.GET.__getitem__('pid'))
    transact.delete()
    return render(request,'transaction_failure.html')


# Payment service redirects here if payment was canceled
@login_required(login_url='/login')
def transactioncancel(request):
     # Find transaction and remove it
    transact = get_object_or_404(Transaction, trID=request.GET.__getitem__('pid'))
    transact.delete()
    return render(request,'transaction_cancel.html')
