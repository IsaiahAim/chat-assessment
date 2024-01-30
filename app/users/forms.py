from django.contrib import messages
from django import forms
from django.contrib.auth.models import User

from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, PasswordResetForm, PasswordChangeForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email',)

    def __init__(self, *args, **kwargs):
        super(CustomUserChangeForm, self).__init__(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=150, min_length=8,
                               widget=forms.TextInput(attrs={"placeholder": "Enter Username"}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"placeholder": "Enter password"}))
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"placeholder": "Re-enter password"}))

    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].widget.attrs.update({"class": "registeration"})
        self.fields["password"].widget.attrs.update({"class": "registeration"})
        self.fields["password2"].widget.attrs.update({"class": "registeration"})

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']

    def validate_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email=email).exists():
            return messages.info("email already exists.")
        return email

# class UserRegistrationForm(forms.ModelForm):
#
#     model = CustomUser
#     first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":"Enter first name"}))
#     last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":"Enter last name"}))
#     email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={"placeholder":"Enter email"}))
#     username = forms.CharField(max_length=150, min_length=8, widget=forms.TextInput(attrs={"placeholder":"Enter Username"}))
#     password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"placeholder":"Enter password"}))
#     password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"placeholder":"Re-enter password"}))
#
#     class Meta:
#         model = CustomUser
#         fields = ["username", "first_name", "last_name", "email", "password1", "password2"]
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields["first_name"].widget.attrs.update({"class":"registeration"})
#         self.fields["last_name"].widget.attrs.update({"class":"registeration"})
#         self.fields["email"].widget.attrs.update({"class":"registeration"})
#         self.fields["username"].widget.attrs.update({"class":"registeration"})
#         self.fields["password1"].widget.attrs.update({"class":"registeration"})
#         self.fields["password2"].widget.attrs.update({"class":"registeration"})
#
#     def validate_email(self):
#         email = self.cleaned_data["email"]
#         if CustomUser.objects.filter(email=email).exists():
#             return messages.info("email already exists.")
#         return email


class UserForm(forms.ModelForm):

    class Meta:
        model = User
        fields = '__all__'
        exclude = ('date_joined', 'profile_code')
        widgets = {
            "email": forms.EmailInput(attrs={"class": "form-control mt-3", "placeholder": "Enter email"}),
            "first_name": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter first name"}),
            "last_name": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter last name"}),
            "gender": forms.Select(attrs={"class": "form-control mt-3"}),
            "phone_no": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter phone_no"}),
            "password": forms.PasswordInput(attrs={"class": "form-control mt-3", "placeholder": "Enter password"}),
            "address": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter address"}),
            "city": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter city"}),
            "state": forms.TextInput(attrs={"class": "form-control mt-3", "placeholder": "Enter state"}),
            "country": forms.Select(attrs={"class": "form-control mt-3"}),
            "profile_picture": forms.FileInput(attrs={"class": "form-control mt-3"}),
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(widget=forms.EmailInput, required=False)
    phone_no = forms.CharField(max_length=14, required=False)
    address = forms.CharField(max_length=100, required=False)
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email',
                  'phone_no', 'address', 'city', 'state']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['last_name'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['email'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['phone_no'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['address'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['city'].widget.attrs.update({"class": "form-control mb-3"})
        self.fields['state'].widget.attrs.update(
            {"class": "form-control mb-3"})
        self.fields['profile_picture'].widget.attrs.update(
            {"class": "form-control mb-3"})


class CustomPasswordResetForm(PasswordResetForm):
    class Meta:
        widgets = {"email": forms.EmailInput(
            attrs={"class": "form-control mt-3", "placeholder": "Enter email"})}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is not registered.")
        return email


class CustomPasswordConfirmForm(PasswordChangeForm):
    pass
