from django.urls import reverse
from django.views import generic
from rolepermissions.mixins import HasPermissionsMixin
from rolepermissions.verifications import has_permission

from .models import Project, ProjectForm


class AllProjects(generic.ListView):
    template_name = 'tasks/all_projects.html'
    context_object_name = 'projects_list'

    def get_context_data(self, **kwargs):
        context = super(AllProjects, self).get_context_data(**kwargs)
        context['have_permissions'] = has_permission(self.request.user, 'crud_projects')
        return context

    def get_queryset(self):
        return Project.objects.order_by('-creation_date')


class CreateProject(HasPermissionsMixin, generic.CreateView):
    model = Project
    template_name = 'tasks/create_project.html'
    form_class = ProjectForm
    required_permission = 'crud_projects'

    def get_context_data(self, **kwargs):
        context = super(CreateProject, self).get_context_data(**kwargs)
        context['have_permissions'] = has_permission(self.request.user, 'crud_projects')
        return context

    def get_success_url(self):
        return reverse("tasks:all_projects")


class DetailProject(generic.DetailView):
    model = Project
    template_name = 'tasks/project.html'

    def get_context_data(self, **kwargs):
        context = super(DetailProject, self).get_context_data(**kwargs)
        context['have_permissions'] = has_permission(self.request.user, 'crud_projects')
        context['tasks'] = Project.objects.get(pk=self.kwargs['pk']).task_set.all()
        return context

    def get_success_url(self):
        return reverse("tasks:all_projects")


class UpdateProject(HasPermissionsMixin, generic.UpdateView):
    model = Project
    template_name = 'tasks/edit_project.html'
    form_class = ProjectForm
    required_permission = 'crud_projects'

    def get_context_data(self, **kwargs):
        context = super(UpdateProject, self).get_context_data(**kwargs)
        context['tasks'] = Project.objects.get(pk=self.kwargs['pk']).task_set.all()
        return context

    def get_success_url(self):
        return reverse("tasks:detail_project", kwargs={'pk': self.kwargs['pk']})


class DeleteProject(HasPermissionsMixin, generic.DeleteView):
    model = Project
    template_name = 'tasks/confirm_project_delete.html'
    required_permission = 'crud_projects'

    def get_success_url(self):
        return reverse("tasks:all_projects")