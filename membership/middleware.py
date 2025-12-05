from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages


class ApprovalRequiredMiddleware:
    """
    Middleware to check if user is approved before allowing access
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
        # URLs that don't require approval
        self.public_urls = [
            '/login/',
            '/register/',
            '/logout/',
            '/static/',
            '/admin/',
            '/pending/',
        ]
    
    def __call__(self, request):
        # Allow public URLs
        if any(request.path.startswith(url) for url in self.public_urls):
            return self.get_response(request)
        
        # Allow unauthenticated users (they'll be redirected by @login_required)
        if not request.user.is_authenticated:
            return self.get_response(request)
        
        # Allow superusers and staff
        if request.user.is_superuser or request.user.is_staff:
            return self.get_response(request)
        
        # Check if user is approved
        if hasattr(request.user, 'profile'):
            if not request.user.profile.is_approved:
                # User is not approved - redirect to pending page
                if request.path != '/pending/':
                    messages.warning(request, 'Your account is pending admin approval.')
                    return redirect('/pending/')
        
        return self.get_response(request)