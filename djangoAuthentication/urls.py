from django.urls import path,include
from . import views
from django.views.decorators.csrf import csrf_exempt
from rest_framework.routers import DefaultRouter
#
# router = DefaultRouter()
# router.register('apis/',views.subfirebaseView,base_name='subfirebaseView')

urlpatterns=[
    path('login/',csrf_exempt(views.authenticate_users),name='login'),
    path('signup/',csrf_exempt(views.create_user),name='signup'),
    # path('api/',include(router.urls)),
    path('courses/',views.CourseView.as_view(),name='course'),
    path('courses/<slug:course_code>/',views.CourseDetail,name='courseDetail'),
    path('student/',views.StudentView.as_view()),
    # path('subb/<int:id>/',views.subDetail,name='subdetail'),
    path('forms/',views.FormsFunction,name='FormsFunction'),
    path('stats/',views.statFunction,name='statFunction'),
    path('available/',views.AvailableCourse,name='available'),
    path('course-search/',views.SearchFuction,name='SearchFuction')
]
