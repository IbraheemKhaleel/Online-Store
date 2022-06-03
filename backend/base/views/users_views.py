from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

from base.models import User
from base.serializers import UserSerializerWithToken, UserSerializer


@api_view(['POST'])
def userRegistration(request):
    data = request.data
    is_staff = request.data.get('is_staff', False)
    try:
        user = User.objects.create_user(first_name=data['name'], email=data['email'],username=data['username'],
                                        password=data['password'], is_staff=is_staff)
        serializer = UserSerializerWithToken(user, many=False).data
        return Response(serializer)
    except Exception as e:
        message = {'message': 'The email should be unique'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def GetAllUsers(request):
    if request.user.is_superuser:
        user_details = User.objects.filter(is_active=True)
        serializer_data = UserSerializer(user_details, many=True).data
        return Response({
            'message': 'User details successfully fetched by admin',
            'status_code': 200,
            'data': serializer_data
        })
    return Response({
        'message': 'This data only authorized by admin',
        'status_code': 403,
        'data': []
    })


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
        If you want to add data outside token
         """

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user)

        for key, value in serializer.data.items():
            data[key] = value

        return data


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer
