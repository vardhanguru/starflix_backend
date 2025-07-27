from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from .models import CustomUser
import json

@csrf_exempt
def login_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            token, created = Token.objects.get_or_create(user=user)
            return JsonResponse({'token': token.key})
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return JsonResponse({'error': 'Method not allowed'}, status=405)

class UserProfileView(APIView):
    def get(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # Build absolute URL for profile image
        profile_image_url = ''
        if user.profile_image:
            profile_image_url = request.build_absolute_uri(user.profile_image.url)
        
        data = {
            'username': user.username,
            'email': user.email,
            'fname': user.fname,
            'lastname': user.lastname,
            'country': user.country,
            'state': user.state,
            'profile_image': profile_image_url
        }
        return JsonResponse(data)

    def put(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        data = request.data
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        user.fname = data.get('fname', user.fname)
        user.lastname = data.get('lastname', user.lastname)
        user.country = data.get('country', user.country)
        user.state = data.get('state', user.state)
        
        if 'profile_image' in request.FILES:
            user.profile_image = request.FILES['profile_image']
        
        user.save()
        
        # Build absolute URL for updated profile image
        profile_image_url = ''
        if user.profile_image:
            profile_image_url = request.build_absolute_uri(user.profile_image.url)
        
        return JsonResponse({
            'username': user.username,
            'email': user.email,
            'fname': user.fname,
            'lastname': user.lastname,
            'country': user.country,
            'state': user.state,
            'profile_image': profile_image_url
        })

class ChangePasswordView(APIView):
    def post(self, request):
        user = request.user
        if not user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        data = request.data
        old_password = data.get('old_password')
        new_password = data.get('new_password')
        confirm_password = data.get('confirm_password')
        if not user.check_password(old_password):
            return JsonResponse({'error': 'Old password is incorrect'}, status=400)
        if new_password != confirm_password:
            return JsonResponse({'error': 'New password and confirm password do not match'}, status=400)
        user.set_password(new_password)
        user.save()
        return JsonResponse({'message': 'Password changed successfully'})