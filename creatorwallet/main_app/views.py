import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Deal, Platform, Attachment, Activity
from .forms import ActivityForm
from .platformAPI.twitch import twitchStats
from .platformAPI.youtube import youtubeStats
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import UserPayment
import stripe
import time

# Create your views here.
# Define the home view
def home(request):
  return render(request, 'home.html')


# Define the about view
def about(request):
  return render(request, 'about.html')

# Definte the dashboard view
def dashboard(request):
  return render(request, 'dashboard.html')


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('home')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm(label_suffix="")
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

class DealCreate(LoginRequiredMixin, CreateView):
  model = Deal
  fields = ['name', 'amount', 'details', 'url', 'promo_code', 'done', 'due_date']
  
  # This inherited method is called when a
  # valid deal form is being submitted
  fields = ['name', 'amount', 'url', 'promo_code', 'due_date', 'details', 'done']
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the deal
    # Let the CreateView do its job as usual
    return super().form_valid(form)
  

class DealUpdate(LoginRequiredMixin, UpdateView):
    model = Deal
    # Let's disallow the renaming of a deal by excluding the name field!
    fields = ['name', 'amount', 'url', 'promo_code', 'due_date', 'details', 'done']
    def get_success_url(self):
      path = self.request.session.get('path')
      return path
  

@login_required
def deals_index(request):
  request.session['path'] = request.get_full_path()
  deals = Deal.objects.filter(user=request.user)
  # You could also retrieve the logged in user's deals like this
  # deals = request.user.deal_set.all()
  return render(request, 'deals/index.html', { 'deals': deals })

@login_required
def deals_detail(request, deal_id):
  request.session['path'] = request.get_full_path()
  deal = Deal.objects.get(id=deal_id)
  if request.method == 'POST':
        stripe.api_key = os.environ['STRIPE_SECRET_KEY_TEST']
        
        stripe.PaymentIntent.create(
          amount=1099,
          currency="usd",
          setup_future_usage="off_session",
        )
        print ("os.getenv('PRODUCT_PRICE')", os.getenv('PRODUCT_PRICE'))
        checkout_session = stripe.checkout.Session.create(
            payment_method_types = ['card'],
            line_items=[
                {
                    'price_data': {
                        'currency': 'usd',
                        'unit_amount': int(deal.amount*100),
                        'product_data': {
                            'name': deal.name,
                            # 'images': ['https://i.imgur.com/EHyR2nP.png'],
                        },
                    },
                    'quantity': 1,
                },
            ],
            mode = 'payment',
            customer_creation = 'always',
            success_url = os.environ['REDIRECT_DOMAIN'] + '/payment_successful?session_id={CHECKOUT_SESSION_ID}',
            cancel_url = os.environ['REDIRECT_DOMAIN'] + '/payment_cancelled',
        )
        return redirect(checkout_session.url, code=303)
  id_list = deal.platforms.values_list('id').filter(user=request.user)
  platforms_deal_doesnt_have = Platform.objects.exclude(id__in = id_list).filter(user=request.user)

  activity_form = ActivityForm()
  return render(request, 'deals/detail.html', { 'deal': deal, "activity_form": activity_form, 'platforms': platforms_deal_doesnt_have  })


def add_activity(request, deal_id):
    # create a ModelForm instance using the data in data that was submitted
    form = ActivityForm(request.POST)
    # validate the form
    if form.is_valid():
        # don't save the form to the db until it
        # has the deal_id assigned
        new_activity = form.save(commit=False)
        new_activity.deal_id = deal_id
        new_activity.save()
    return redirect("detail", deal_id=deal_id)

class ActivityDelete(LoginRequiredMixin, DeleteView):
    model = Activity
    def get_success_url(self):
      path = self.request.session.get('path')
      return path

class DealDelete(LoginRequiredMixin, DeleteView):
    model = Deal
    success_url = "/deals"

class PlatformList(LoginRequiredMixin, ListView):
  model = Platform

  def get_queryset(self):
      self.request.session['path'] = self.request.get_full_path()
      return Platform.objects.filter(user=self.request.user)

@login_required
def platforms_detail(request, platform_id):
  request.session['path'] = request.get_full_path()

  stats = []
  platform = Platform.objects.get(id=platform_id)
  if "youtube.com" in platform.url.lower():
    stats = youtubeStats(platform.platform_username)
  elif "twitch.tv" in platform.url.lower():
    stats = twitchStats(platform.platform_username)

  return render(request, 'platforms/details.html', {
    'platform': platform, 'stats': stats
  })

class PlatformCreate(LoginRequiredMixin, CreateView):
  model = Platform
  fields = ['name', 'url', 'platform_username']
  success_url = '/platforms'

  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    print ('self.request.user', self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)



class PlatformUpdate(LoginRequiredMixin, UpdateView):
  model = Platform
  fields = ['name', 'url']
  def get_success_url(self):
    path = self.request.session.get('path')
    return path

class PlatformDelete(LoginRequiredMixin, DeleteView):
  model = Platform
  success_url = '/platforms'

@login_required
def assoc_platform(request, deal_id, platform_id):
  # Note that you can pass a platform's id instead of the whole platform object
  Deal.objects.get(id=deal_id).platforms.add(platform_id)
  return redirect('detail', deal_id=deal_id)

@login_required
def unassoc_platform(request, deal_id, platform_id):
  # Note that you can pass a platform's id instead of the whole platform object
  Deal.objects.get(id=deal_id).platforms.remove(platform_id)
  return redirect('detail', deal_id=deal_id)


@login_required
def delete_attachment(request, deal_id, attachment_id):
  if request.method == 'POST':
    attachment = Attachment.objects.get(id=attachment_id)
    client = boto3.client('s3')
    key = attachment.url.split('/')[-2]+"/"+attachment.url.split('/')[-1]
    bucket = os.environ['S3_BUCKET']
    client.delete_object(Bucket=bucket, Key=key)

    attachment.delete()

  return redirect('detail', deal_id=deal_id)


def add_attachment(request, deal_id):
    # attachment-file will be the "name" attribute on the <input type="file">
    attachment_file = request.FILES.get('attachment-file', None)
    if attachment_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + "/" + attachment_file.name
        # just in case something goes wrong
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(attachment_file, bucket, key)
            # build the full url string
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            print ('url', url)
            # we can assign to deal_id or deal (if you have a deal object)
            Attachment.objects.create(url=url, deal_id=deal_id, filename=attachment_file.name)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)

    return redirect('detail',  deal_id=deal_id)


## use Stripe dummy card: 4242 4242 4242 4242
def payment_successful(request):
	stripe.api_key = os.environ['STRIPE_SECRET_KEY_TEST']
	checkout_session_id = request.GET.get('session_id', None)
	session = stripe.checkout.Session.retrieve(checkout_session_id)
	customer = stripe.Customer.retrieve(session.customer)
	user_id = request.user.id
	user_payment = UserPayment.objects.get(app_user=user_id)
	user_payment.stripe_checkout_id = checkout_session_id
	user_payment.save()
	return render(request, 'user_payment/payment_successful.html', {'customer': customer})


def payment_cancelled(request):
	stripe.api_key = os.environ['STRIPE_SECRET_KEY_TEST']
	return render(request, 'user_payment/payment_cancelled.html')


@csrf_exempt
def stripe_webhook(request):
	stripe.api_key = os.environ['STRIPE_SECRET_KEY_TEST']
	time.sleep(10)
	payload = request.body
	signature_header = request.META['HTTP_STRIPE_SIGNATURE']
	event = None
	try:
		event = stripe.Webhook.construct_event(
			payload, signature_header, os.environ['STRIPE_WEBHOOK_SECRET_TEST']
		)
	except ValueError as e:
		return HttpResponse(status=400)
	except stripe.error.SignatureVerificationError as e:
		return HttpResponse(status=400)
	if event['type'] == 'checkout.session.completed':
		session = event['data']['object']
		session_id = session.get('id', None)
		time.sleep(15)
		user_payment = UserPayment.objects.get(stripe_checkout_id=session_id)
		user_payment.payment_bool = True
		user_payment.save()
	return HttpResponse(status=200)

