from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
# Create your views here.
class Demo(APIView):
    permission_classes = [AllowAny] 
    def get(self,req):
        print(req)
        print("hi")
        return Response({"msg":"ok is this drf?"})

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        if response.status_code == 200:
            refresh_token = response.data.get('refresh')
            # Set refresh token in httponly cookie
            response.set_cookie(
            key='refresh_token_user',
            value=refresh_token,
            httponly=True,
            secure=True,     # okay for localhost
            samesite='None',   # ✅ use Lax for local
            path='/',
            max_age=7*24*60*60
        )

            del response.data['refresh']

        return response
    
class CustomTokenRefreshView(APIView):
    authentication_classes = []  # 🚀 no auth required
    permission_classes = [] 
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('refresh_token_user')

        if refresh_token is None:
            return Response({'detail': 'No refresh token in cookie'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            refresh = RefreshToken(refresh_token)
            access_token = str(refresh.access_token)

            response = Response({'access': access_token}, status=200)

            # OPTIONAL: rotate refresh token & set new cookie
            new_refresh = str(refresh)
            response.set_cookie(
                key='refresh_token_user',
                value=new_refresh,
                httponly=True,
                secure=True,  # enable in production
                samesite='None',
                max_age=7 * 24 * 60 * 60,
            
                path='/',
            )
            return response

        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class LogoutView(APIView):
    permission_classes = []  # no auth required

    def post(self, request):
        response = Response({"detail": "Logged out"}, status=200)
        # Delete refresh token cookie
        response.delete_cookie(
            key="refresh_token_user",
            path="/",
            samesite='None',  # matches original cookie
            httponly=True,    # optional, but recommended
        )
        return response
