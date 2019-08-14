from rest_framework import serializers
from .models import CourseManagement,StudentManagement,GradeManagement,StatusTable,SessionNameTable,SessionCourseTable
from rest_framework.serializers import HyperlinkedIdentityField

class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseManagement
        fields = '__all__'

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudentManagement
        fields= '__all__'

class GradeManagementSerializer(serializers.ModelSerializer):
    class Meta:
        model = GradeManagement
        fields = '__all__'

class StatusTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusTable
        fields= '__all__'

class SessionNameTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionNameTable
        fields= '__all__'

class SessionCourseTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionCourseTable
        fields= '__all__'

class SessionNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionNameTable
        fields= ['session_name']
