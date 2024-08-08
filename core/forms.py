from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from inventory.models import Collection, Sneaker, SneakerVariation
from django.forms import inlineformset_factory

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
            }),
            'password1': forms.PasswordInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
            }),
            'password2': forms.PasswordInput(attrs={
                'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
            }),
        }

    def save(self, commit=True):
        user = super(UserRegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']
        widgets = {
            'bio': forms.TextInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'location': forms.HiddenInput(),

        }



class SneakerForm(forms.ModelForm):
    class Meta:
        model = Sneaker
        fields = '__all__'
        widgets = {
            'user': forms.HiddenInput(),
            'name': forms.TextInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'brand': forms.TextInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'price': forms.NumberInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'release_date': forms.DateInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'type': 'date'}),
            'is_new': forms.CheckboxInput(attrs={'class': 'form-checkbox text-blue-600 focus:ring-blue-500'}),
            'purchase_date': forms.DateInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm', 'type': 'date'}),
            'color': forms.TextInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'location': forms.TextInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
        }




class SneakerVariationForm(forms.ModelForm):
    class Meta:
        model = SneakerVariation
        fields = ['size', 'quantity']
        widgets = {
            'size': forms.TextInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
            'quantity': forms.NumberInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
        }

SneakerVariationFormset = inlineformset_factory(
    Sneaker,
    SneakerVariation,
    extra=1,
    form=SneakerVariationForm,  # Start with one empty form for variations
    can_delete=True
)





class CollectionForm(forms.ModelForm):
    sneakers = forms.ModelMultipleChoiceField(
        queryset=Sneaker.objects.none(),  # Default empty queryset
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Collection
        fields = ['description']
        widgets = {
            'description': forms.Textarea(attrs={'class': 'mt-1 block w-full h-10 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'}),
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        if user:
            # Set the queryset for sneakers field based on the provided user's profile
            profile = Profile.objects.get(user=user)
            self.fields['sneakers'].queryset = Sneaker.objects.filter(user=profile)

        if self.instance.pk:
            # Get sneakers already in the collection
            current_sneakers = self.instance.sneaker.all()
            # Attach display names to indicate if they are already in the collection
            self.fields['sneakers'].label_from_instance = self.get_label_from_instance(current_sneakers)

    def get_label_from_instance(self, current_sneakers):
        def label_from_instance(sneaker):
            if sneaker in current_sneakers:
                return f"{sneaker.name} (Already in collection)"
            else:
                return sneaker.name
        return label_from_instance