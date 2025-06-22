from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from .models import SubProject, UserProfile
import random
import string


class CaptchaField(forms.CharField):
    """验证码字段"""
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 4
        kwargs['min_length'] = 4
        kwargs['widget'] = forms.TextInput(attrs={
            'placeholder': '请输入验证码',
            'class': 'form-control',
            'style': 'text-transform: uppercase;'
        })
        super().__init__(*args, **kwargs)


class LoginForm(AuthenticationForm):
    """登录表单"""
    username = forms.CharField(
        label='用户名',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入用户名'
        })
    )
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': '请输入密码'
        })
    )
    captcha = CaptchaField(label='验证码')


class SubProjectForm(forms.ModelForm):
    """子项目表单"""
    class Meta:
        model = SubProject
        fields = [
            'project_number', 'date', 'construction_period',
            'start_date', 'completion_date', 'address',
            'construction_unit', 'contact_person', 'phone',
            'contractor', 'contractor_contact', 'owner',
            'area', 'construction_cost', 'rectification_details', 'remarks'
        ]
        widgets = {
            'project_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'construction_period': forms.TextInput(attrs={'class': 'form-control'}),
            'start_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'completion_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'construction_unit': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_person': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'contractor': forms.TextInput(attrs={'class': 'form-control'}),
            'contractor_contact': forms.TextInput(attrs={'class': 'form-control'}),
            'owner': forms.TextInput(attrs={'class': 'form-control'}),
            'area': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'construction_cost': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'rectification_details': forms.NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'remarks': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CreateUserForm(forms.ModelForm):
    """创建用户表单（仅管理员可用）"""
    password = forms.CharField(
        label='密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    password_confirm = forms.CharField(
        label='确认密码',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    is_admin = forms.BooleanField(
        label='是否为管理员',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    organization = forms.CharField(
        label='所属单位',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入所属单位'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': '用户名',
            'first_name': '姓',
            'last_name': '名',
            'email': '邮箱',
        }
    
    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('两次输入的密码不一致')
        return password_confirm
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                is_admin=self.cleaned_data['is_admin'],
                organization=self.cleaned_data['organization']
            )
        return user


class UpdateUserForm(forms.ModelForm):
    """修改用户表单（仅管理员可用）"""
    is_admin = forms.BooleanField(
        label='是否为管理员',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    organization = forms.CharField(
        label='所属单位',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '请输入所属单位'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'username': '用户名',
            'first_name': '姓',
            'last_name': '名',
            'email': '邮箱',
        }
    
    def __init__(self, *args, **kwargs):
        self.user_profile = kwargs.pop('user_profile', None)
        super().__init__(*args, **kwargs)
        if self.user_profile:
            self.fields['is_admin'].initial = self.user_profile.is_admin
            self.fields['organization'].initial = self.user_profile.organization
    
    def save(self, commit=True):
        user = super().save(commit=commit)
        if commit and self.user_profile:
            self.user_profile.is_admin = self.cleaned_data['is_admin']
            self.user_profile.organization = self.cleaned_data['organization']
            self.user_profile.save()
        return user 