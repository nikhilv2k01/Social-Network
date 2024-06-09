from rest_framework import generics, status, permissions, throttling
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, LoginSerializer, FriendRequestSerializer
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .models import FriendRequest, User

# Create your views here.


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(
            email=serializer.validated_data["email"].lower(),
            password=serializer.validated_data["password"],
        )
        if user:
            refresh = RefreshToken.for_user(user)
            return Response(
                {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                }
            )
        return Response(
            {"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED
        )


class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        keyword = self.request.query_params.get("search", "").lower()
        if "@" in keyword:
            return User.objects.filter(email__iexact=keyword)
        return User.objects.filter(
            Q(username__icontains=keyword) | Q(email__icontains=keyword)
        )


class SendFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [throttling.ScopedRateThrottle]
    throttle_scope = "burst"

    def post(self, request, *args, **kwargs):
        to_user_id = request.data.get("to_user_id")

        # Validate to_user_id
        if not to_user_id:
            return Response(
                {"error": "to_user_id is required"}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            to_user = User.objects.get(id=to_user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except ValueError:
            return Response(
                {"error": "Invalid user ID format"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Create the friend request
        FriendRequest.objects.create(from_user=request.user, to_user=to_user)
        return Response(
            {"message": "Friend request sent"}, status=status.HTTP_201_CREATED
        )


class RespondFriendRequestView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request_id = request.data.get("request_id")
        action = request.data.get("action")
        friend_request = FriendRequest.objects.get(id=request_id)

        if friend_request.to_user != request.user:
            return Response(
                {"error": "Not authorized"}, status=status.HTTP_403_FORBIDDEN
            )

        if action == "accept":
            friend_request.status = "accepted"
        elif action == "reject":
            friend_request.status = "rejected"

        friend_request.save()
        return Response({"message": f"Friend request {action}ed"})


class ListFriendsView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        friend_requests = user.sent_requests.filter(status="accepted")
        friend_ids = friend_requests.values_list("to_user_id", flat=True)
        return User.objects.filter(id__in=friend_ids)


class ListPendingRequestsView(generics.ListAPIView):
    serializer_class = FriendRequestSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.request.user.received_requests.filter(status="pending")
