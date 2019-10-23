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
    path('courses/',views.CourseView.as_view(),name='course'),
    path('all-courses/',views.courseLists),
    path('registered/<slug:course_code>/',views.registerdUsersOnCourse),
    path('grades/',views.postGrade),
    path('courses/<slug:course_code>/',views.CourseDetail,name='courseDetail'),
    path('student-grade/<slug:course_name>/',views.particularStudentResult),
    path('student/',views.StudentView),
    path('forms/',views.FormsFunction,name='FormsFunction'),
    path('stats/',views.statFunction,name='statFunction'),
    path('available/',views.AvailableCourse,name='available'),
    path('course-search/',views.SearchFuction,name='SearchFuction'),
    path('session-plan/',views.sessionPlan,name='sessionPlan'),
    path('session-name-insert/<slug:session_name>/',views.InsertSessionNameDetail,name='InsertSessionNameDetail'),
    path('session-name-search/<slug:session_name>/',views.SearchSessionNameDetail,name='InsertSessionNameDetail'),
    path('session-name/',views.InsertSessionName),
    path('session-names/',views.listOfSession,name='listOfSession'),
    path('App/sessions', views.SessionManagement.as_view()),
    path('counter/',views.clickFunctionEvent),
    path('logout/',views.logoutFunction),
    path('profile/', views.studentProfile),
    path('usercourse/', views.SpecificCourse),
]
