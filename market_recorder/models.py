from django.db import models

# Create your models here.
class MarketData(models.Model):
    market_pair = models.CharField(max_length=50)
    last_price = models.DecimalField(max_digits=10, decimal_places=2)
    price_change = models.DecimalField(max_digits=10, decimal_places=2)
    recorded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.market_pair
    
    class Meta:
        app_label = 'market_recorder'
    
class Order(models.Model):
    market_data = models.ForeignKey(MarketData, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate the total based on price and amount
        self.total = self.price * self.amount
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return f"Order for {self.market_data.market_pair}"

class Transaction(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transaction at {self.timestamp}"

class MarketDepth(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Market Depth at Price {self.price}"
    
class Trade(models.Model):
    buy_or_sell_choices = [
        ('buy', 'Buy'),
        ('sell', 'Sell'),
    ]

    price = models.DecimalField(max_digits=10, decimal_places=2)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, editable=False)
    available_price = models.DecimalField(max_digits=10, decimal_places=2)
    volume = models.DecimalField(max_digits=10, decimal_places=2)
    margin = models.DecimalField(max_digits=10, decimal_places=2)
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    buy_or_sell = models.CharField(max_length=4, choices=buy_or_sell_choices)
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        self.percentage = ((self.price - self.available_price) / self.available_price) * 100
        super(Trade, self).save(*args, **kwargs)

    def __str__(self):
        return f"Trade {self.id}"