from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from stable_schedule.forms import AddHorseForm, ModifyHorseForm, AddFeedingForm, AddHealthForm, AddCompetitionForm, \
    AddTrainingForm, ModifyFeedingForm, ModifyHealthForm, AddHorseToCompetitionForm, ModifyTrainingForm
from stable_schedule.models import Horse, Feeding, Health, Competition, TrainingSchedule, HorseCompetition
from .models import Horse
from .forms import AddHorseForm

# Create your views here.
class IndexView(View):

    def get(self, request):
        return render(request, 'index.html')

class AddHorseView(LoginRequiredMixin,View):
    def get(self, request):
        form = AddHorseForm()
        return render(request, 'add_horse.html', {'form': form})

    def post(self, request):
        form = AddHorseForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            pedigree = form.cleaned_data['pedigree']
            Horse.objects.create(name=name, age=age, pedigree=pedigree, owner=request.user)
            return redirect('horse_list')
        else:
            return render(request, 'add_horse.html', {'form': form})

class ShowHorseDetailView(LoginRequiredMixin, View):

    def get(self, request, id):
        horse = Horse.objects.get(id=id)
        form = AddHorseForm()
        return render(request, 'horse_details.html', {'horse': horse, 'form': form})

class ShowHorseListView(LoginRequiredMixin,View):

    def get(self, request):
        horses = Horse.objects.filter(owner=request.user)
        return render(request, "horses_list.html", {"horses": horses})


class DeleteHorseView(LoginRequiredMixin,View):
    def get(self, request, id):
        horses = Horse.objects.get(pk=id)
        return render(request, 'horse_delete.html', {'horses': horses})

    def post(self, request, id):
        answer = request.POST['answer']
        if answer == 'Yes':
            Horse.objects.get(pk=id).delete()
        return redirect('horse_list')

class ModifyHorseView(LoginRequiredMixin,View):
    def get(self, request, id):
        horse = Horse.objects.get(pk=id)
        form = ModifyHorseForm(instance=horse)
        return render(request, 'modify_horse.html', {'form': form})

    def post(self, request, id):
        form = ModifyHorseForm(request.POST)
        horses = Horse.objects.get(pk=id)
        if form.is_valid():
            name = form.cleaned_data['name']
            age = form.cleaned_data['age']
            pedigree = form.cleaned_data['pedigree']
            horses.name = name
            horses.age = age
            horses.pedigree = pedigree
            horses.save()
            return redirect('horse_list')
        else:
            return render(request, 'modify_horse.html', {'form': form})

class AddFeedingToHorseView(LoginRequiredMixin,View):

    def get(self, request, id):
        horse = Horse.objects.get(pk=id)
        form = AddFeedingForm()
        return render(request, 'add_feed.html', {'horse': horse, 'form': form})

    def post(self, request, id):
        ingredients = request.POST.get('ingredients')
        time_of_day = request.POST.get('time_of_day')
        horse = Horse.objects.get(pk=id)
        Feeding.objects.create(ingredients=ingredients, time_of_day=time_of_day,
                            horse=horse)
        return redirect('horse_details', id)

class FeedingView(LoginRequiredMixin, View):

    def get(self, request):
        horse = Horse.objects.all()
        feeding = Feeding.objects.all()
        return render(request, 'feeding_list.html', {'feeding': feeding, 'horse':horse})

class ModifyFeedingView(LoginRequiredMixin,View):
    def get(self, request, id):
        feeding = Feeding.objects.get(pk=id)
        form = ModifyFeedingForm(instance=feeding)
        return render(request, 'modify_feeding.html', {'form': form})

    def post(self, request, id):
        form = ModifyFeedingForm(request.POST)
        feeding = Feeding.objects.get(pk=id)
        if form.is_valid():
            ingredients = form.cleaned_data['ingredients']
            time_of_day = form.cleaned_data['time_of_day']
            feeding.ingredients = ingredients
            feeding.time_of_day = time_of_day
            feeding.save()
            return redirect('feeding_list')
        else:
            return render(request, 'modify_feeding.html', {'form': form})

class DeleteFeedingView(LoginRequiredMixin,View):
    def get(self, request, id):
        feeding = Feeding.objects.get(pk=id)
        return render(request, 'feeding_delete.html', {'feeding': feeding})

    def post(self, request, id):
        answer = request.POST['answer']
        if answer == 'Yes':
            Feeding.objects.get(pk=id).delete()
        return redirect('feeding_list')


class AddHealthToHorseView(LoginRequiredMixin,View):

    def get(self, request, id):
        horse = Horse.objects.get(pk=id)
        form = AddHealthForm()
        return render(request, 'add_health.html', {'horse': horse, 'form': form})

    def post(self, request, id):
        care = request.POST.get('care')
        date = request.POST.get('date')
        horse = Horse.objects.get(pk=id)
        Health.objects.create(care=care, date=date,horse=horse)
        return redirect('horse_details', id)


class HealthView(LoginRequiredMixin, View):

    def get(self, request):
        horse = Horse.objects.all()
        health = Health.objects.all()
        return render(request, 'health_list.html', {'health': health, 'horse':horse})

class DeleteHealthView(LoginRequiredMixin,View):
    def get(self, request, id):
        health = Health.objects.get(pk=id)
        return render(request, 'health_delete.html', {'health': health})

    def post(self, request, id):
        answer = request.POST['answer']
        if answer == 'Yes':
            Health.objects.get(pk=id).delete()
        return redirect('horse_health')


class ModifyHealthView(LoginRequiredMixin,View):
    def get(self, request, id):
        health = Health.objects.get(pk=id)
        form = ModifyHealthForm(instance=health)
        return render(request, 'modify_feeding.html', {'form': form})

    def post(self, request, id):
        form = ModifyHealthForm(request.POST)
        health = Health.objects.get(pk=id)
        if form.is_valid():
            care = form.cleaned_data['care']
            health.care = care
            health.save()
            return redirect('horse_health')
        else:
            return render(request, 'modify_health.html', {'form': form})
class AddTrainingScheduleView(LoginRequiredMixin,View):

    def get(self, request, id):
        horse = Horse.objects.get(pk=id)
        form = AddTrainingForm()
        return render(request, 'training_schedule.html', {'horse': horse, 'form': form})

    def post(self, request, id):
        place = request.POST.get('place')
        date = request.POST.get('date')
        horse = Horse.objects.get(pk=id)
        TrainingSchedule.objects.create(place=place, date=date,horse=horse)
        return redirect('horse_details', id)


class TrainingView(LoginRequiredMixin, View):

    def get(self, request):
        horse = Horse.objects.all()
        trainingschedule = TrainingSchedule.objects.all()
        return render(request, 'training_list.html', {'trainingschedule': trainingschedule, 'horse':horse})


class DeleteTrainingView(LoginRequiredMixin,View):
    def get(self, request, id):
        trainingschedule = TrainingSchedule.objects.get(pk=id)
        return render(request, 'training_schedule_delete.html', {'trainingschedule': trainingschedule})

    def post(self, request, id):
        answer = request.POST['answer']
        if answer == 'Yes':
            TrainingSchedule.objects.get(pk=id).delete()
        return redirect('training_list')


class ModifyTrainingView(LoginRequiredMixin,View):
    def get(self, request, id):
        trainingschedule = TrainingSchedule.objects.get(pk=id)
        form = ModifyTrainingForm(instance=trainingschedule)
        return render(request, 'modify_training.html', {'form': form})

    def post(self, request, id):
        form = ModifyTrainingForm(request.POST)
        trainingschedule = TrainingSchedule.objects.get(pk=id)
        if form.is_valid():
            place = form.cleaned_data['place']
            trainingschedule.place = place
            trainingschedule.save()
            return redirect('training_list')
        else:
            return render(request, 'modify_training.html', {'form': form})


class AddCompetitionsView(LoginRequiredMixin,View):

    def get(self, request):
        form = AddCompetitionForm()
        return render(request, 'add_competition.html', {'form': form})

    def post(self, request):
        form = AddCompetitionForm(request.POST)
        if form.is_valid():
            place = form.cleaned_data['place']
            date = form.cleaned_data['date']
            Competition.objects.create(place=place, date=date)
            return redirect('competitions_list')
        else:
            return render(request, 'add_competition.html', {'form': form})


class CompetitionListView(View):
    def get(self, request):
        competitions = Competition.objects.all()
        return render(request, 'competition_list.html', {'competitions': competitions})


class HorseCompetitionView(View):
    def get(self, request):
        horsecompetitions = HorseCompetition.objects.all()
        return render(request, 'horsecompetitions_list.html', {'horsecompetitions': horsecompetitions})

class DeleteCompetitionsView(LoginRequiredMixin, View):
    def get(self, request, id):
        competitions = Competition.objects.get(pk=id)
        return render(request, 'competition_delete.html', {'competitions': competitions})

    def post(self, request, id):
        answer = request.POST['answer']
        if answer == 'Yes':
            Competition.objects.get(pk=id).delete()
        return redirect('competitions_list')


class AddHorseToCompetition(LoginRequiredMixin,View):
    def get(self, request):
        horses = Horse.objects.all()
        competitions = Competition.objects.all()
        return render(request, 'add_horse_to_competitions.html', {'horses':horses, 'competitions':competitions})

    def post(self, request):
            score = request.POST.get('score')
            horse_id = request.POST.get('horse')
            horse = Horse.objects.get(pk=horse_id)
            competition = request.POST.get('competition')
            competition = Competition.objects.get(pk=competition)
            hc = HorseCompetition(score=score, horse=horse, competition=competition)
            hc.save()
            return redirect ('competition_summary')



