from django.shortcuts import render,get_object_or_404
from .forms import UserForm
from django.contrib.auth import authenticate,login as lg
from django.contrib.auth.models import User
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework.response import Response
from django.conf import settings
import jwt
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.decorators import api_view,permission_classes,renderer_classes
from rest_framework import status
from rest_framework.renderers import JSONRenderer
from .models import CourseManagement,StudentManagement,GradeManagement,StatusTable,DeadLine,OfferedCourses,SessionTable
from .serializers import CourseSerializer,StudentSerializer,GradeManagementSerializer,StatusTableSerializer
from rest_framework.parsers import JSONParser
from rest_framework import viewsets

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

def sessionPlan(request):
    if 'One' in request.POST:
        session = request.POST['session']
        sessionName = request.POST['session_name']
        sessionYear = request.POST['session_year']
        maxCredit = request.POST['max_credit']
        matchSession = OfferedCourses.objects.filter(session = session)
        availableCourse=[]
        courseSession=[]
        courseCode=[]
        courseCredit=[]
        for i in matchSession:
            availableCourse.append(i.courseCode.course_name)
            courseCode.append(i.courseCode.course_code)
            course = CourseManagement.objects.get(course_code=i.courseCode.course_code)
            courseCredit.append(course.credit)
        return render(request,'session.html',{'maxCredit':maxCredit,'session':session,'sessionName':sessionName,'sessionYear':sessionYear,'yes':'Yes','availableCourse':availableCourse,'courseCode':courseCode,'courseSession':courseSession,'courseCredit':courseCredit})
    elif 'Two' in request.POST:
        session = request.POST['session']
        offer = request.POST.getlist('checkBox')
        sessionName = request.POST['session_name']
        sessionYear = request.POST['session_year']
        sessionCredit = request.POST['courseCredit']
        maxCredit = request.POST['max_credit']
        matchSession = OfferedCourses.objects.filter(session = session)
        availableCourse=[]
        for i in matchSession:
            availableCourse.append(i.courseCode.course_code)
        courseCode = request.POST.getlist('course_code')
        course=''
        for i in courseCode:
            course = CourseManagement.objects.get(course_code=i)
        a=course.course_code
        for j in courseCode:
            for i in offer:
                course = CourseManagement.objects.get(course_code=i)
                print(course.credit)
                if course.course_code == i:
                    off = SessionTable.objects.create(max_credit=int(maxCredit),courseCode_id=course.course_code,session_name=sessionName,session_year=sessionYear,session_session=session,session_credit=int(course.credit),Offered="Yes")
                else:
                    off = SessionTable.objects.create(max_credit=int(maxCredit),courseCode_id=course.course_code,session_name=sessionName,session_year=sessionYear,session_session=session,session_credit=int(course.credit),Offered="No")
            break
        return render(request,'session.html',{'two':session})
    else:
        return render(request,'session.html')
