from django.urls import path
from .views import (views, csrfTokenViews, propertyViews, projectViews,
                    choiceViews, authViews, followViews, voteViews)
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path('get-csrf-token/', csrf_exempt(csrfTokenViews.get_csrf_token), name='get_csrf_token'),
    path('register/', authViews.RegisterView.as_view()),
    path('login/', authViews.LoginView.as_view()),
    path('logout/', authViews.LogoutView.as_view()),
    path('user/<int:pk>/', authViews.UserAuthView.as_view()),
    path('user/admin/', authViews.UsersAPIView.as_view()),
    path('user/admin/<int:pk>/', authViews.UserView.as_view()),
    path('property/', propertyViews.PropertyView.as_view()),
    path('property/<int:pk>/', propertyViews.PropertyDetailsView.as_view()),
    path('propertycheck/', propertyViews.PropertyCheckView.as_view()),
    path('querylocation/', propertyViews.PropertyQueryLocationView.as_view()),
    path('querylocationdb/', propertyViews.PropertyQueryLocationDBView.as_view()),
    path('querylocationaround/', propertyViews.PropertyQueryLocationAroundView.as_view()),
    path('querylocationaroundall/', propertyViews.PropertyQueryLocationViewNotInDBAll.as_view()),
    path('projects/', projectViews.ProjectsView.as_view()), #projects related to a property
    path('projectsfollowedpropertiesuser/', projectViews.ProjectsUserFollowedPropertyView.as_view()), #projects related to property followed by the user
    path('project/<int:pk>/', projectViews.ProjectDetailsView.as_view()),
    path('project/', projectViews.ProjectView.as_view()),
    path('allprojects/', projectViews.ProjectAllNearbyView.as_view()),
    path('choice/', choiceViews.ChoiceView.as_view()),
    path('choice/<int:pk>/', choiceViews.ChoiceDetailsView.as_view()),
    path('vote/', voteViews.VoteView.as_view()),
    path('vote/<int:pk>/', voteViews.VoteDetailsView.as_view()),
    path('votesproperty/<int:propertyid>/', voteViews.VotePropertyView.as_view()),  # votes related to a property
    path('votesproject/<int:projectid>/', voteViews.VoteProjectView.as_view()),  # votes related to a project
    path('voteuserproporties/', voteViews.VotePropertyUserView.as_view()),  # votes related to projects in property
    path('voteuserfollowedproperties/', voteViews.VoteUserFollowedPropertiesView.as_view()),  # votes related to followed properties
    path('follows/', followViews.FollowsView.as_view()),
    path('follow/', followViews.FollowView.as_view()),
    path('follow/<int:pk>/', followViews.FollowViewDetailsView.as_view()),
]