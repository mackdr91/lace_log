from .models import Sneaker, SneakerVariation
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.shortcuts import get_object_or_404
from django.conf import settings
import zipfile
import os
from django.http import HttpResponse
import openpyxl
from core.forms import SneakerForm, SneakerVariationFormset




@login_required(login_url='core:login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def inventory(request):
    user_profile = request.user.profile  # Assuming a OneToOneField from User to Profile
    sneakers = Sneaker.objects.filter(user=user_profile)
    content = {
        'sneakers': sneakers,
    }
    return render(request, 'inventory/sneaker_inv.html', content)


def delete_sneaker(request, pk):
    sneaker = get_object_or_404(Sneaker, pk=pk)
    sneaker.delete()
    return redirect('inventory:inventory')


def download_qr_codes(request):
    # Create a temporary zip file
    zip_filename = "qr_codes.zip"
    zip_filepath = os.path.join(settings.MEDIA_ROOT, zip_filename)

    with zipfile.ZipFile(zip_filepath, 'w') as zip_file:
        # Loop through all sneakers and add their QR code to the zip file
        sneakers = Sneaker.objects.all()
        for sneaker in sneakers:
            qr_code_filename = f"{sneaker.id}.png"
            qr_code_filepath = os.path.join(settings.STATIC_ROOT, 'qr_codes', qr_code_filename)
            print(qr_code_filepath)

            if os.path.exists(qr_code_filepath):
                zip_file.write(qr_code_filepath, qr_code_filename)

    # Serve the zip file as a downloadable response
    with open(zip_filepath, 'rb') as zip_file:
        response = HttpResponse(zip_file.read(), content_type='application/zip')
        response['Content-Disposition'] = f'attachment; filename="{zip_filename}"'

    # Optionally delete the temporary file after serving it
    os.remove(zip_filepath)

    return response




def generate_sneaker_spreadsheet(request):
    # Create an in-memory Excel workbook and worksheet
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Sneaker Inventory"

    # Define the header row
    headers = [
        "Name", "Brand", "Price", "Release Date", "Is New",
        "Purchase Date", "Color", "Location", "Description",
        "Sizes and Quantities"
    ]
    ws.append(headers)

    # Add data rows
    sneakers = Sneaker.objects.all()
    for sneaker in sneakers:
        # Retrieve all variations for the current sneaker
        variations = SneakerVariation.objects.filter(sneaker=sneaker)

        # Collect size and quantity for each variation
        size_quantity_list = [f"Size: {variation.size}, Quantity: {variation.quantity}" for variation in variations]
        size_quantity_str = "; ".join(size_quantity_list)

        # Append sneaker data along with sizes and quantities
        ws.append([
            sneaker.name,
            sneaker.brand,
            sneaker.price,
            sneaker.release_date,
            "Yes" if sneaker.is_new else "No",
            sneaker.purchase_date,
            sneaker.color,
            sneaker.location,
            sneaker.description,
            size_quantity_str  # Sizes and quantities as a single string
        ])

    # Set the response to download the file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=sneaker_inventory.xlsx'
    wb.save(response)

    return response

def add_sneaker(request):
    extra_forms = 5  # Default number of extra forms

    if request.method == 'POST':
        # Get the number of additional forms from POST data
        extra = int(request.POST.get('additional_forms', extra_forms))
        sneaker_form = SneakerForm(request.POST)
        formset = SneakerVariationFormset(request.POST, instance=sneaker_form.instance, extra=extra)

        if sneaker_form.is_valid() and formset.is_valid():
            sneaker = sneaker_form.save()
            formset.instance = sneaker
            formset.save()
            return redirect('core:home')
    else:
        # Handle the extra forms dynamically for GET request
        extra = int(request.GET.get('extra_forms', extra_forms))
        sneaker_form = SneakerForm()
        formset = SneakerVariationFormset(instance=sneaker_form.instance)

    context = {
        'sneaker_form': sneaker_form,
        'formset': formset,
        'extra_forms': extra,  # Pass extra_forms to the template if needed
    }
    return render(request, 'core/add_sneaker.html', context)
