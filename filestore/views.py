from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from .models import File, CartItem, FileLike
from theblog.models import Comment
from theblog.forms import CommentForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_save
from django.contrib import messages
import os
from .models import File
            

#download file 
@login_required
def download_file(request, file_id):
    file = get_object_or_404(File, id=file_id)

    # Check if the user has made the payment and is the author
    if request.user == file.author and file.price_paid:
        # Construct the file's absolute path
        file_path = os.path.join(settings.MEDIA_ROOT, str(file.zipped_file))
        
        # Check if the file exists
        if os.path.exists(file_path):
            # Open the file for reading in binary mode
            with open(file_path, 'rb') as f:
                response = HttpResponse(f.read(), content_type='application/force-download')
                response['Content-Disposition'] = f'attachment; filename="{file.zipped_file.name}"'
                return response
        else:
            return HttpResponse("File not found.", status=404)
    else:
        return HttpResponse("You don't have permission to access this file.", status=403)
    
    
#file detail downloads
@login_required
def file_detail(request, file_id):
    file = get_object_or_404(File, id=file_id)
    user = request.user

    # Check if the user has already added this file to their cart
    cart_item, created = CartItem.objects.get_or_create(user=user, file=file)

    context = {
        'file': file,
        'cart_item': cart_item,
    }

    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            # Increase the quantity of this item in the cart
            cart_item.quantity += 1
            cart_item.save()
            # Redirect back to the file detail page
            return redirect('file_detail', file_id=file_id)

    return render(request, 'file_detail.html', context)

#file details
def upload_file(request):
    if request.method == 'POST':
        # Get the file data from the request
        file_data = request.FILES.get('file')
        video_data = request.FILES.get('video')
        image_data = request.FILES.get('image')  

        if file_data:
            # Check the duration of the video
           
            # Create a new File object and set its properties
            new_file = File(
                author=request.user,
                title=request.POST.get('title'),
                price=request.POST.get('price'),
                description=request.POST.get('description'),
                # Set other fields accordingly
                website_url=request.POST.get('website_url'),
                whatsapp_number=request.POST.get('whatsapp_number'),
                facebook_url=request.POST.get('facebook_url'),
                location=request.POST.get('location'),
                twitter_url=request.POST.get('twitter_url'),
                playstore_url=request.POST.get('playstore_url'),
                linkedin_url=request.POST.get('linkedin_url'),
                instagram_url=request.POST.get('instagram_url'),
                pinterest_url=request.POST.get('pinterest_url'),
                youtube_url=request.POST.get('youtube_url'),
            )

            # Assign the file data to the zipped_file field
            new_file.zipped_file = file_data

            # Assign the video data to the video field
            
            # Assign the image data to the image field
            new_file.image = image_data

            new_file.save()

            # Redirect to a success page or take other actions
            return redirect(reverse('file_detail', args=[new_file.id]))

    return render(request, 'upload_file.html')



#you can delete and add items here 
@login_required
def add_to_cart(request, file_id):
    file = get_object_or_404(File, id=file_id)
    
    # Check if the item is already in the cart for the current user
    cart_item, created = CartItem.objects.get_or_create(user=request.user, file=file)
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    # Redirect the user to the cart view
    return redirect('cart_view')

#remove from cart
@login_required
def remove_from_cart(request, file_id):
    # Find the specific cart item to remove
    cart_item = get_object_or_404(CartItem, user=request.user, file_id=file_id)

    # Check if the cart item's quantity is greater than 1, then decrease the quantity
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        # If the quantity is 1 or less, remove the entire cart item
        cart_item.delete()

    # Redirect back to the cart view
    return redirect('cart_view')

#cart_view

@login_required
def cart_view(request):
    cart_items = CartItem.objects.filter(user=request.user)
    
    # Calculate the total price for each item and add it to the cart_item objects
    for item in cart_items:
        item.total_price = item.file.price * item.quantity
    
    # Calculate the overall total price by summing the individual item total prices
    total_price = sum(item.total_price for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    
    return render(request, 'cart_view.html', context)
#view my cart 
def cart(request):
    # Assuming you have a list of items in your cart
    cart_items = CartItem.objects.filter(user=request.user)  # Replace with your logic
    
    for item in cart_items:
        item.total_price = item.file.price * item.quantity
    
    return render(request, 'cart_template.html', {'cart_items': cart_items})

#likes
def like_file(request, file_id):
    file_to_like = File.objects.get(pk=file_id)
    FileLike.objects.create(user=request.user, file=file_to_like)
    return redirect('file-detail', file_id=file_id)

#notification

#view all the uplaoded files
def view_uploaded_files(request):
    # Query the database to get all File objects
    files = File.objects.all()

    context = {
        'files': files,
    }

    return render(request, 'uploaded_files.html', context)

#process the payments
def process_payment(request):
    if request.method == 'POST':
        # Retrieve cart items and calculate total price
        cart_items = CartItem.objects.filter(user=request.user)
        total_price = sum(item.total_price for item in cart_items)

        # Process payment here using PayPal API or another payment gateway
        # Handle the payment and update the order status accordingly

        # Redirect to a thank you page or order confirmation page
        return redirect('thank_you_page')  # Replace with the actual URL
    else:
        # Handle GET request or other cases as needed
        return redirect('cart')