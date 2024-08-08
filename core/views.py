from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from inventory.utils import generate_qr_code
from django.core.paginator import Paginator

from .forms import ProfileForm, UserRegisterForm




from inventory.models import Sneaker, Collection
from .forms import SneakerForm, CollectionForm, SneakerVariationFormset

def landing_page(request):
    return render(request, 'core/landing.html')




def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatically log the user in after registration
            return redirect('core:profile')  # Redirect to the home page or any other page
    else:
        form = UserRegisterForm()

    return render(request, 'core/register.html', {'form': form})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@login_required(login_url='core:login')
def create_profile(request):
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('core:home')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'core/create_profile.html', {'form': form})
def Login(request):
	if request.method == 'POST':

		# AuthenticationForm_can_also_be_used__

		username = request.POST['username']
		password = request.POST['password']
		user = authenticate(request, username = username, password = password)
		if user is not None:
			form = login(request, user)
			messages.success(request, f' welcome {username} !!')
			return redirect('core:home')
		else:
			messages.info(request, 'account done not exit plz sign in')
	form = AuthenticationForm()
	return render(request, 'core/login.html', {'form':form, 'title':'log in'})


@login_required(login_url='core:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def home(request):
    user_profile = request.user.profile  # Assuming a OneToOneField from User to Profile
    sneakers = Sneaker.objects.filter(user=user_profile)
    print(sneakers)
    collection = Collection.objects.filter(user=user_profile)
    paginator = Paginator(sneakers, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    content = {
        'sneakers': sneakers,
        'collection': collection,
        'page_obj': page_obj
    }
    return render(request, 'core/home.html', content)

@login_required(login_url='core:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_sneaker(request):
    if request.method == 'POST':
        sneaker_form = SneakerForm(request.POST)
        formset = SneakerVariationFormset(request.POST, instance=sneaker_form.instance)

        if sneaker_form.is_valid() and formset.is_valid():
            sneaker = sneaker_form.save(commit=False)
            sneaker.user = request.user.profile
            sneaker.save()
            formset.instance = sneaker
            formset.save()
            messages.success(request, 'Sneaker added successfully!')
            return redirect('core:home')
    else:
        sneaker_form = SneakerForm()
        formset = SneakerVariationFormset(instance=sneaker_form.instance)

    context = {
        'sneaker_form': sneaker_form,
        'formset': formset,
    }
    return render(request, 'core/add_sneaker.html', context)





@login_required(login_url='core:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def add_collection(request):
	if request.method == 'POST':
		form = CollectionForm(request.POST)
		if form.is_valid():
			collection = form.save(commit=False)
			collection.user = request.user.profile
			collection.save()
			return redirect('core:home')
	else:
		form = CollectionForm(initial={'user': request.user.profile})

	collection = Collection.objects.filter(user=request.user.profile)
	return render(request, 'core/add_collection.html', {'form': form,})

@login_required(login_url='core:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_sneaker(request, pk):
    sneaker = get_object_or_404(Sneaker, pk=pk)

    if request.method == 'POST':
        form = SneakerForm(request.POST, instance=sneaker)
        formset = SneakerVariationFormset(request.POST, instance=sneaker)

        if form.is_valid() and formset.is_valid():
            sneaker = form.save(commit=False)
            sneaker.user = request.user.profile
            sneaker.save()
            formset.save()

            # Regenerate the QR code with the updated details
            generate_qr_code(sneaker)

            print(request, 'Sneaker updated successfully!')

            return redirect('core:sneaker_detail', pk=sneaker.pk)
    else:
        form = SneakerForm(instance=sneaker)
        formset = SneakerVariationFormset(instance=sneaker)

    return render(request, 'core/edit_sneaker.html', {'form': form, 'formset': formset})



@login_required(login_url='core:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def edit_collection(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    if request.method == 'POST':
        form = CollectionForm(request.POST, instance=collection, user=request.user)
        if form.is_valid():
            # Save the form data, but don't commit to the database yet
            collection = form.save(commit=False)

            # Get the sneakers currently in the collection
            current_sneakers = set(collection.sneaker.all())

            # Get the sneakers selected in the form
            new_sneakers = set(form.cleaned_data['sneakers'])

            # Combine the current and new sneakers
            collection.sneaker.set(current_sneakers.union(new_sneakers))

            # Save the collection with the updated sneakers
            collection.save()

            return redirect('core:collection_detail', pk=collection.pk)
    else:
        # Filter sneakers by the current user

        form = CollectionForm(instance=collection, user=request.user)

    return render(request, 'core/edit_collection.html', {'form': form, 'collection': collection})

@login_required(login_url='core:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def remove_sneaker_from_collection(request, collection_pk, sneaker_pk):
    collection = get_object_or_404(Collection, pk=collection_pk)
    sneaker = get_object_or_404(Sneaker, pk=sneaker_pk)

    if request.method == 'POST':
        collection.sneaker.remove(sneaker)
        return redirect('core:collection_detail', pk=collection_pk)

    return render(request, 'core/remove_sneaker.html', {'collection': collection, 'sneaker': sneaker})

@login_required(login_url='core:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def delete_collection(request, pk):
    collection = get_object_or_404(Collection, pk=pk)

    if request.method == 'POST':
        collection.delete()
        return redirect('core:home')  # Redirect to a list of collections or a home page

    return render(request, 'core/delete_collection.html', {'collection': collection})

@login_required(login_url='core:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def collection_detail(request, pk):
    collection = get_object_or_404(Collection, pk=pk)
    return render(request, 'core/collection_detail.html', {'collection': collection})

@login_required(login_url='core:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def sneaker_detail(request, pk):
	sneaker = Sneaker.objects.get(pk=pk)
	return render(request, 'core/sneaker_detail.html', {'sneaker': sneaker})
