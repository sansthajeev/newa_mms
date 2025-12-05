from django.db import models
from django.core.validators import RegexValidator
from django.utils import timezone
from decimal import Decimal
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class Member(models.Model):
    """Primary member information"""
    # Primary Information
    name = models.CharField(max_length=200, verbose_name="Full Name")
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."
    )
    phone_number = models.CharField(
        validators=[phone_regex],
        max_length=17,
        verbose_name="Phone Number"
    )
    email = models.EmailField(verbose_name="Email Address")
    permanent_address = models.TextField(verbose_name="Permanent Address")
    current_address = models.TextField(verbose_name="Current Address")
    
    # Secondary Information
    father_name = models.CharField(max_length=200, verbose_name="Father's Name")
    mother_name = models.CharField(max_length=200, verbose_name="Mother's Name")
    spouse_name = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name="Spouse Name"
    )
    citizenship_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Citizenship Number"
    )
    citizenship_issue_date = models.DateField(
        verbose_name="Citizenship Issue Date",
        blank=True,
        null=True
    )
    citizenship_issue_district = models.CharField(
        max_length=100,
        verbose_name="Citizenship Issue District",
        blank=True,
        null=True
    )
    
    # Membership Information
    MEMBERSHIP_CHOICES = [
        ('REGULAR', 'Regular'),
        ('LIFETIME', 'Lifetime Membership'),
    ]
    membership_type = models.CharField(
        max_length=20,
        choices=MEMBERSHIP_CHOICES,
        default='REGULAR',
        verbose_name="Membership Type"
    )
    membership_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Membership Number"
    )
    join_date = models.DateField(default=timezone.now, verbose_name="Join Date")
    is_active = models.BooleanField(default=True, verbose_name="Active Status")
    
    # Payment Terms
    PAYMENT_FREQUENCY_CHOICES = [
        ('ANNUAL', 'Annual'),
        ('MONTHLY', 'Monthly'),
    ]
    payment_frequency = models.CharField(
        max_length=20,
        choices=PAYMENT_FREQUENCY_CHOICES,
        default='ANNUAL',
        verbose_name="Payment Frequency",
        help_text="How often member pays (only for Regular members)"
    )
    
    # Membership Status Tracking
    last_payment_date = models.DateField(
        blank=True,
        null=True,
        verbose_name="Last Payment Date",
        help_text="Date of most recent payment"
    )
    membership_valid_until = models.DateField(
        blank=True,
        null=True,
        verbose_name="Membership Valid Until",
        help_text="Date when membership expires (null for lifetime members)"
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-join_date']
        verbose_name = "Member"
        verbose_name_plural = "Members"
    
    def __str__(self):
        return f"{self.membership_number} - {self.name}"
    
    def get_total_paid(self):
        """Calculate total amount paid by this member"""
        return self.payments.aggregate(
            total=models.Sum('amount')
        )['total'] or Decimal('0.00')
    
    def get_membership_status(self):
        """
        Calculate current membership status
        Returns: dict with status, days_remaining, is_expired
        """
        # Lifetime members never expire
        if self.membership_type == 'LIFETIME':
            if self.last_payment_date:
                return {
                    'status': 'ACTIVE',
                    'status_display': 'Active (Lifetime)',
                    'is_expired': False,
                    'days_remaining': None,
                    'message': 'Lifetime membership - never expires'
                }
            else:
                return {
                    'status': 'PENDING',
                    'status_display': 'Pending Payment',
                    'is_expired': False,
                    'days_remaining': None,
                    'message': 'Awaiting initial payment'
                }
        
        # Regular members - check expiry
        if not self.membership_valid_until:
            return {
                'status': 'PENDING',
                'status_display': 'Pending Payment',
                'is_expired': False,
                'days_remaining': None,
                'message': 'Awaiting initial payment'
            }
        
        today = timezone.now().date()
        days_remaining = (self.membership_valid_until - today).days
        
        if days_remaining > 30:
            return {
                'status': 'ACTIVE',
                'status_display': 'Active',
                'is_expired': False,
                'days_remaining': days_remaining,
                'message': f'Valid until {self.membership_valid_until.strftime("%B %d, %Y")}'
            }
        elif days_remaining > 0:
            return {
                'status': 'EXPIRING',
                'status_display': 'Expiring Soon',
                'is_expired': False,
                'days_remaining': days_remaining,
                'message': f'Expires in {days_remaining} days'
            }
        else:
            return {
                'status': 'EXPIRED',
                'status_display': 'Expired',
                'is_expired': True,
                'days_remaining': days_remaining,
                'message': f'Expired {abs(days_remaining)} days ago'
            }
    
    def calculate_next_payment_date(self):
        """Calculate when next payment is due"""
        if self.membership_type == 'LIFETIME':
            return None  # Lifetime members don't have recurring payments
        
        if not self.last_payment_date:
            return self.join_date  # First payment due at join date
        
        if self.payment_frequency == 'MONTHLY':
            return self.last_payment_date + relativedelta(months=1)
        else:  # ANNUAL
            return self.last_payment_date + relativedelta(years=1)
    
    def get_expected_fee_amount(self):
        """Get the fee amount this member should pay"""
        try:
            fee = MembershipFee.objects.get(
                membership_type=self.membership_type,
                payment_mode=self.payment_frequency,
                is_active=True
            )
            return fee.amount
        except MembershipFee.DoesNotExist:
            return None


class Child(models.Model):
    """Children information for members"""
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='children',
        verbose_name="Parent Member"
    )
    name = models.CharField(max_length=200, verbose_name="Child's Name")
    date_of_birth = models.DateField(
        verbose_name="Date of Birth",
        blank=True,
        null=True
    )
    GENDER_CHOICES = [
        ('MALE', 'Male'),
        ('FEMALE', 'Female'),
        ('OTHER', 'Other'),
    ]
    gender = models.CharField(
        max_length=10,
        choices=GENDER_CHOICES,
        verbose_name="Gender",
        blank=True,
        null=True
    )
    
    class Meta:
        ordering = ['date_of_birth']
        verbose_name = "Child"
        verbose_name_plural = "Children"
    
    def __str__(self):
        return f"{self.name} (Child of {self.member.name})"


class MembershipFee(models.Model):
    """Membership fee structure"""
    membership_type = models.CharField(
        max_length=20,
        choices=[
            ('REGULAR', 'Regular'),
            ('LIFETIME', 'Lifetime Membership'),
        ],
        verbose_name="Membership Type"
    )
    PAYMENT_FREQUENCY_CHOICES = [
        ('ANNUAL', 'Annual'),
        ('MONTHLY', 'Monthly'),
    ]
    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_FREQUENCY_CHOICES,
        verbose_name="Payment Frequency"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Fee Amount"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description"
    )
    is_active = models.BooleanField(default=True, verbose_name="Active")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['membership_type', 'payment_mode']
        verbose_name = "Membership Fee"
        verbose_name_plural = "Membership Fees"
        unique_together = ['membership_type', 'payment_mode']
    
    def __str__(self):
        return f"{self.get_membership_type_display()} - {self.get_payment_mode_display()}: NPR {self.amount}"


class Payment(models.Model):
    """Revenue collection records"""
    member = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name="Member"
    )
    membership_fee = models.ForeignKey(
        MembershipFee,
        on_delete=models.PROTECT,
        related_name='payments',
        verbose_name="Fee Structure"
    )
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Payment Amount"
    )
    payment_date = models.DateField(default=timezone.now, verbose_name="Payment Date")
    
    PAYMENT_MODE_CHOICES = [
        ('CASH', 'Cash'),
        ('BANK_TRANSFER', 'Bank Transfer'),
        ('ONLINE', 'Online Payment'),
        ('CHEQUE', 'Cheque'),
    ]
    payment_mode = models.CharField(
        max_length=20,
        choices=PAYMENT_MODE_CHOICES,
        verbose_name="Payment Mode"
    )
    transaction_reference = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Transaction Reference"
    )
    receipt_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name="Receipt Number"
    )
    collected_by = models.CharField(
        max_length=100,
        blank=True,
        null=True,
        verbose_name="Collected By"
    )
    remarks = models.TextField(
        blank=True,
        null=True,
        verbose_name="Remarks"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-payment_date']
        verbose_name = "Payment"
        verbose_name_plural = "Payments"
    
    def __str__(self):
        return f"{self.receipt_number} - {self.member.name} - NPR {self.amount}"
    
    def save(self, *args, **kwargs):
        """Auto-generate receipt number and update member status"""
        # Generate receipt number if not provided
        if not self.receipt_number:
            from datetime import datetime
            date_str = datetime.now().strftime('%Y%m%d')
            last_payment = Payment.objects.filter(
                receipt_number__startswith=f'NSS-{date_str}'
            ).order_by('receipt_number').last()
            
            if last_payment:
                last_number = int(last_payment.receipt_number.split('-')[-1])
                new_number = last_number + 1
            else:
                new_number = 1
            
            self.receipt_number = f'NSS-{date_str}-{new_number:04d}'
        
        # Save the payment first
        super().save(*args, **kwargs)
        
        # Update member's payment status
        self.update_member_status()
    
    def update_member_status(self):
        """Update member's last payment date and membership validity"""
        member = self.member
        
        # Update last payment date
        member.last_payment_date = self.payment_date
        
        # Calculate membership validity
        if member.membership_type == 'LIFETIME':
            # Lifetime members never expire
            member.membership_valid_until = None
        else:
            # Regular members - calculate expiry based on payment frequency
            frequency = self.membership_fee.payment_mode  # ANNUAL or MONTHLY
            
            if frequency == 'MONTHLY':
                # Add 1 month
                member.membership_valid_until = self.payment_date + relativedelta(months=1)
            else:  # ANNUAL
                # Add 1 year
                member.membership_valid_until = self.payment_date + relativedelta(years=1)
        
        member.save()