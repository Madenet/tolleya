from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from django.http import Http404
from django.views.generic import DetailView, CreateView, UpdateView, DeleteView, ListView, CreateView
from .models import Post, Comment, Notification, UserProfile, PostActivity, TradingActivity
#from marketoverview.models import TradingActivity
from django.views.generic import TemplateView
from photo.models import Photo, Category
from .forms import PostForm, EditForm, CommentForm, PostSearchForm 
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.utils import timezone
from django.db.models import Sum
#from market_recorder
from django.core.exceptions import ObjectDoesNotExist  
from market_recorder.views import TransactionCreateView, MarketDepthListView, TransactionListView, TradeCreateView, OrderCreateView, OrderListView
from market_recorder.models import Transaction, MarketDepth, Trade, Order, MarketData
#end
#filestore
from filestore.models import File
#login required 
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
#view defined
from django.views import View
from django.core.mail import send_mail
#csrf token for email lock
from django.views.decorators.csrf import csrf_protect
from django.conf import settings 
# Modify your HomeView
class HomeView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'social/home.html'
    context_object_name = 'posts'
    ordering = ['-post_date']

    def get_queryset(self):
        user = self.request.user

        if user.is_superuser:
            # If the user is a superuser, return all posts
            return Post.objects.all()
        else:
            # Get authors that the user is following
            followed_authors = user.profile.followers.all()
            
            # Get posts from followed authors
            queryset = Post.objects.filter(author__in=followed_authors)
            
            return queryset
    #calcultating winning and loses on my homeview
    def calculate_winnings_losses(self):
        transactions = Transaction.objects.all()
        total_investment = transactions.aggregate(Sum('price'))['price__sum']
        total_amount = transactions.aggregate(Sum('amount'))['amount__sum']
        
        try:
            latest_transaction_price = Transaction.objects.latest('timestamp').price
        except ObjectDoesNotExist:
            latest_transaction_price = 0  # Provide a default value (0 in this case)

        total_winnings_losses = total_investment - (total_amount * latest_transaction_price)

        return {
            'total_investment': total_investment,
            'total_amount': total_amount,
            'total_winnings_losses': total_winnings_losses,
        }

    def get_custom_buttons(self, user):
        return CustomButton.objects.filter(user=user)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #market watch data here: 
        order_create_view = OrderCreateView(model=Order())  # Pass an empty Order instance
        order_list_view = OrderListView(model=Order())
        # Get the most recent broker and photo for the user
        #context to calculate wins and losses
        # Calculate winnings and losses and include them in the context
        photos = Photo.objects.all()
        #end
        activity_id = self.request.GET.get('activity_id')
        recently_added_photo = Photo.objects.filter(author=self.request.user).order_by('-upload_date').first()
        
        custom_buttons = self.get_custom_buttons(self.request.user)
        # Get instances of the File model to display in the template
        files = File.objects.order_by('-upload_date').all()
        # Include the TransactionCreateView, TransactionListView,
        # MarketDepthListView, and TradeCreateView instances in the context
        transaction_create_view = TransactionCreateView(model=Transaction())
        transaction_list_view = TransactionListView(model=Transaction())
        market_depth_list_view = MarketDepthListView(model=MarketDepth())
        trade_create_view = TradeCreateView(model=Trade())
        # Get the user's profile data
        user_profile = UserProfile.objects.get(user=self.request.user)
        #activity_list_url = reverse('activity_list')
        # Add trading activities to the context
        trading_activities = TradingActivity.objects.filter(user=self.request.user)
        recent_trading_activities = trading_activities.order_by('-due_date')  # Order by due_date descending
        context['trading_activities'] = recent_trading_activities
        context['activity_id'] = activity_id
        #context['activity_list_url'] = activity_list_url
        #market watch context
        # Now include the ProfileView data
        
        context['order_create_view'] = order_create_view
        context['order_list_view'] = order_list_view
        context['transaction_create_view'] = transaction_create_view
        context['transaction_list_view'] = transaction_list_view
        context['market_depth_list_view'] = market_depth_list_view
        context['trade_create_view'] = trade_create_view
        #end
        context['photos'] = photos
        context['recently_added_broker'] = recently_added_broker
        context['recently_added_photo'] = recently_added_photo
        context['custom_buttons'] = custom_buttons
        context['files'] = files
        context['user_profile'] = user_profile  # Pass the user's profile to the context
        context['view_uploaded_files_url'] = reverse('view_uploaded_files')
        
        return context
#my external redirect urls

def external_redirect(request, url):
    return redirect(url)

#post list views
class PostListView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
        ).order_by('-created_on')
        form = PostForm()

        context = {
            'post_list': posts,
            'form': form,
        }
        
        return render(request, 'social/post_list.html', context)

class PostDetailView(LoginRequiredMixin, View):
    def get(self, request, pk, *args, **kwargs):
        user = request.user
        post = Post.objects.get(pk=pk)
        categories = Category.objects.all()
        form = CommentForm()
        
        # Retrieve the UserProfile instance associated with the post's author
        profile = UserProfile.objects.get(user=post.author)
        followers = profile.followers.all()

        comments = Comment.objects.filter(post=post).order_by('-created_on')
        categories = Category.objects.filter(user=user)

        # Retrieve the user's activity for this post (if any)
        user_activity = PostActivity.objects.filter(post=post, user=user).first()

        context = {
            'categories': categories,
            'post': post,
            'form': form,
            'comments': comments,
            'profile': profile,
            'followers': followers,
            'user_activity': user_activity,
        }

        return render(request, 'social/post_detail.html', context)

    def post(self, request, pk, *args, **kwargs):
        user = request.user
        post = Post.objects.get(pk=pk)
        categories = Category.objects.all()
        
        # Handle updating an existing activity or creating a new one
        result = request.POST.get('result')
        details = request.POST.get('details')
        strategy = request.POST.get('strategy')
        analysis = request.POST.get('analysis')
        improvement = request.POST.get('improvement')

        if result is not None:  # Check if activity data is being submitted
            user_activity = PostActivity.objects.filter(post=post, user=user).first()

            if user_activity:
                # Update the existing activity
                user_activity.result = result
                user_activity.details = details
                user_activity.strategy = strategy
                user_activity.analysis = analysis
                user_activity.improvement = improvement
                user_activity.save()
            else:
                # Create a new activity
                PostActivity.objects.create(
                    post=post,
                    user=user,
                    result=result,
                    details=details,
                    strategy=strategy,
                    analysis=analysis,
                    improvement=improvement
                )
        
        # Handle adding comments
        form = CommentForm(request.POST)
        
        if form.is_valid():
            comment_text = form.cleaned_data['comment']
            new_comment = Comment(comment=comment_text, post=post, author=user)
            new_comment.save()
            form = CommentForm()  # Clear the form after saving the comment

        # Retrieve the UserProfile instance associated with the post's author
        profile = UserProfile.objects.get(user=post.author)
        followers = profile.followers.all()

        comments = Comment.objects.filter(post=post).order_by('-created_on')
        categories = Category.objects.filter(user=user)

        context = {
            'categories': categories,
            'post': post,
            'form': form,
            'comments': comments,
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'social/post_detail.html', context)

    #---END CATEGORY    

#create the activity here: 
def submit_activity(request, post_id):
    if request.method == 'POST':
        # Process and save the submitted data
        result = request.POST.get('result')
        details = request.POST.get('details')
        strategy = request.POST.get('strategy')
        analysis = request.POST.get('analysis')
        improvement = request.POST.get('improvement')
        
        # Save the data to the database using your model (PostActivity)
        post = Post.objects.get(pk=post_id)  # Get the post based on the post_id
        user = request.user  # Get the current user
        
        post_activity = PostActivity(
            post=post,
            user=user,
            result=result,
            details=details,
            strategy=strategy,
            analysis=analysis,
            improvement=improvement
        )
        post_activity.save()
        
        # Redirect the user to the post detail page
        return redirect('post-detail', pk=post_id)

#New comment box for the users
def add_comment(request):
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        # Save the comment to the database or perform any other necessary actions

        # Create a dictionary with the comment details
        comment_data = {
            'author': request.user.username,
            'created_on': timezone.now().strftime('%Y-%m-%d %H:%M:%S'),
            'comment': comment_text,
        }

        # Return the comment details as JSON response
        return JsonResponse(comment_data)

    # Handle non-POST requests, if needed
    return render(request, 'comment_form.html')


#AddLike and Dislike the app
class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            post.dislikes.remove(request.user)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=post.author, post=post)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

#add like and dislike
class AddDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            post.likes.remove(request.user)

        is_dislike = False

        for dislike in post.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            post.dislikes.add(request.user)

        if is_dislike:
            post.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
#--------End


#user search and List followers
class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
        )

        context = {
            'profile_list': profile_list,
        }

        return render(request, 'social/search.html', context)

# followers
class ListFollowers(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {
            'profile': profile,
            'followers': followers,
        }

        return render(request, 'social/followers_list.html', context)
#---------End


#Add comment like and dislike
class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if is_dislike:
            comment.dislikes.remove(request.user)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)
            notification = Notification.objects.create(notification_type=1, from_user=request.user, to_user=comment.author, comment=comment)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

#Add comments
class AddCommentDislike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        comment = Comment.objects.get(pk=pk)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if is_like:
            comment.likes.remove(request.user)

        is_dislike = False

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            comment.dislikes.add(request.user)

        if is_dislike:
            comment.dislikes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)
#---------End


#profile
class ProfileView(View):
    def get(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user

        form = ProfilePageForm(instance=profile)

        followers = profile.followers.all()
        is_following = False

        if request.user.is_authenticated:
            for follower in followers:
                if follower == request.user:
                    is_following = True
                    break

        number_of_followers = len(followers)

        context = {
            'user': user,
            'profile': profile,
            'form': form,
            'number_of_followers': number_of_followers,
            'is_following': is_following,
        }
        return render(request, "registration/profile.html", context)

    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        form = ProfilePageForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile', pk=pk)
        else:
            return render(request, "registration/profile.html", {'form': form})
# End__Profile


#PostNotification
class PostNotification(View):
    def get(self, request, notification_pk, post_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        post = Post.objects.get(pk=post_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('post-detail', pk=post_pk)


#follow notification and remove notification
class FollowNotification(View):
    def get(self, request, notification_pk, profile_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)
        profile = UserProfile.objects.get(pk=profile_pk)

        notification.user_has_seen = True
        notification.save()

        return redirect('profile', pk=profile_pk)

class RemoveNotification(View):
    def delete(self, request, notification_pk, *args, **kwargs):
        notification = Notification.objects.get(pk=notification_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type='text/plain')
#--------End

#Post edit class
class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
#---END edit post


#comment delete view
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post-detail', kwargs={'pk': pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
#---END comment


#Post delete class
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy('post-list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author
#----END DELETE post


#Comment Reply to users
class CommentReplyView(LoginRequiredMixin, View):
    def post(self, request, post_pk, pk, *args, **kwargs):
        post = Post.objects.get(pk=post_pk)
        parent_comment = Comment.objects.get(pk=pk)
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=parent_comment.author, comment=new_comment)

        return redirect('post-detail', pk=post_pk)
#-----END COMMENT VIEW

# Add post section
class AddPostView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'social/add_post.html'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()

        # Retrieve recipient email from the form
        recipient_email = self.request.POST.get('recipient_email')

        # Send email notification
        subject = 'New Post Added'
        message = f'A new post has been added:\n\nTitle: {form.cleaned_data["title"]}\nTag: {form.cleaned_data["tags"]}\nAuthor: {form.cleaned_data["author"]}\n\n{form.cleaned_data["body"]}\n\n{form.cleaned_data["Where_to_Apply"]}'
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [recipient_email])

        return super().form_valid(form)



#add comment section
class AddCommentView(CreateView):
    model = Comment  
    form_class = CommentForm
    template_name = 'social/add_comment.html'
    #fields = '__all__'
    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    #fields = ('title', 'body')
    success_url = reverse_lazy('home')

#follower add and delete follower
class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        notification = Notification.objects.create(notification_type=3, from_user=request.user, to_user=profile.user)

        return redirect('profile', pk=profile.pk)

#removefollower()
class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        notification = Notification.objects.create(notification_type=2, from_user=request.user, to_user=profile.user)

        return redirect('profile', pk=profile.pk)

#fields = ('title', 'body')
class UpdatePostView(UpdateView):
    model = Post
    form_class = EditForm
    template_name = "update_post.html"
    #fields = ['title', 'title_tag', 'body']

class DeletePostView(DeleteView):
    model = Post
    template_name = 'delete_post.html'
    success_url = reverse_lazy('home')
#search page


#Post search
#search page
def post_search(request):
    form = PostSearchForm()
    q = ''
    c = ''
    results = []
    query = Q()

    if request.POST.get('action') == 'post':
        search_string = str(request.POST.get('ss'))

        if search_string is not None:
            search_string = Post.objects.filter(
                title__contains=search_string)[:5]

            data = serializers.serialize('json', list(
                search_string), fields=('id', 'title', 'slug'))

            return JsonResponse({'search_string': data})

    if 'q' in request.GET:
        form = PostSearchForm(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            c = form.cleaned_data['c']

            if c is not None:
                query &= Q(category=c)
            if q is not None:
                query &= Q(title__contains=q)

            results = Post.objects.filter(query)

    return render(request, 'social/search-file.html',
                  {'form': form,
                   'q': q,
                   'results': results})

#---END title post search


#Each individual must see a unique carousel page
def carousel_page(request):
    if request.user.is_superuser:
        # Admin user can see all posts
        posts = Post.objects.all()
    else:
        # Individual users can only see their own posts
        posts = Post.objects.filter(user=request.user)
    return render(request, 'carousel_page.html', {'posts': posts})


#Trading activity
class TradingActivityListView(LoginRequiredMixin, ListView):
    model = TradingActivity
    template_name = 'tradingactivity/tradingactivity_list.html'
    context_object_name = 'activities'
    ordering = ['-due_date']

    def get_queryset(self):
        return TradingActivity.objects.filter(user=self.request.user)

#create the trading view
class TradingActivityCreateView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tradingactivity/create_activity.html')

    def post(self, request):
        user = request.user
        title = request.POST.get('title')
        description = request.POST.get('description')
        due_date = request.POST.get('due_date')
        
        TradingActivity.objects.create(user=user, title=title, description=description, due_date=due_date)
        
        return redirect('trading-activity-list')    

#view the trading activity_list
class TradingActivityListView(LoginRequiredMixin, ListView):
    model = TradingActivity
    template_name = 'tradingactivity/tradingactivity_list.html'
    context_object_name = 'trading_activities'
    ordering = ['-due_date']

    def get_queryset(self):
        # Filter the queryset to retrieve activities associated with the logged-in user
        user = self.request.user
        return TradingActivity.objects.filter(user=user)

#edit trading activity : 
class EditActivityView(View):
    template_name = 'tradingactivity/edit_activity.html'

    def get(self, request, activity_id):
        try:
            activity = TradingActivity.objects.get(id=activity_id)
            if activity.user == request.user:
                context = {
                    'activity': activity,
                    'activity_id': activity_id,
                }
                return render(request, self.template_name, context)
            else:
                return redirect('theblog:activity_list')
        except TradingActivity.DoesNotExist:
            pass

#delete activities
class DeleteActivityView(View):
    def get(self, request, activity_id):
        try:
            activity = TradingActivity.objects.get(id=activity_id)
            if activity.user == request.user:
                activity.delete()
        except TradingActivity.DoesNotExist:
            pass

        return redirect('theblog:activity_list')

#homeview
class HealthcareView(TemplateView):
    template_name = 'health/healthcare.html'

#crowdfunding
class CrowdfundingView(TemplateView):
    template_name = 'crowdfunding.html'

#social justice and civil rights
class SocialJusticeView(TemplateView):
    template_name = 'social_justice.html'

#agriculture
class AgricultureView(TemplateView):
    template_name = 'agriculture.html'

#news section
# ########################################################
# News & Events
# ########################################################

def news_view(request):
    items = NewsAndEvents.objects.all().order_by("-updated_date")
    context = {
        "title": "News & Events",
        "items": items,
    }
    return render(request, "core/news.html", context)


#add news events posts
def post_add(request):
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        post = NewsAndEvents.objects.create(
            title=data.get('title'),
            summary=data.get('summary'),
            posted_as=data.get('posted_as'),
            image=image,
        )

        # Email logic here...

        messages.success(request, "News post added!")
        return redirect('home')

    return render(request, 'core/post_add.html')



def edit_post(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)
    if request.method == "POST":
        form = NewsAndEventsForm(request.POST, instance=instance)
        title = request.POST.get("title")
        if form.is_valid():
            form.save()

            messages.success(request, (title + " has been updated."))
            return redirect("home")
        else:
            messages.error(request, "Please correct the error(s) below.")
    else:
        form = NewsAndEventsForm(instance=instance)
    return render(
        request,
        "hod_template/post_add.html",
        {
            "title": "Edit Post",
            "form": form,
        },
    )



def delete_post(request, pk):
    post = get_object_or_404(NewsAndEvents, pk=pk)
    title = post.title
    post.delete()
    messages.success(request, (title + " has been deleted."))
    return redirect("staff_home")