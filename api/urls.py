from rest_framework.routers import SimpleRouter

from OrderManagement import config
from api.views import ApiViewSet

router = SimpleRouter()


urlpatterns = router.urls
for k, v in config.__dict__.items():
    if '__' not in k and 'serializers' not in k:
        print('/serve/' + v.get('url') + "/" + ' has been initialized')
        router.register(r'' + v.get("url"), ApiViewSet, basename=v.get("url"))
