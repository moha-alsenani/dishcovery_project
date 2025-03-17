from dishcovery.models import Cuisine

def cuisine_context(request):
    return {'cuisines': Cuisine.objects.all()}  
