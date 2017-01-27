from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib.auth.models import User

from .models import Project, Task


class AllProjectsView(generic.ListView):
    template_name = 'tasks/all_projects.html'
    context_object_name = 'projects_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Project.objects.order_by('-creation_date')


class ProjectView(generic.DetailView):
    model = Project
    template_name = 'tasks/project_detail.html'

    # def get(self, request, *args, **kwargs):
    #     self.object = self.get_object()
    #     if self.object.voted_users.filter(pk=request.user.pk).exists() or not \
    #             request.user.is_authenticated:
    #         return redirect('polls:results', pk=self.object.pk)
    #     else:
    #         context = self.get_context_data(object=self.object)
    #         return self.render_to_response(context)


class ResultsView(generic.DetailView):
    model = Project
    template_name = 'tasks/results.html'


# class ProfileView(LoginRequiredMixin, generic.UpdateView):
#     model = User
#     fields = '__all__'
#
#     def get_object(self, queryset=None):
#         return self.request.user


# @login_required()
# def vote(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     try:
#         selected_choice = question.choice_set.get(pk=request.POST['choice'])
#     except (KeyError, Choice.DoesNotExist):
#         return render(request, 'tasks/project_detail.html', {
#             'question': question,
#             'error_message': "You didn't select a choice.",
#         })
#     else:
#         selected_choice.votes= F('votes') + 1
#         selected_choice.save(update_fields=['votes'])
#         question.voted_users.add(request.user)
#         question.save()
#         return redirect('polls:results', pk=question.id)

