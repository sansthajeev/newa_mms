from django.urls import path
from . import views

app_name = 'membership'

urlpatterns = [
    # Authentication
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('pending/', views.pending_approval, name='pending_approval'),
    
    # User Approval (Admin Only)
    path('users/', views.user_approval_list, name='user_approval_list'),
    path('users/<int:pk>/', views.user_detail_admin, name='user_detail'),
    path('users/<int:pk>/approve/', views.user_approve, name='user_approve'),
    path('users/<int:pk>/unapprove/', views.user_unapprove, name='user_unapprove'),
    
    # Dashboard
    path('', views.home, name='home'),
    
    # Members
    path('members/', views.member_list, name='member_list'),
    path('members/add/', views.member_add, name='member_add'),
    path('members/<int:pk>/', views.member_detail, name='member_detail'),
    path('members/<int:pk>/edit/', views.member_edit, name='member_edit'),
    path('members/<int:pk>/delete/', views.member_delete, name='member_delete'),
    
    # Payments
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/add/', views.payment_add, name='payment_add'),
    path('payments/<int:pk>/edit/', views.payment_edit, name='payment_edit'),
    path('payments/<int:pk>/delete/', views.payment_delete, name='payment_delete'),
    path('payments/<int:pk>/receipt/', views.payment_receipt, name='payment_receipt'),
    
    # Membership Fees
    path('fees/', views.fee_list, name='fee_list'),
    path('fees/add/', views.fee_add, name='fee_add'),
    path('fees/<int:pk>/edit/', views.fee_edit, name='fee_edit'),
    path('fees/<int:pk>/delete/', views.fee_delete, name='fee_delete'),
    
    # Reports
    path('reports/revenue/', views.revenue_report, name='revenue_report'),
    path('reports/renewal-required/', views.renewal_required_report, name='renewal_required_report'),
    path('reports/membership-expiry/', views.membership_expiry_report, name='membership_expiry_report'),
    path('reports/new-members/', views.new_members_report, name='new_members_report'),
]