from django.urls import path, include
from .views import TransactionCreateView, TransactionListView, MarketDepthListView, OrderCreateView, OrderListView,  calculate_winnings_losses, TradeCreateView

urlpatterns = [
    path('create/', OrderCreateView.as_view(), name='order_create'),
    path('list/', OrderListView.as_view(), name='order_list'),
    path('create/', TransactionCreateView.as_view(), name='transaction_create'),
    path('list/', TransactionListView.as_view(), name='transaction_list'),
    path('calculate/', calculate_winnings_losses, name='calculate_winnings_losses'),
    path('market_depth/', MarketDepthListView.as_view(), name='market_depth_list'),
    path('create/', TradeCreateView.as_view(), name='trade_create'),
]

