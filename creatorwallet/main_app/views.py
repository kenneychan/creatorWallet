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
from .models import Deal, PlatformContent, Attachment
from .forms import ActivityForm
from .platformAPI.twitch import twitchStats
from .platformAPI.youTube import youTubeStats


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
  

class DealUpdate(LoginRequiredMixin, UpdateView):
    model = Deal
    # Let's disallow the renaming of a deal by excluding the name field!
    fields = ['name', 'amount', 'url', 'promo_code', 'due_date', 'details', 'done']
    def get_success_url(self):
      return reverse('detail', args=(self.object.pk,))
  

@login_required
def deals_index(request):
  deals = Deal.objects.filter(user=request.user)
  # You could also retrieve the logged in user's deals like this
  # deals = request.user.deal_set.all()
  return render(request, 'deals/index.html', { 'deals': deals })

@login_required
def deals_detail(request, deal_id):
  deal = Deal.objects.get(id=deal_id)
  id_list = deal.platformscontent.values_list('id').filter(user=request.user)
  platformscontent_deal_doesnt_have = PlatformContent.objects.exclude(id__in = id_list).filter(user=request.user)

  activity_form = ActivityForm()
  return render(request, 'deals/detail.html', { 'deal': deal, "activity_form": activity_form, 'platformscontent': platformscontent_deal_doesnt_have  })


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


class DealDelete(LoginRequiredMixin, DeleteView):
    model = Deal
    success_url = "/deals"


class PlatformContentList(LoginRequiredMixin, ListView):
  model = PlatformContent

  def get_queryset(self):
      return PlatformContent.objects.filter(user=self.request.user)


# class PlatformContentDetail(LoginRequiredMixin, DetailView):
#   model = PlatformContent
def platformContents_detail(request, platformcontent_id):
  platformContent = PlatformContent.objects.get(id=platformcontent_id)
  print ('url', platformContent.url.lower())
  if "youtube.com" in platformContent.url.lower():
    stats = youTubeStats(platformContent.platform_username)
  elif "twitch.tv" in platformContent.url.lower():
    stats = twitchStats(platformContent.platform_username)

  return render(request, 'platformContents/details.html', {
    'platformContent': platformContent, 'stats': stats
  })

class PlatformContentCreate(LoginRequiredMixin, CreateView):
  model = PlatformContent
  fields = ['name', 'url', 'platform_username']
  success_url = '/platformscontent'

  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    print ('self.request.user', self.request.user)
    form.instance.user = self.request.user  # form.instance is the cat
    # Let the CreateView do its job as usual
    return super().form_valid(form)



class PlatformContentUpdate(LoginRequiredMixin, UpdateView):
  model = PlatformContent
  fields = ['name', 'url']
  success_url = '/platformscontent'
  


class PlatformContentDelete(LoginRequiredMixin, DeleteView):
  model = PlatformContent
  success_url = '/platformscontent'

@login_required
def assoc_platformcontent(request, deal_id, platformcontent_id):
  # Note that you can pass a platform's id instead of the whole platform object
  Deal.objects.get(id=deal_id).platformscontent.add(platformcontent_id)
  return redirect('detail', deal_id=deal_id)

@login_required
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

    print (Attachment.objects.all())

    return redirect('detail',  deal_id=deal_id)