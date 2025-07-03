from django.shortcuts import render
# Create your views here.
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from .models import Order, Transaction, MarketDepth, Trade

class OrderCreateView(CreateView):
    model = Order
    fields = ['market_data', 'price', 'amount']
    template_name = 'order_create.html'
    success_url = reverse_lazy('order_list')

class OrderListView(ListView):
    model = Order
    template_name = 'order_list.html'
    context_object_name = 'orders'

def calculate_winnings_losses(request):
    transactions = Transaction.objects.all()
    total_investment = transactions.aggregate(Sum('price'))['price__sum']
    total_amount = transactions.aggregate(Sum('amount'))['amount__sum']
    total_winnings_losses = total_investment - (total_amount * Transaction.objects.latest('timestamp').price)

    context = {
        'total_investment': total_investment,
        'total_amount': total_amount,
        'total_winnings_losses': total_winnings_losses,
    }

    return render(request, 'winnings_losses.html', context)

class TransactionCreateView(CreateView):
    model = Transaction
    fields = ['price', 'amount']
    template_name = 'transaction_create.html'
    success_url = '/winnings_losses/calculate/'

class TransactionListView(ListView):
    model = Transaction
    template_name = 'transaction_list.html'
    context_object_name = 'transactions'

class MarketDepthListView(ListView):
    model = MarketDepth
    template_name = 'market_depth_list.html'
    context_object_name = 'market_depth'


class TradeCreateView(CreateView):
    model = Trade
    fields = ['price', 'amount', 'available_price', 'volume', 'margin', 'fee', 'buy_or_sell']
    template_name = 'trade_create.html'
    success_url = reverse_lazy('trade_list')