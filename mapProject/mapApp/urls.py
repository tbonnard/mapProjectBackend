from django.urls import path
from .views import views, csrfTokenViews, propertyViews, projectViews, choiceViews, authViews
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
    # path('projects/<str:uuid>/', projectViews.ProjectsView.as_view()), #projects related to a property
    path('projects/', projectViews.ProjectsView.as_view()), #projects related to a property
    path('project/<int:pk>/', projectViews.ProjectDetailsView.as_view()),
    path('project/', projectViews.ProjectView.as_view()),
    path('choice/', choiceViews.ChoiceView.as_view()),
    path('choice/<int:pk>/', choiceViews.ChoiceDetailsView.as_view()),
]