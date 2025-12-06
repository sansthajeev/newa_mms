from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Member, Child, MembershipFee, Payment


class LoginForm(AuthenticationForm):
    """Custom login form"""
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Username'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )


class RegisterForm(UserCreationForm):
    """User registration form"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Email'
        })
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'First Name'
        })
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Last Name'
        })
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Username'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm Password'
        })


class MemberForm(forms.ModelForm):
    """Form for adding/editing members"""
    
    class Meta:
        model = Member
        fields = [
            'photograph', 'name', 'date_of_birth', 'gender', 'phone', 'email', 'address',
            'father_name', 'grandfather_name', 'spouse_name',
            'citizenship_number', 'citizenship_issue_date', 'citizenship_issue_district',
            'membership_type', 'payment_frequency', 'join_date', 'is_active'
        ]
        widgets = {
            'photograph': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+977XXXXXXXXXX'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@example.com'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Full Address'}),
            'father_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Father's Name"}),
            'grandfather_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Grandfather's Name (Optional)"}),
            'spouse_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Spouse's Name (Optional)"}),
            'citizenship_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Citizenship Number'}),
            'citizenship_issue_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'citizenship_issue_district': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Issue District'}),
            'membership_type': forms.Select(attrs={'class': 'form-select'}),
            'payment_frequency': forms.Select(attrs={'class': 'form-select'}),
            'join_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
    
    def save(self, commit=True):
        member = super().save(commit=False)
        
        # Auto-generate membership number if not provided
        if not member.membership_number:
            last_member = Member.objects.all().order_by('id').last()
            if last_member and last_member.membership_number:
                try:
                    last_number = int(last_member.membership_number.split('-')[-1])
                    member.membership_number = f"NSS-MEM-{last_number + 1:05d}"
                except:
                    member.membership_number = f"NSS-MEM-{Member.objects.count() + 1:05d}"
            else:
                member.membership_number = "NSS-MEM-00001"
        
        if commit:
            member.save()
        return member


class ChildForm(forms.ModelForm):
    """Form for adding children"""
    
    class Meta:
        model = Child
        fields = ['name', 'date_of_birth', 'gender']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Child's Name"}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'gender': forms.Select(attrs={'class': 'form-select'}),
        }


# Formset for managing multiple children
from django.forms import inlineformset_factory

ChildFormSet = inlineformset_factory(
    Member,
    Child,
    form=ChildForm,
    extra=1,
    can_delete=True,
    widgets={
        'name': forms.TextInput(attrs={'class': 'form-control'}),
        'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        'gender': forms.Select(attrs={'class': 'form-select'}),
    }
)


class MembershipFeeForm(forms.ModelForm):
    """Form for managing membership fees"""
    
    class Meta:
        model = MembershipFee
        fields = ['membership_type', 'payment_frequency', 'amount', 'description', 'is_active']
        widgets = {
            'membership_type': forms.Select(attrs={'class': 'form-select'}),
            'payment_frequency': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Amount'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Description (Optional)'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }


class PaymentForm(forms.ModelForm):
    """Form for recording payments"""
    
    class Meta:
        model = Payment
        fields = [
            'member', 'membership_fee', 'amount', 'payment_date',
            'payment_mode', 'transaction_reference', 'collected_by', 'remarks'
        ]
        widgets = {
            'member': forms.Select(attrs={'class': 'form-select'}),
            'membership_fee': forms.Select(attrs={'class': 'form-select'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Amount'}),
            'payment_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'payment_mode': forms.Select(attrs={'class': 'form-select'}),
            'transaction_reference': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Transaction Reference (Optional)'}),
            'collected_by': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Collected By'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Remarks (Optional)'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Order members by name
        self.fields['member'].queryset = Member.objects.filter(is_active=True).order_by('name')
        
        # Filter membership fees - only show active fees
        self.fields['membership_fee'].queryset = MembershipFee.objects.filter(is_active=True)
        
        # If editing existing payment, filter fees based on member
        if self.instance.pk and self.instance.member:
            member = self.instance.member
            self.fields['membership_fee'].queryset = MembershipFee.objects.filter(
                membership_type=member.membership_type,
                payment_frequency=member.payment_frequency,
                is_active=True
            )
            # Auto-fill amount from fee structure
            if self.instance.membership_fee:
                self.initial['amount'] = self.instance.membership_fee.amount
        
        # Add data attributes for JavaScript filtering
        self.fields['member'].widget.attrs.update({
            'id': 'id_member',
            'onchange': 'updateFeeOptions()'
        })
        self.fields['membership_fee'].widget.attrs.update({
            'id': 'id_membership_fee',
            'onchange': 'updateAmount()'
        })
    
    def clean(self):
        cleaned_data = super().clean()
        member = cleaned_data.get('member')
        membership_fee = cleaned_data.get('membership_fee')
        
        if member and membership_fee:
            # Validate that fee matches member's type and frequency
            if membership_fee.membership_type != member.membership_type:
                raise forms.ValidationError(
                    f"Selected fee is for {membership_fee.get_membership_type_display()} members, "
                    f"but this member is {member.get_membership_type_display()}."
                )
            
            if membership_fee.payment_frequency != member.payment_frequency:
                raise forms.ValidationError(
                    f"Selected fee is for {membership_fee.get_payment_frequency_display()} payments, "
                    f"but this member pays {member.get_payment_frequency_display()}."
                )
        
        return cleaned_data