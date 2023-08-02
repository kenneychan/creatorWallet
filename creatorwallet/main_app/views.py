import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Deal, PlatformContent, Attachment

# Create your views here.
# Define the home view
def home(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'home.html')


# Define the about view
def about(request):
  # Include an .html file extension - unlike when rendering EJS templates
  return render(request, 'about.html')


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
  

class DealUpdate(UpdateView):
    model = Deal
    # Let's disallow the renaming of a deal by excluding the name field!
    fields = ['name', 'amount', 'url', 'promo_code', 'due_date', 'details', 'done']
  

@login_required
def deals_index(request):
  deals = Deal.objects.filter(user=request.user)
  # You could also retrieve the logged in user's deals like this
  # deals = request.user.deal_set.all()
  return render(request, 'deals/index.html', { 'deals': deals })


def deals_detail(request, deal_id):
  deal = Deal.objects.get(id=deal_id)
  id_list = deal.platformscontent.values_list('id')
  platformscontent_deal_doesnt_have = PlatformContent.objects.exclude(id__in = id_list)
  return render(request, 'deals/detail.html', { 'deal': deal, 'platformscontent': platformscontent_deal_doesnt_have})

class DealDelete(DeleteView):
    model = Deal
    success_url = "/deals"


class PlatformContentList(ListView):
  model = PlatformContent


class PlatformContentDetail(DetailView):
  model = PlatformContent


class PlatformContentCreate(CreateView):
  model = PlatformContent
  fields = '__all__'


class PlatformContentUpdate(UpdateView):
  model = PlatformContent
  fields = ['name', 'url']
  


class PlatformContentDelete(DeleteView):
  model = PlatformContent
  success_url = '/platformscontent'


def assoc_platformcontent(request, deal_id, platformcontent_id):
  # Note that you can pass a platform's id instead of the whole platform object
  Deal.objects.get(id=deal_id).platformscontent.add(platformcontent_id)
  return redirect('detail', deal_id=deal_id)
def unassoc_platformcontent(request, deal_id, platformcontent_id):
  # Note that you can pass a platform's id instead of the whole platform object
  Deal.objects.get(id=deal_id).platformscontent.remove(platformcontent_id)
  return redirect('detail', deal_id=deal_id)

# def add_attachment(request, deal_id):
def add_attachment(request, deal_id):
    # attachment-file will be the "name" attribute on the <input type="file">
    attachment_file = request.FILES.get('attachment-file', None)
    if attachment_file:
        s3 = boto3.client('s3')
        # need a unique "key" for S3 / needs image file extension too
        key = uuid.uuid4().hex[:6] + attachment_file.name[attachment_file.name.rfind('.'):]
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

    print (Attachment.objects.all())

    return redirect('detail',  deal_id=deal_id)