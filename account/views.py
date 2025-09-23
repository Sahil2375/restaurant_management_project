from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .serializers import UserProfileSerializer

class UserProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        # Return the logged-in user
        return self.request.user