from django.conf.urls import url, include
from rest_framework import routers
from views import UserViewSet, GroupViewSet, CaseViewSet, ResultViewSet, FlowViewSet, SuiteViewSet, AuthViewSet, \
    ObtainAuthToken, AuthScript1ViewSet, PlanViewSet

router = routers.DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'case', CaseViewSet)
router.register(r'result', ResultViewSet)
router.register(r'flow', FlowViewSet)
router.register(r'suite', SuiteViewSet)
router.register(r'auth', AuthViewSet)
router.register(r'auth_s', AuthScript1ViewSet)
router.register(r'plans',PlanViewSet)

# Wire up our API using automatic URL routing.
#  Additionally, we include login URLs for the browseable API.
urlpatterns = [
    url(r'^api/', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api-token-auth/', ObtainAuthToken.as_view()),
]
