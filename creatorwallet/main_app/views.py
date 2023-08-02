from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# Import the login_required decorator
from django.contrib.auth.decorators import login_required
# Import the mixin for class-based views
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Deal, PlatformContent


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
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


class DealCreate(LoginRequiredMixin, CreateView):
  model = Deal
  # This inherited method is called when a
  # valid deal form is being submitted
  fields = ['name', 'amount', 'details', 'url', 'promo_code', 'create_date', 'done', 'due_date']
  def form_valid(self, form):
    # Assign the logged in user (self.request.user)
    form.instance.user = self.request.user  # form.instance is the deal
    # Let the CreateView do its job as usual
    return super().form_valid(form)
  

class DealUpdate(UpdateView):
    model = Deal
    # Let's disallow the renaming of a deal by excluding the name field!
    fields = ['name', 'amount', 'details', 'url', 'promo_code', 'create_date', 'done', 'due_date']
  

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