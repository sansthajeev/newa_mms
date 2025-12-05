# Quick Start Guide - Newa Samparka Samuha

## 🚀 Getting Started in 5 Minutes

### Step 1: Install Dependencies (1 minute)
```bash
pip install -r requirements.txt --break-system-packages
```

### Step 2: Setup Database (1 minute)
```bash
cd newa_samparka_samuha
python3 manage.py migrate
```

### Step 3: Create Admin User (1 minute)
**Option A - Quick Setup (Use existing credentials):**
- Username: `admin`
- Password: `admin123`

**Option B - Create Your Own:**
```bash
python3 manage.py createsuperuser
```

### Step 4: Run Server (30 seconds)
```bash
python3 manage.py runserver
```

### Step 5: Access Application (30 seconds)
Open your browser and visit:
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

---

## 📝 First Steps After Login

### 1. Setup Fee Structure (Required First!)
1. Go to Admin Panel
2. Navigate to: **Membership → Membership Fees**
3. Add fee structures:
   - **Regular - Cash**: NPR 500.00
   - **Regular - Bank Transfer**: NPR 500.00
   - **Lifetime - Cash**: NPR 5,000.00
   - **Lifetime - Bank Transfer**: NPR 5,000.00

### 2. Add Your First Member
1. Go to: **Membership → Members**
2. Click "**Add Member**"
3. Fill in the form:
   - Name: John Doe
   - Phone: +9779841234567
   - Email: john@example.com
   - Permanent Address: Kathmandu, Nepal
   - Current Address: Kathmandu, Nepal
   - Father's Name: Father Name
   - Mother's Name: Mother Name
   - Citizenship Number: 12345678
   - Membership Type: Regular
4. Click "**Save**"
   - Membership Number will be auto-generated!

### 3. Record First Payment
1. Go to: **Membership → Payments**
2. Click "**Add Payment**"
3. Fill in:
   - Member: Select "John Doe"
   - Membership Fee: Select "Regular - Cash"
   - Amount: 500.00
   - Payment Mode: Cash
   - Collected By: Your Name
4. Click "**Save**"
   - Receipt Number will be auto-generated!

### 4. View Dashboard
1. Go to main homepage: http://127.0.0.1:8000/
2. You'll see:
   - Total members: 1
   - Total revenue: NPR 500.00
   - Recent members and payments

---

## 🎯 Common Tasks

### Add Multiple Members
Use the admin panel to add members one by one or use Django shell for bulk import.

### Generate Reports
1. Click "**Reports**" in navigation
2. Select date range
3. Click "**Generate Report**"
4. View revenue breakdown by mode and type
5. Click "**Print**" to print

### Print Receipt
1. Go to **Payments** list
2. Find the payment
3. Click "**Receipt**" button
4. Click "**Print Receipt**"

### Search Members
1. Go to **Members** page
2. Use search box to search by:
   - Name
   - Membership Number
   - Phone
   - Email
3. Use filters for:
   - Membership Type
   - Active/Inactive Status

---

## 💡 Pro Tips

1. **Auto-Generated Numbers**: 
   - Membership Numbers: NSS-MEM-00001, NSS-MEM-00002, etc.
   - Receipt Numbers: NSS-20241205-0001, NSS-20241205-0002, etc.

2. **Add Children**: 
   - Edit any member
   - Scroll to "Children" section
   - Click "Add another Child"

3. **Quick Actions**: 
   - Use dashboard quick action buttons
   - Access admin panel for advanced features

4. **Member History**: 
   - Click on any member name
   - View complete payment history
   - See total amount paid

---

## 📱 Navigation Guide

### Main Website
```
Home (/)
├── Dashboard with statistics
├── Quick action buttons
├── Recent members
└── Recent payments

Members (/members/)
├── Search and filter
├── List all members
└── View member details

Payments (/payments/)
├── Filter by date and mode
├── List all payments
└── Print receipts

Reports (/reports/revenue/)
├── Date range selection
├── Revenue breakdown
└── Detailed transactions
```

### Admin Panel (/admin/)
```
Membership
├── Members (Add, Edit, Delete)
├── Children (Linked to members)
├── Membership Fees (Fee structures)
└── Payments (Record payments)
```

---

## ❓ Quick FAQ

**Q: How do I change admin password?**
A: Go to Admin Panel → Users → admin → Change password

**Q: Can I have multiple membership types?**
A: Yes, currently supports Regular and Lifetime. Can be extended in models.py

**Q: How to backup data?**
A: Run: `python3 manage.py dumpdata > backup.json`

**Q: How to restore backup?**
A: Run: `python3 manage.py loaddata backup.json`

**Q: Can I customize receipt template?**
A: Yes, edit: `membership/templates/membership/payment_receipt.html`

---

## 🎓 Learning Resources

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap 5 Docs: https://getbootstrap.com/docs/5.3/
- Python Tutorial: https://docs.python.org/3/tutorial/

---

**Need Help?** Check the full README.md for detailed documentation!

**System Version**: 1.0.0  
**Quick Start Updated**: December 2025