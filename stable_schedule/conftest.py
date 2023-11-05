import pytest
from django.contrib.auth.models import User, Permission

from stable_schedule.models import Horse, Feeding, Health, TrainingSchedule, Competition, HorseCompetition


@pytest.fixture
def user():
    u = User.objects.create(username='ala')
    return u

@pytest.fixture
def horses():
    h = Horse.objects.create(
        name='bobek',
        age=5,
        pedigree='NN',
        owner= user,
    )
    return h

@pytest.fixture
def horse(user):
    t = Horse.objects.create(
        name='bobek',
        age=5,
        pedigree='NN',
        owner= user,
    )
    return t

@pytest.fixture
def feeding(horse):
    f = Feeding.objects.create(
        ingredients='owies',
        time_of_day='rano',
        horse= horse
    )
    return f

@pytest.fixture
def health(horse):
    h = Health.objects.create(
        care='szcsepienie',
        date='2023-10-27',
        horse= horse
    )
    return h

@pytest.fixture
def trainingschedule(horse):
    th = TrainingSchedule.objects.create(
        place='Katowice',
        date='2023-10-27',
        horse= horse
    )
    return th

@pytest.fixture
def competitions():
    c = Competition.objects.create(
        place='Katowice',
        date='2023-10-27',
    )
    return c

@pytest.fixture
def horsecompetitions(competitions, horse):
    hc = HorseCompetition.objects.create(
        score = 80,
        competition = competitions,
        horse= horse,
    )
    return hc

@pytest.fixture
def users_lst():
    user_lst =[]
    user_lst.append(User.objects.create(username='ala'))
    user_lst.append(User.objects.create(username='basia'))
    user_lst.append(User.objects.create(username='kasia'))
    return user_lst

@pytest.fixture
def horses_lst(users_lst):
    lst =[]
    lst.append(Horse.objects.create(
        name='horse1',
        age=10,
        pedigree='NN',
        owner=users_lst[0],
    )),
    lst.append(Horse.objects.create(
        name='horse2',
        age=5,
        pedigree='NN',
        owner=users_lst[0],
    )),
    lst.append(Horse.objects.create(
        name='horse3',
        age=8,
        pedigree='NN',
        owner=users_lst[0],
    ))
    return lst

