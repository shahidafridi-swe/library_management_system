from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserAccount


class RegisterUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    def __init__(self, *args, **kwargs):
        super(RegisterUserForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        
    def save(self, commit=True):
        user = super().save(commit=False)    
        if commit:
            user.save()
            UserAccount.objects.create(
                user = user,
                account_number = 12340000+user.id,
            )
            
class UpdateUserProfile(UserChangeForm):
    password = None
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
    def __init__(self, *args, **kwargs):
        super(UpdateUserProfile, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.help_text = ''
        
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True


        