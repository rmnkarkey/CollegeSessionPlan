from django.shortcuts import render,get_object_or_404
from .forms import UserForm
from django.contrib.auth import authenticate,login as lg
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework.response import Response
from django.conf import settings
import jwt
import json
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,renderer_classes
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .models import CourseManagement,StudentManagement,GradeManagement,OfferedCourses,SessionNameTable,SessionCourseTable
from .serializers import SessionNameSerializer,CourseSerializer,StudentSerializer,GradeManagementSerializer,StatusTableSerializer,SessionNameTableSerializer,SessionCourseTableSerializer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets
from django.utils import timezone

@api_view(['POST'])
@permission_classes([AllowAny,])
def authenticate_users(request):
    username=request.data['username']
    print(username)
    password=request.data['password']
    user = authenticate(username=username,password=password)
    if user:
        try:
            payload=jwt_payload_handler(user)
            token=jwt.encode(payload,settings.SECRET_KEY)
            userDetails={}
            userDetails['username']=user.username
            userDetails['token']=token
            print(userDetails['token'])
            lg(request,user)
            return Response(userDetails,status=status.HTTP_200_OK)
        except Exception as e:
            raise e
    else:
        res={
            'error':'can not authenticate'
        }
        return Response(res)

def create_user(request):
    if request.POST:
        form=UserForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=User.objects.create_user(username=username,password=password)
            if user:
                return render(request,'login.html')
    else:
        form=UserForm()
        return render(request,'signup.html',{'form':form})

@api_view(['GET'])
def display(request):
    context={
        'user':'kokokok',
        'anything':'ajdhfkjh'
    }
    return Response(context)

class CourseView(APIView):
    def get(self,request):
        course=CourseManagement.objects.all()
        serilizer = CourseSerializer(course,many=True)
        return Response(serilizer.data)

    def post(self,request,*args,**kwargs):
        data =request.data
        print(data)
        print('............')
        serializer = CourseSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST  )

class StudentView(APIView):
    def get(self,request):
        student=StudentManagement.objects.all()
        serilizer = StudentSerializer(student,many=True)
        return Response(serilizer.data)

    def post(self,request,*args,**kwargs):
        data =request.data
        print(data)
        print('............')
        serializer = StudentSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_200_OK)
        else:
            return Response(serializer.errors,status = status.HTTP_400_BAD_REQUEST  )

@api_view(['GET','POST','DELETE'])
@permission_classes([AllowAny,])
def CourseDetail(request,course_code):
    if request.method=="GET":
        try:
            sub = CourseManagement.objects.get(course_code=course_code)
            if sub:
                response={
                'course_name':sub.course_name,
                'year':sub.year,
                'credit':sub.credit,
                'session':sub.session,
                'prerequisite':sub.prerequisite
                }
                return Response(response)
        except CourseManagement.DoesNotExist:
            return Response('Course not found')

    elif request.method=="POST":
        try:
            sub = CourseManagement.objects.get(course_code=course_code)
            if sub:
                instance = CourseManagement.objects.get(course_code=course_code)
                serializer = CourseSerializer(instance,data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data)
        except CourseManagement.DoesNotExist:
            return Response('Course not found')

    elif request.method=="DELETE":
        try:
            instance = CourseManagement.objects.get(course_code=course_code)
            if instance:
                instance.delete()
                return Response('Course Deleted')
        except CourseManagement.DoesNotExist:
            return Response("Course found")

@api_view(['GET','POST'])
def FormsFunction(request):
    if request.method=="GET":
        grades = GradeManagement.objects.all()
        sub = GradeManagementSerializer(grades,many=True)
        return Response(sub.data)

    elif request.method=="POST":
        univ = request.POST['university_id']
        cours = request.POST['course_code']
        marks = request.POST['marks']
        univ_id = StudentManagement.objects.get(university_id=univ)
        cours_id = CourseManagement.objects.get(course_code=cours)
        gradeMan = GradeManagement.objects.create(university_id=univ_id,course_code=cours_id,marks=int(marks))
        GradeObjects = GradeManagement.objects.all()
        status=''
        if univ_id:
            for i in GradeObjects:
                if univ_id==i.university_id:
                    status = i.status
        stat = StatusTable.objects.create(university_id=univ_id,course_code=cours_id,session=univ_id.enrolled_session,status=status)
        return Response("Grade Added Succesfull")

@api_view(['GET'])
def statFunction(request):
    stats = StatusTable.objects.all()
    stat = StatusTableSerializer(stats,many=True)
    return Response(stat.data)

def AvailableCourse(request):
    student = StudentManagement.objects.get(university_id=99)
    course = CourseManagement.objects.all()
    for j in course:
        if student.enrolled_session == j.session and student.current_year == j.year:
            print("{} {}".format(j.session,j.course_name))

def SearchFuction(request):
    if request.method=="POST":
        course_code = request.POST['course_code']
        course = CourseManagement.objects.get(course_code=course_code)
        return render(request,'search.html',{'course':course})
    else:
        return render(request,'search.html')

# def courseRegister(request):
#     if request.method=='POST':
#         pass
#     else:
#         course = SessionTable.objects.all()
#         return render(request,'register.html',{'course':course})

# @api_view(['GET'])
# def updateSession(request):
#     session = SessionTable.objects.all()
#     sessionSer = SessionTableSerializer(session,many=True)
#     return Response(sessionSer.data)

# @api_view(['GET','PUT',"DELETE"])
# def updateSessionView(request,id):
#     if request.method=="PUT":
#         # session = SessionTable.objects.get(id=id)
#         # session_name=request.data['session_name']
#         # session_year=request.data['session_year']
#         # session_session=request.data['session_session']
#         # max_credit=request.data['max_credit']
#         # courseCode=request.data['courseCode']
#         # session_credit=request.data['session_credit']
#         # Offered=request.data['Offered']
#         #
#         try:
#             session = SessionTable.objects.get(id=id)
#             if session:
#                 instance = SessionTable.objects.get(id=id)
#                 serializer = SessionTableSerializer(instance,data=request.data)
#                 if serializer.is_valid():
#                     serializer.save()
#                     return Response(serializer.data)
#         except SessionTable.DoesNotExist:
#             return Response('Not found')
#
#     elif request.method=="DELETE":
#         try:
#             instance = SessionTable.objects.get(id=id)
#             if instance:
#                 instance.delete()
#                 return Response('Session Deleted')
#         except SessionTable.DoesNotExist:
#             return Response("session not found")
#
#     else:
#         try:
#             session = SessionTable.objects.get(id=id)
#             code = session.courseCode
#             if session:
#                 response={
#                 'session_name':session.session_name,
#                 'session_year':session.session_year,
#                 'session_session':session.session_session,
#                 'max_credit':session.max_credit,
#                 'courseCode':str(code),
#                 'session_course_credit':session.course_credit,
#                 'Offered':session.Offered,
#                 }
#                 return Response(response)
#         except SessionTable.DoesNotExist:
#             return Response('Not found')

#search Function for session
@api_view(['GET','POST'])
def sessionPlan(request):
    if request.method == "POST":
        session = request.data['session']
        matchSession = OfferedCourses.objects.filter(session = session)
        courseSession=[]
        availableCourse=[]
        courseCode=[]
        courseCredit=[]
        for i in matchSession:
            availableCourse.append(i.courseCode.course_name)
            courseCode.append(i.courseCode.course_code)
            course = CourseManagement.objects.get(course_code=i.courseCode.course_code)
            courseCredit.append(course.credit)
        dictionary ={'session':session,'availableCourse':availableCourse,'courseCode':courseCode,'courseCredit':courseCredit}
        if matchSession:
            return Response(dictionary)
        else:
            return Response("not found")
    else:
        session = SessionNameTable.objects.all()
        sessionSer = SessionNameTableSerializer(session,many=True)
        return Response(sessionSer.data)


@api_view(['GET','POST'])
def InsertSessionName(request):
    if request.method=='POST':
        session_name=request.data['session_name']
        session_year=request.data['session_year']
        date_created=timezone.now().date()
        max_credit=request.data['max_credit']
        start_date=request.data['start_date']
        end_date=request.data['end_date']
        session_name=SessionNameTable.objects.create(session_name=session_name,session_year=session_year,date_created=date_created,max_credit=max_credit,start_date=start_date,end_date=end_date)
        return Response("Succesfully Saved")
    else:
        session = SessionNameTable.objects.all()
        sessionSer = SessionNameTableSerializer(session,many=True)
        return Response(sessionSer.data)

@api_view(['GET','POST'])
def InsertSessionNameDetail(request,session_name):
    if request.method=="POST":
        session = SessionNameTable.objects.get(session_name=session_name)
        # print(session.session_name)
        session_session=request.data['session_session']
        offer = request.data.get('checkBox')
        courseCode = request.data.get('courseCode')
        print('................')
        print(courseCode)
        print('................')
        course=''
        for j in courseCode:
            course = CourseManagement.objects.get(course_code=j)
            print(course.credit)
            if course.course_code == j:
                course_session = SessionCourseTable.objects.create(session_name_id=session.session_name,session_session=session_session,courseCode_id=course.course_code,course_credit=course.credit,Offered="Yes")
        return Response('saved')
    else:
        session = SessionCourseTable.objects.all()
        sessionSer = SessionCourseTableSerializer(session,many=True)
        return Response(sessionSer.data)

@api_view(['GET'])
def listOfSession(request):
    if request.method=="GET":
        session = SessionNameTable.objects.all()
        sessionSer = SessionNameSerializer(session,many=True)
        return Response(sessionSer.data)

@api_view(['GET'])
def SearchSessionNameDetail(request,session_name):
    session = SessionCourseTable.objects.filter(session_name=session_name)
    courseCodeList=[]
    courseCredit=[]
    for i in session:
        courseCode=i.courseCode.course_name
        course_credit=i.course_credit
        # course=CourseManagement.objects.filter(course_code=courseCode)
        # for i in course:
        courseCodeList.append(courseCode)
        courseCredit.append(course_credit)
        # print(courseCodeList)
    #     dictionary={
    #         'courseCode':courseCode,
    #         'course_credit':course_credit
    #         }
    # datas = json.dumps(dictionary)
    return Response(courseCodeList)

# @api_view(['GET','POST'])
# def saveFunction(request):
#     if request.method=="POST":
#         session = request.data['session']
#         # print(session)
#         # print('... .')
#         # offer = request.POST.get('checkBox', False)
#         offer = request.data.get('checkBox')
#         # offer = request.data.getlist('checkBox')
#         # print(offer,'........')
#         sessionName = request.data['session_name']
#         # print(sessionName)
#         sessionYear = request.data['session_year']
#         # print(sessionYear)
#         # sessionCredit = request.data['courseCredit']
#         maxCredit = request.data['max_credit']
#         # print(maxCredit)
#         startDate = request.data['startdate']
#         # print(startDate)
#         deadline = request.data['deadline']
#         # print(deadline)
#         # print(',,,,,')
#         matchSession = OfferedCourses.objects.filter(session = session)
#         # print(matchSession)
#         # print('....')
#         availableCourse=[]
#         for i in matchSession:
#             availableCourse.append(i.courseCode.course_code)
#         courseCode = request.data.get('course_code')
#         print(courseCode)
#         course=''
#         for i in courseCode:
#             course = CourseManagement.objects.get(course_code=i)
#         # a=course.course_code
#         for j in courseCode:
#             for i in offer:
#                 course = CourseManagement.objects.get(course_code=i)
#                 print(course.credit)
#                 if course.course_code == i:
#                     off = SessionTable.objects.create(max_credit=int(maxCredit),courseCode_id=course.course_code,session_name=sessionName,session_year=sessionYear,session_session=session,course_credit=int(course.credit),Offered="Yes")
#                 else:
#                     off = SessionTable.objects.create(max_credit=int(maxCredit),courseCode_id=course.course_code,session_name=sessionName,session_year=sessionYear,session_session=session,course_credit=int(course.credit),Offered="No")
#             break
#         return Response("success")
#     else:
#         session = SessionTable.objects.all()
#         sessionSer = SessionTableSerializer(session,many=True)
#         return Response(sessionSer.data)
#
# @api_view(['GET','POST'])
