from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken
from users.serializers import (
    LoginSerializer, RegisterSerializer, ResetPasswordSerializer, 
    UserSerializer, ProfileSerializer, UpdateProfileSerializer,
    UnifiedOrderSerializer
)
from drf_spectacular.utils import extend_schema
from rent.models import RentOrder, RentItem
from market.models import MarketOrder, MarketItem
from django.db.models import Sum
from users.models import User

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(description="Register a new user")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    @extend_schema(
        request=LoginSerializer,
        responses={200: dict, 400: str},
        description="Login with phone number and password"
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data.get('phone_number')
            password = serializer.validated_data.get('password')
            
            user = authenticate(username=phone_number, password=password)
            
            if user:
                login(request, user)
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': UserSerializer(user).data
                })
            return Response({'error': 'Username or password is not correct'}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordView(generics.CreateAPIView):
    serializer_class = ResetPasswordSerializer
    permission_classes = [AllowAny]

    @extend_schema(description="Request a password reset (sent to admin)")
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "result": "Sizning parolni tiklash so'rovingiz adminga muvaffaqiyatli yuborildi. Tez orada siz bilan bog'lanishadi."
        }, status=status.HTTP_201_CREATED)

class ProfileView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UpdateProfileView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

class UserOrdersView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: UnifiedOrderSerializer(many=True)},
        description="Get all orders (Rent and Market) for the current user"
    )
    def get(self, request):
        status_filter = request.query_params.get('status', 'all')
        
        rent_orders = RentOrder.objects.filter(user=request.user)
        market_orders = MarketOrder.objects.filter(user=request.user)
        
        combined = []
        
        for ro in rent_orders:
            image = ro.rent_item.images.first().image if ro.rent_item.images.exists() else None
            combined.append({
                'id': ro.id,
                'item_id': ro.rent_item.id,
                'type': 'rent',
                'name': ro.rent_item.name,
                'image': image,
                'size': ro.land_area,
                'date_time': ro.order_date,
                'status': 'active',
                'price': ro.rent_item.price
            })
            
        for mo in market_orders:
            combined.append({
                'id': mo.id,
                'item_id': mo.item.id,
                'type': 'market',
                'name': mo.item.name,
                'image': None, 
                'size': str(mo.quantity),
                'date_time': mo.delivery_date,
                'status': 'delivered', 
                'price': mo.item.price * mo.quantity
            })
            
        if status_filter != 'all':
            combined = [o for o in combined if o['status'] == status_filter]
            
        serializer = UnifiedOrderSerializer(combined, many=True, context={'request': request})
        return Response(serializer.data)

class UserListView(generics.ListCreateAPIView):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return User.objects.none()
        return super().get_queryset()

    def perform_create(self, serializer):
        user = serializer.save()
        password = self.request.data.get('password')
        if password:
            user.set_password(password)
            user.save()

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        if not self.request.user.is_staff:
            return User.objects.none()
        return super().get_queryset()

class DashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses={200: dict},
        description="Dashboard statistics for staff users"
    )
    def get(self, request):
        if not request.user.is_staff:
            return Response({"error": "Forbidden"}, status=403)

        users_count = User.objects.count()
        rent_orders_count = RentOrder.objects.count()
        market_orders_count = MarketOrder.objects.count()
        
        rent_items_count = RentItem.objects.count()
        market_items_count = MarketItem.objects.count()

        rent_revenue = RentOrder.objects.aggregate(total=Sum('rent_item__price'))['total'] or 0
        market_revenue = MarketOrder.objects.aggregate(total=Sum('item__price'))['total'] or 0
        
        return Response({
            "users_count": users_count,
            "orders_count": rent_orders_count + market_orders_count,
            "equipment_count": rent_items_count + market_items_count,
            "total_revenue": float(rent_revenue + market_revenue),
        })

class PublicStatsView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={200: dict},
        description="Publicly available general statistics"
    )
    def get(self, request):
        return Response({
            "users_count": User.objects.count(),
            "orders_count": RentOrder.objects.count() + MarketOrder.objects.count(),
            "equipment_count": RentItem.objects.count() + MarketItem.objects.count(),
        })
