from rest_framework import serializers

class user_register_serializer(serializers.Serializer):
    email       = serializers.CharField()  
    first_name  = serializers.CharField()  
    last_name   = serializers.CharField()  
    password    = serializers.CharField()

class user_login_serializer(serializers.Serializer):
    email       = serializers.CharField(max_length = 255)
    password    = serializers.CharField(max_length = 255)


 