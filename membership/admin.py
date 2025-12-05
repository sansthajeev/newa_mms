from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import Member, Child, MembershipFee, Payment


class ChildInline(admin.TabularInline):
    """Inline admin for children"""
    model = Child
    extra = 1
    fields = ['name', 'date_of_birth', 'gender']


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    """Admin interface for Member model"""
    list_display = [
        'membership_number',
        'name',
        'phone_number',
        'email',
        'membership_type',
        'is_active',
        'join_date',
        'total_paid_display'
    ]
    list_filter = [
        'membership_type',
        'is_active',
        'join_date',
        'created_at'
    ]
    search_fields = [
        'name',
        'membership_number',
        'phone_number',
        'email',
        'citizenship_number',
        'father_name',
        'mother_name'
    ]
    readonly_fields = ['created_at', 'updated_at', 'total_paid_display']
    
    fieldsets = (
        ('Primary Information', {
            'fields': (
                'name',
                'phone_number',
                'email',
                'permanent_address',
                'current_address'
            )
        }),
        ('Secondary Information', {
            'fields': (
                'father_name',
                'mother_name',
                'spouse_name',
                'citizenship_number',
                'citizenship_issue_date',
                'citizenship_issue_district'
            )
        }),
        ('Membership Details', {
            'fields': (
                'membership_type',
                'membership_number',
                'join_date',
                'is_active',
                'total_paid_display'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    inlines = [ChildInline]
    
    def total_paid_display(self, obj):
        """Display total amount paid"""
        if obj.pk:
            total = obj.get_total_paid()
            return format_html(
                '<strong style="color: green;">NPR {:,.2f}</strong>',
                total
            )
        return "-"
    total_paid_display.short_description = 'Total Paid'
    
    def save_model(self, request, obj, form, change):
        """Auto-generate membership number if not provided"""
        if not obj.membership_number:
            # Get the last membership number
            last_member = Member.objects.all().order_by('id').last()
            if last_member and last_member.membership_number:
                try:
                    last_number = int(last_member.membership_number.split('-')[-1])
                    obj.membership_number = f"NSS-MEM-{last_number + 1:05d}"
                except:
                    obj.membership_number = f"NSS-MEM-{Member.objects.count() + 1:05d}"
            else:
                obj.membership_number = "NSS-MEM-00001"
        super().save_model(request, obj, form, change)


@admin.register(Child)
class ChildAdmin(admin.ModelAdmin):
    """Admin interface for Child model"""
    list_display = ['name', 'member', 'date_of_birth', 'gender']
    list_filter = ['gender', 'date_of_birth']
    search_fields = ['name', 'member__name']
    autocomplete_fields = ['member']


@admin.register(MembershipFee)
class MembershipFeeAdmin(admin.ModelAdmin):
    """Admin interface for MembershipFee model"""
    list_display = [
        'membership_type',
        'payment_mode',
        'amount_display',
        'is_active',
        'created_at'
    ]
    list_filter = ['membership_type', 'payment_mode', 'is_active']
    search_fields = ['description']
    
    fieldsets = (
        ('Fee Structure', {
            'fields': (
                'membership_type',
                'payment_mode',
                'amount',
                'description',
                'is_active'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def amount_display(self, obj):
        """Display amount with currency"""
        return format_html(
            '<strong>NPR {:,.2f}</strong>',
            obj.amount
        )
    amount_display.short_description = 'Amount'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    """Admin interface for Payment model"""
    list_display = [
        'receipt_number',
        'member_link',
        'amount_display',
        'payment_mode',
        'payment_date',
        'collected_by'
    ]
    list_filter = [
        'payment_mode',
        'payment_date',
        'created_at'
    ]
    search_fields = [
        'receipt_number',
        'member__name',
        'member__membership_number',
        'transaction_reference',
        'collected_by'
    ]
    readonly_fields = ['receipt_number', 'created_at', 'updated_at']
    autocomplete_fields = ['member', 'membership_fee']
    date_hierarchy = 'payment_date'
    
    fieldsets = (
        ('Payment Information', {
            'fields': (
                'member',
                'membership_fee',
                'amount',
                'payment_date',
                'payment_mode',
                'transaction_reference'
            )
        }),
        ('Receipt Details', {
            'fields': (
                'receipt_number',
                'collected_by',
                'remarks'
            )
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    
    def member_link(self, obj):
        """Create a link to the member"""
        url = reverse('admin:membership_member_change', args=[obj.member.pk])
        return format_html(
            '<a href="{}">{}</a>',
            url,
            obj.member.name
        )
    member_link.short_description = 'Member'
    
    def amount_display(self, obj):
        """Display amount with currency"""
        return format_html(
            '<strong style="color: green;">NPR {:,.2f}</strong>',
            obj.amount
        )
    amount_display.short_description = 'Amount'
    
    actions = ['generate_receipt_report']
    
    def generate_receipt_report(self, request, queryset):
        """Generate receipt report for selected payments"""
        # This can be extended to generate PDF receipts
        self.message_user(
            request,
            f"Selected {queryset.count()} payment(s) for receipt generation."
        )
    generate_receipt_report.short_description = "Generate receipts for selected payments"