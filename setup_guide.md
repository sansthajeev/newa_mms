# Newa Samparka Samuha - Complete Setup & Deployment Guide

## 📦 What You Have

A complete Django membership management system with:
- ✅ Member management (primary & secondary info)
- ✅ Children tracking
- ✅ Payment recording with auto-receipt generation
- ✅ Revenue reports and analytics
- ✅ Beautiful responsive web interface
- ✅ Admin panel for data management
- ✅ Print-friendly receipt templates

## 📂 Project Files Overview

```
newa_samparka_samuha/
├── README.md                       # Complete documentation
├── QUICKSTART.md                   # Quick start guide
├── requirements.txt                # Python dependencies
├── manage.py                       # Django management script
├── db.sqlite3                      # Database (created after migration)
│
├── newa_samparka_samuha/          # Project settings
│   ├── settings.py                # Configuration
│   ├── urls.py                    # URL routing
│   └── wsgi.py                    # WSGI config
│
└── membership/                     # Main application
    ├── models.py                  # Database models (Member, Payment, etc.)
    ├── admin.py                   # Admin interface configuration
    ├── views.py                   # Business logic
    ├── urls.py                    # App URLs
    ├── templates/                 # HTML templates
    │   └── membership/
    │       ├── base.html          # Base layout
    │       ├── home.html          # Dashboard
    │       ├── member_list.html   # Members listing
    │       ├── member_detail.html # Member details
    │       ├── payment_list.html  # Payments listing
    │       ├── payment_receipt.html # Receipt template
    │       └── revenue_report.html # Revenue reports
    └── migrations/                # Database migrations
```

## 🖥️ System Requirements

### Minimum Requirements
- **OS**: Windows, macOS, or Linux
- **Python**: 3.8 or higher
- **RAM**: 2GB minimum
- **Disk Space**: 100MB for application + database

### Recommended for Production
- **OS**: Ubuntu Server 20.04+ or Windows Server
- **Python**: 3.10+
- **RAM**: 4GB+
- **Database**: PostgreSQL 12+ (for production)
- **Web Server**: Nginx or Apache
- **SSL**: Let's Encrypt certificate

## 🚀 Installation Steps

### Step 1: Extract the Project
```bash
# Extract the downloaded folder
unzip newa_samparka_samuha.zip
cd newa_samparka_samuha
```

### Step 2: Install Python (if not installed)

**Windows:**
1. Download Python from https://python.org
2. Run installer, check "Add Python to PATH"
3. Open Command Prompt and verify:
   ```
   python --version
   ```

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip
```

### Step 3: Create Virtual Environment (Recommended)
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/Mac:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 4: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 5: Initialize Database
```bash
python3 manage.py migrate
```

### Step 6: Create Admin User
```bash
python3 manage.py createsuperuser
```
Follow prompts to create your admin account.

**Or use pre-configured admin:**
- Username: `admin`
- Password: `admin123`

### Step 7: Run Development Server
```bash
python3 manage.py runserver
```

### Step 8: Access the Application
Open browser and visit:
- **Main App**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/

## 🎯 Initial Configuration

### 1. Setup Fee Structures (IMPORTANT - Do This First!)
Before adding members or recording payments:

1. Login to Admin Panel
2. Go to **Membership → Membership Fees**
3. Add these fee structures:

| Membership Type | Payment Mode  | Amount      |
|----------------|---------------|-------------|
| Regular        | Cash          | NPR 500.00  |
| Regular        | Bank Transfer | NPR 500.00  |
| Regular        | Online        | NPR 500.00  |
| Regular        | Cheque        | NPR 500.00  |
| Lifetime       | Cash          | NPR 5000.00 |
| Lifetime       | Bank Transfer | NPR 5000.00 |
| Lifetime       | Online        | NPR 5000.00 |
| Lifetime       | Cheque        | NPR 5000.00 |

### 2. Customize Organization Details
Edit `membership/templates/membership/payment_receipt.html`:
- Update organization address
- Add logo (optional)
- Modify footer information

### 3. Test with Sample Data
Add a test member and record a payment to verify everything works.

## 🌐 Production Deployment

### Option 1: Deploy on Your Own Server

#### Using Gunicorn + Nginx (Linux)

1. **Install Gunicorn:**
```bash
pip install gunicorn
```

2. **Create Gunicorn service file:**
```bash
sudo nano /etc/systemd/system/newa_samparka.service
```

Add:
```ini
[Unit]
Description=Newa Samparka Samuha
After=network.target

[Service]
User=your_username
Group=www-data
WorkingDirectory=/path/to/newa_samparka_samuha
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:8000 newa_samparka_samuha.wsgi:application

[Install]
WantedBy=multi-user.target
```

3. **Start service:**
```bash
sudo systemctl start newa_samparka
sudo systemctl enable newa_samparka
```

4. **Configure Nginx:**
```bash
sudo nano /etc/nginx/sites-available/newa_samparka
```

Add:
```nginx
server {
    listen 80;
    server_name your_domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }
    
    location /static/ {
        root /path/to/newa_samparka_samuha;
    }

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

5. **Enable site:**
```bash
sudo ln -s /etc/nginx/sites-available/newa_samparka /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

### Option 2: Deploy on PythonAnywhere (Easy)

1. Create account at https://www.pythonanywhere.com
2. Upload project files
3. Create virtual environment
4. Configure WSGI file
5. Set static files path
6. Done! Your app is live

### Option 3: Deploy on Heroku

1. Install Heroku CLI
2. Create `Procfile`:
```
web: gunicorn newa_samparka_samuha.wsgi
```
3. Create `runtime.txt`:
```
python-3.11.0
```
4. Deploy:
```bash
heroku create your-app-name
git push heroku main
heroku run python manage.py migrate
```

## 🔒 Security Checklist for Production

- [ ] Change SECRET_KEY in settings.py
- [ ] Set DEBUG = False
- [ ] Update ALLOWED_HOSTS with your domain
- [ ] Use PostgreSQL instead of SQLite
- [ ] Set up SSL certificate (HTTPS)
- [ ] Configure firewall
- [ ] Regular database backups
- [ ] Update dependencies regularly
- [ ] Use environment variables for sensitive data
- [ ] Enable CSRF protection
- [ ] Set up proper logging

## 💾 Backup & Restore

### Backup Database
```bash
# Create backup
python3 manage.py dumpdata > backup_$(date +%Y%m%d_%H%M%S).json

# Or backup just membership data
python3 manage.py dumpdata membership > membership_backup.json
```

### Restore Database
```bash
python3 manage.py loaddata backup_file.json
```

### Automated Backups (Linux)
Create a cron job:
```bash
crontab -e
```

Add:
```
0 2 * * * cd /path/to/project && python3 manage.py dumpdata > backups/backup_$(date +\%Y\%m\%d).json
```

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'django'"
**Solution:** Install dependencies: `pip install -r requirements.txt`

### Issue: "Database is locked"
**Solution:** 
- Close all connections to database
- Restart server
- Consider using PostgreSQL for production

### Issue: Static files not loading
**Solution:** 
```bash
python3 manage.py collectstatic
```

### Issue: Port 8000 already in use
**Solution:** 
```bash
# Use different port
python3 manage.py runserver 8080

# Or find and kill process using port 8000
# Linux/Mac:
lsof -ti:8000 | xargs kill -9
# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

### Issue: Permission denied
**Solution:** 
- Check file permissions
- Run with sudo (not recommended)
- Change ownership: `sudo chown -R $USER:$USER .`

## 📊 Monitoring & Maintenance

### Check System Health
```bash
# Check if service is running
sudo systemctl status newa_samparka

# View logs
sudo journalctl -u newa_samparka -f

# Check database size
du -h db.sqlite3
```

### Update Application
```bash
# Pull latest code
git pull origin main

# Update dependencies
pip install -r requirements.txt --upgrade

# Run migrations
python3 manage.py migrate

# Restart service
sudo systemctl restart newa_samparka
```

## 📞 Support & Resources

### Documentation
- Full README: See README.md
- Quick Start: See QUICKSTART.md
- Django Docs: https://docs.djangoproject.com/

### Community
- Django Forum: https://forum.djangoproject.com/
- Stack Overflow: Tag with 'django'
- Python Discord: https://discord.gg/python

## 📝 Customization Guide

### Add New Fields to Member
1. Edit `membership/models.py`
2. Add field to Member model
3. Run migrations:
   ```bash
   python3 manage.py makemigrations
   python3 manage.py migrate
   ```
4. Update admin.py to show new field

### Change Colors/Styling
Edit Bootstrap classes in templates:
- `bg-primary` → `bg-success` (change colors)
- Modify `templates/membership/base.html` for global styles

### Add New Report
1. Create view in `views.py`
2. Add URL in `urls.py`
3. Create template in `templates/membership/`

## 🎓 Training Your Team

### For Admin Users
1. Show admin panel navigation
2. Demonstrate adding members
3. Show payment recording process
4. Explain receipt printing
5. Walk through reports

### For Regular Users
1. Dashboard overview
2. Search and filter members
3. View member details
4. Access reports

## 📋 Best Practices

1. **Regular Backups**: Daily automated backups
2. **Test Changes**: Use development environment first
3. **Document Modifications**: Keep change log
4. **Update Regularly**: Security patches
5. **Monitor Performance**: Check server resources
6. **User Training**: Regular training sessions
7. **Data Validation**: Review data periodically

## 🚦 Going Live Checklist

- [ ] All fee structures configured
- [ ] Admin account secured (strong password)
- [ ] Test member added successfully
- [ ] Test payment recorded successfully
- [ ] Receipt printing works
- [ ] Reports generate correctly
- [ ] Backup system configured
- [ ] Production settings applied
- [ ] SSL certificate installed
- [ ] Domain configured
- [ ] Team trained
- [ ] Documentation accessible

---

## 🎉 You're All Set!

Your Newa Samparka Samuha membership management system is ready to use!

**Next Steps:**
1. Complete initial configuration
2. Train your team
3. Import existing member data (if any)
4. Start recording memberships and payments!

**Need Help?** 
Refer to README.md for detailed documentation or QUICKSTART.md for quick reference.

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Platform**: Django 6.0 + Python 3.12 + Bootstrap 5