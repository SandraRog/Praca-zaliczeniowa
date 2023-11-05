import pytest
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse

from stable_schedule.models import Horse, TrainingSchedule, Feeding, Health, Competition, HorseCompetition
from django.test import TestCase

from .forms import AddHorseForm, ModifyHorseForm, AddFeedingForm, ModifyFeedingForm, AddHealthForm, ModifyHealthForm, \
    AddTrainingForm, ModifyTrainingForm, AddCompetitionForm, AddHorseToCompetitionForm
from .validators import check_amount
from django.core.exceptions import ValidationError
# Create your tests here.

def test_index_view():
    client = Client()
    url = reverse('index')
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony add_horse - z logowaniem i bez
def test_add_horse_view_not_login():
    client = Client()
    url = reverse('add_horse')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_add_hose_view_login_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('add_horse')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddHorseForm)

@pytest.mark.django_db
def test_add_hose_view_login_post(user):
    client = Client()
    client.force_login(user)
    data = {
        'name':'bobek',
        'age': 5,
        'pedigree':'NN',
    }
    url = reverse('add_horse')
    response = client.post(url, data)
    assert response.status_code == 302
    assert Horse.objects.get(**data, owner=user)

#testy wyświetlania strony horse_details - z logowaniem i bez
@pytest.mark.django_db
def test_horse_details_view_not_login(horse):
    client = Client()
    url = reverse('horse_details', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_hose_details_view_login_get(horse):
    client = Client()
    client.force_login(horse.owner)
    url = reverse('horse_details', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony horse_list - z logowaniem i bez
@pytest.mark.django_db
def test_horse_list_view_not_login():
    client = Client()
    url = reverse('horse_list')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_horse_list_view_login_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('horse_list')
    response = client.get(url)
    assert response.status_code == 200

#nowy test
@pytest.mark.django_db
def test_horse_list(users_lst, horses_lst):
    client = Client()
    client.force_login(users_lst[0])
    url = reverse('horse_list')
    response = client.get(url)
    assert response.status_code == 200
    assert response.context['horses'].count() == len(horses_lst)
    for p in horses_lst:
        assert p in response.context['horses']


#testy wyświetlania strony horse_modify - z logowaniem i bez
@pytest.mark.django_db
def test_horse_modify_view_not_login(horse):
    client = Client()
    url = reverse('horse_modify', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_hose_modify_view_login_get(horse):
    client = Client()
    client.force_login(horse.owner)
    url = reverse('horse_modify', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], ModifyHorseForm)

@pytest.mark.django_db
def test_hose_modify_view_login_post(user):
    client = Client()
    client.force_login(user)
    data = {
        'name':'bobek',
        'age': 5,
        'pedigree':'NN',
    }
    url = reverse('add_horse')
    response = client.post(url, data)
    assert response.status_code == 302
    assert Horse.objects.get(**data, owner=user)

#testy wyświetlania strony horse_delete - z logowaniem i bez
@pytest.mark.django_db
def test_horse_delete_view_not_login(horse):
    client = Client()
    url = reverse('horse_delete', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_hose_delete_view_login_get(horse):
    client = Client()
    client.force_login(horse.owner)
    url = reverse('horse_delete', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony horse_feeding - z logowaniem i bez
@pytest.mark.django_db
def test_add_horse_feeding_not_login(horse):
    client = Client()
    url = reverse('horse_feeding', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_add_hose_feeding_login_get(user, horse):
    client = Client()
    client.force_login(user)
    url = reverse('horse_feeding', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddFeedingForm)

@pytest.mark.django_db
def test_add_feeding_view_login_post(horse):
    client = Client()
    client.force_login(horse.owner)
    data = {
        'ingredients': 'owies',
        'time_of_day': 'rano',
    }
    url = reverse('horse_feeding', kwargs={'id':horse.id})
    response = client.post(url, data)
    assert response.status_code == 302
    assert Feeding.objects.get(**data, horse=horse)

#testy wyświetlania strony feeding_list - z logowaniem i bez
@pytest.mark.django_db
def test_feeding_list_view_not_login():
    client = Client()
    url = reverse('feeding_list')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_feeding_list_view_login_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('feeding_list')
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony modify_feeding - z logowaniem i bez
@pytest.mark.django_db
def test_feeding_modify_view_not_login(feeding, horse):
    client = Client()
    url = reverse('modify_feeding', kwargs={'id':feeding.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_feeding_modify_view_login_get(user, feeding):
    client = Client()
    client.force_login(user)
    url = reverse('modify_feeding', kwargs={'id':feeding.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], ModifyFeedingForm)

@pytest.mark.django_db
def test_feeding_modify_view_login_post(user, feeding):
    client = Client()
    client.force_login(user)
    data = {
        'ingredients': 'owies',
        'time_of_day': 'rano',
    }
    url = reverse('modify_feeding', kwargs={'id':feeding.id})
    response = client.post(url, data)
    assert response.status_code == 302
    assert Feeding.objects.get(**data)


#testy wyświetlania strony delete_feeding - z logowaniem i bez
@pytest.mark.django_db
def test_feeding_delete_view_not_login(feeding, horse):
    client = Client()
    url = reverse('delete_feeding', kwargs={'id':feeding.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_feeding_delete_view_login_get(user, feeding):
    client = Client()
    client.force_login(user)
    url = reverse('delete_feeding', kwargs={'id':feeding.id})
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony horse_health - z logowaniem i bez
@pytest.mark.django_db
def test_add_horse_health_not_login(horse):
    client = Client()
    url = reverse('horse_health', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_add_horse_health_login_get(user, horse):
    client = Client()
    client.force_login(user)
    url = reverse('horse_health', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddHealthForm)

@pytest.mark.django_db
def test_add_horse_health_view_login_post(horse):
    client = Client()
    client.force_login(horse.owner)
    data = {
        'care': 'kowal',
    }
    url = reverse('horse_health', kwargs={'id':horse.id})
    response = client.post(url, data)
    assert response.status_code == 302
    assert Health.objects.get(**data, horse=horse)

#testy wyświetlania strony health_list - z logowaniem i bez
@pytest.mark.django_db
def test_health_list_view_not_login():
    client = Client()
    url = reverse('horse_health')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_health_list_view_login_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('horse_health')
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony delete_health - z logowaniem i bez
@pytest.mark.django_db
def test_health_delete_view_not_login(health, horse):
    client = Client()
    url = reverse('delete_health', kwargs={'id':health.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_health_delete_view_login_get(user, health):
    client = Client()
    client.force_login(user)
    url = reverse('delete_health', kwargs={'id':health.id})
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony modify_health - z logowaniem i bez
@pytest.mark.django_db
def test_health_modify_view_not_login(health, horse):
    client = Client()
    url = reverse('modify_health', kwargs={'id':health.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_health_modify_view_login_get(user, health):
    client = Client()
    client.force_login(user)
    url = reverse('modify_health', kwargs={'id':health.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], ModifyHealthForm)

@pytest.mark.django_db
def test_health_modify_view_login_post(user, health):
    client = Client()
    client.force_login(user)
    data = {
        'care': 'kowal',
    }
    url = reverse('modify_health', kwargs={'id':health.id})
    response = client.post(url, data)
    assert response.status_code == 302
    assert Health.objects.get(**data)

#testy wyświetlania strony training_schedule - z logowaniem i bez
@pytest.mark.django_db
def test_add_horse_training_not_login(horse):
    client = Client()
    url = reverse('training_schedule', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_add_hose_training_login_get(user, horse):
    client = Client()
    client.force_login(user)
    url = reverse('training_schedule', kwargs={'id':horse.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddTrainingForm)

@pytest.mark.django_db
def test_add_horse_training_view_login_post(horse):
    client = Client()
    client.force_login(horse.owner)
    data = {
        'place': 'las',
    }
    url = reverse('training_schedule', kwargs={'id':horse.id})
    response = client.post(url, data)
    assert response.status_code == 302
    assert TrainingSchedule.objects.get(**data, horse=horse)

#testy wyświetlania strony training_list - z logowaniem i bez
def test_training_list_view_not_login():
    client = Client()
    url = reverse('training_list')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_training_list_view_login_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('training_list')
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony delete_training_schedule - z logowaniem i bez
@pytest.mark.django_db
def test_training_schedule_delete_view_not_login(trainingschedule, horse):
    client = Client()
    url = reverse('delete_training_schedule', kwargs={'id':trainingschedule.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_training_schedule_delete_view_login_get(user, trainingschedule):
    client = Client()
    client.force_login(user)
    url = reverse('delete_training_schedule', kwargs={'id':trainingschedule.id})
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony modify_training_schedule - z logowaniem i bez
@pytest.mark.django_db
def test_training_schedule_modify_view_not_login(trainingschedule, horse):
    client = Client()
    url = reverse('modify_training_schedule', kwargs={'id':trainingschedule.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_training_schedule_modify_view_login_get(user, trainingschedule):
    client = Client()
    client.force_login(user)
    url = reverse('modify_training_schedule', kwargs={'id':trainingschedule.id})
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], ModifyTrainingForm)

@pytest.mark.django_db
def test_training_schedule_modify_view_login_post(user, trainingschedule):
    client = Client()
    client.force_login(user)
    data = {
        'place': 'las',
    }
    url = reverse('modify_training_schedule', kwargs={'id':trainingschedule.id})
    response = client.post(url, data)
    assert response.status_code == 302
    assert TrainingSchedule.objects.get(**data)

#testy wyświetlania strony competitions - z logowaniem i bez
def test_competitions_view_not_login():
    client = Client()
    url = reverse('competitions')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_competitions_view_login_get(user):
    client = Client()
    client.force_login(user)
    url = reverse('competitions')
    response = client.get(url)
    assert response.status_code == 200
    assert isinstance(response.context['form'], AddCompetitionForm)

@pytest.mark.django_db
def test_competitions_view_login_post(user):
    client = Client()
    client.force_login(user)
    data = {
        'place':'Katowice',
        'date': '2023-10-27',
    }
    url = reverse('competitions')
    response = client.post(url, data)
    assert response.status_code == 302
    assert Competition.objects.get(**data)

#testy wyświetlania strony competitions_detele - z logowaniem i bez
@pytest.mark.django_db
def test_competitions_delete_view_not_login(competitions, horse):
    client = Client()
    url = reverse('competitions_detele', kwargs={'id':competitions.id})
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_competitions_delete_view_login_get(user, competitions):
    client = Client()
    client.force_login(user)
    url = reverse('competitions_detele', kwargs={'id':competitions.id})
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony competitions_list
@pytest.mark.django_db
def test_competitions_list_view():
    client = Client()
    url = reverse('competitions_list')
    response = client.get(url)
    assert response.status_code == 200

#testy wyświetlania strony add_horse_to_competition - z logowaniem i bez
@pytest.mark.django_db
def test_add_horse_to_competition_not_login(horse, competitions):
    client = Client()
    url = reverse('add_horse_to_competition')
    response = client.get(url)
    assert response.status_code == 302
    assert response.url.startswith(reverse('login'))

@pytest.mark.django_db
def test_add_hose_to_competition_login_get(user, horse, competitions):
    client = Client()
    client.force_login(user)
    url = reverse('add_horse_to_competition')
    response = client.get(url)
    assert response.status_code == 200

@pytest.mark.django_db
def test_competitions_view_login_post(user, horse, competitions):
    client = Client()
    client.force_login(user)
    data = {
        'score': 89,
        'horse': horse.id,
        'competition': competitions.id,
    }
    url = reverse('add_horse_to_competition')
    response = client.post(url, data)
    assert response.status_code == 302
    assert HorseCompetition.objects.get(**data)

#testy wyświetlania strony competition_summary - z logowaniem i bez
@pytest.mark.django_db
def test_horsecompetitions_list_view():
    client = Client()
    url = reverse('competition_summary')
    response = client.get(url)
    assert response.status_code == 200

#test walidacji
def test_funkcja_check_amount_dziala():
    assert ValidationError, check_amount(100)
    assert ValidationError, check_amount(-10)