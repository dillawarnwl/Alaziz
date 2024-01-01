from .models import DonorRegister

def user_image(request):
    user_image_url = None

    if request.user.is_authenticated:
        try:
            user_data = DonorRegister.objects.get(user=request.user)
            user_image_url = user_data.img.url if user_data.img else None
        except DonorRegister.DoesNotExist:
            user_image_url = None  
    return {'user_image_url': user_image_url}
