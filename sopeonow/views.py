from datetime import datetime
from django.shortcuts import render, get_object_or_404, redirect
from .models import Inventory, Order, Transaction
from .forms import SellItemForm, CreateItemForm
from django.db.models import F, Sum
from django.contrib import messages

now = datetime.now()
def home(request):
    totalProfit = sum(item.calculate_profit() for item in Inventory.objects.all())
    
    totalItemsStock = sum(item.quantity for item in Inventory.objects.all())

    highestCostItem = Inventory.objects.order_by('-cost').first()
    
    highestProfitsItem = Inventory.objects.annotate(
        profit=F('selling_price') - F('cost')
    ).order_by('-profit').first()
    
    mostSoldItem = Inventory.objects.annotate(
        sold=Sum('transaction__quantity')
    ).order_by('-sold').first()
    
    outOfStock = Inventory.objects.filter(quantity=0)
  
    # highestProfitItem = Inventory.objects.annotate(
    #     profit_earned=Sum('transaction__selling_price') - Sum('transaction__cost')
    # ).order_by('-profit_earned').first()
    
    context = {
        'totalProfit': totalProfit,
        'totalItemsStock': totalItemsStock,
        'highestCostItem': highestCostItem,
        'highestProfitsItem': highestProfitsItem,
        'mostSoldItem': mostSoldItem,
        'outOfStock': outOfStock,
        # 'highestProfitItem': highestProfitItem,
    }        
    return render(request,'home.html',context)

def itemList(request):
    items = Inventory.objects.all()
    return render(request, 'itemList.html', {'items': items})

def allOrders(request):
    items = Order.objects.all()
    return render(request, 'allOrders.html', {'items': items})

def allTransactions(request):
    items = Transaction.objects.all()
    return render(request, 'allTransactions.html', {'items': items})

def sellItem(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    if request.method == 'POST':
        form = SellItemForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data['quantity']
            selling_price = form.cleaned_data['selling_price']
            
            if quantity > 0 and selling_price//quantity >= item.cost*2 and quantity+item.quantity_sold < item.quantity:
                item.quantity_sold += quantity
                item.quantity -= quantity
                item.save()
                
                transaction = Transaction(item=item,name=item.name, quantity=quantity, selling_price=selling_price,transactiondttm=now)
                transaction.save()
                
                return redirect('itemDetails', item_id=item.id)
            elif selling_price//quantity < item.cost*2:
                form.add_error('selling_price', 'selling_price cannot be less than cost.')
                messages.info(request,'selling price cannot be less than double of cost.')
            else:
                form.add_error('quantity', 'Quantity sold cannot be more than available stock.')
                messages.info(request,'Quantity sold cannot be more than available stock.')
    else:
        form = SellItemForm()
    
    return render(request, 'sellItem.html', {'item': item, 'form': form})

def createItem(request):
    if request.method == 'POST':
        form = CreateItemForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('itemList')
    else:
        form = CreateItemForm()
    
    return render(request, 'createItem.html', {'form': form,'titleName':"Create"})

def itemDetails(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    
    if request.method == 'POST':
        new_quantity = int(request.POST.get('new_quantity'))
        if new_quantity > 0:
            # item.quantity += new_quantity
            item.save()
            order = Order(item=item,name=item.name, quantity=new_quantity, cost=item.cost,orderdttm=now)
            order.save()           
        return redirect('itemDetails', item_id=item.id)
    return render(request, 'itemDetails.html', {'item': item})

def edit_item(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    
    if request.method == 'POST':
        form = CreateItemForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            return redirect('itemDetails', item_id=item.id)
    else:
        form = CreateItemForm(instance=item)
    
    return render(request, 'createItem.html', {'item': item, 'form': form,'titleName':"Edit"})

def orders_placed(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    orders = Order.objects.filter(item=item, is_received=False, is_cancel=False)
    return render(request, 'orders_placed.html', {'item': item, 'orders': orders})

def orders_received(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    orders = Order.objects.filter(item=item, is_received=True)
    return render(request, 'orders_received.html', {'item': item, 'orders': orders})

def orders_canceled(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    orders = Order.objects.filter(item=item, is_cancel=True)
    return render(request, 'orders_canceled.html', {'item': item, 'orders': orders})

def item_transactions(request, item_id):
    item = get_object_or_404(Inventory, pk=item_id)
    transactions = Transaction.objects.filter(item=item)
    
    return render(request, 'item_transactions.html', {'item': item, 'transactions': transactions})

def confirm_received(request, order_id,new_quantity):
    order = get_object_or_404(Order, pk=order_id)
    item = order.item
    if new_quantity > 0:
        item.quantity += new_quantity
        item.save()
    order.is_received = True
    order.save()
    return redirect('orders_placed', item_id=item.id)
    
def confirm_canceled(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.is_cancel = True
    order.save()
    return redirect('orders_placed', item_id=order.item.id)
