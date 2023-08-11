from django.urls import path
from .views import (
    CustomLoginView,
    RegisterPage,
    CreateChallengeView,
    PendingChallengesView,
    AcceptChallengeView,
    ChallengesView,
    logout_view
)

urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('register/', RegisterPage.as_view(), name='register'),
    path('create-challenge/', CreateChallengeView.as_view(), name='create_challenge'),
    path('pending-challenges/', PendingChallengesView.as_view(), name='pending_challenges'),
    path('accept-challenge/<int:pk>/', AcceptChallengeView.as_view(), name='accept_challenge'),
    path('logout/',logout_view, name='logout'),
    path('', ChallengesView.as_view(), name='challenges'),
]
