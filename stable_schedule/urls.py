"""
URL configuration for overseer project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from stable_schedule import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('horse/new/', views.AddHorseView.as_view(), name='add_horse'),
    path('horse/<int:id>/', views.ShowHorseDetailView.as_view(), name='horse_details'),
    path('horse/list/', views.ShowHorseListView.as_view(), name='horse_list'),
    path('horse/modify/<int:id>/', views.ModifyHorseView.as_view(), name='horse_modify'),
    path('horse/delete/<int:id>/', views.DeleteHorseView.as_view(), name='horse_delete'),
    path('horse/feeding/<int:id>/', views.AddFeedingToHorseView.as_view(), name='horse_feeding'),
    path('horse/feeding/list/', views.FeedingView.as_view(), name='feeding_list'),
    path('horse/feeding/<int:id>/modify/', views.ModifyFeedingView.as_view(), name='modify_feeding'),
    path('horse/feeding/delete/<int:id>/', views.DeleteFeedingView.as_view(), name='delete_feeding'),
    path('horse/health/<int:id>/', views.AddHealthToHorseView.as_view(), name='horse_health'),
    path('horse/health/list/', views.HealthView.as_view(), name='horse_health'),
    path('horse/health/<int:id>/delete/', views.DeleteHealthView.as_view(), name='delete_health'),
    path('horse/health/<int:id>/modify/', views.ModifyHealthView.as_view(), name='modify_health'),
    path('horse/training_schedule/<int:id>/', views.AddTrainingScheduleView.as_view(), name='training_schedule'),
    path('horse/training_schedule/list/', views.TrainingView.as_view(), name='training_list'),
    path('horse/training_schedule/<int:id>/delete/', views.DeleteTrainingView.as_view(), name='delete_training_schedule'),
    path('horse/training_schedule/<int:id>/modify/', views.ModifyTrainingView.as_view(), name='modify_training_schedule'),
    path('horse/competitions/', views.AddCompetitionsView.as_view(), name='competitions'),
    path('horse/competitions/delete/<int:id>/', views.DeleteCompetitionsView.as_view(), name='competitions_detele'),
    path('horse/competitions/list/', views.CompetitionListView.as_view(), name='competitions_list'),
    path('horse/competitions/add_horse/', views.AddHorseToCompetition.as_view(), name='add_horse_to_competition'),
    path('horse/competitions/summary/', views.HorseCompetitionView.as_view(), name='competition_summary'),


]