from rest_framework import serializers
from .models import CourseManagement,StudentManagement,GradeManagement,StatusTable,SessionTable
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

class SessionTableSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionTable
        fields = '__all__'
