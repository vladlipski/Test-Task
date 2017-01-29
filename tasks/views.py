# from django.urls import reverse
# from django.views import generic
# from rolepermissions.mixins import HasPermissionsMixin
# from rolepermissions.verifications import has_permission
#
# from .models import Project, ProjectForm, Task, TaskForm
#
#
# class AllProjects(generic.ListView):
#     template_name = 'tasks/project-list.html'
#     context_object_name = 'projects_list'
#
#     def get_context_data(self, **kwargs):
#         context = super(AllProjects, self).get_context_data(**kwargs)
#         context['create_project_permission'] = has_permission(self.request.user, 'create_project')
#         return context
#
#     def get_queryset(self):
#         return Project.objects.order_by('-creation_date')
#
#
# class CreateProject(HasPermissionsMixin, generic.CreateView):
#     model = Project
#     template_name = 'tasks/creation_form.html'
#     form_class = ProjectForm
#     required_permission = 'create_project'
#
#     def get_context_data(self, **kwargs):
#         context = super(CreateProject, self).get_context_data(**kwargs)
#         context['object_name'] = Project.__name__.lower()
#         return context
#
#     def get_success_url(self):
#         return reverse("tasks:all_projects")
#
#
# class DetailProject(generic.DetailView):
#     model = Project
#     template_name = 'tasks/project-detail.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(DetailProject, self).get_context_data(**kwargs)
#         context['edit_project_permission'] = has_permission(self.request.user, 'edit_project')
#         context['tasks'] = Project.objects.get(pk=self.kwargs['pk']).task_set.all()
#         return context
#
#
# class UpdateProject(HasPermissionsMixin, generic.UpdateView):
#     model = Project
#     template_name = 'tasks/project-update.html'
#     form_class = ProjectForm
#     required_permission = 'edit_project'
#
#     def get_context_data(self, **kwargs):
#         context = super(UpdateProject, self).get_context_data(**kwargs)
#         context['tasks'] = Project.objects.get(pk=self.kwargs['pk']).task_set.all()
#         context['create_task_permission'] = has_permission(self.request.user, 'create_task')
#         return context
#
#     def get_success_url(self):
#         return reverse("tasks:detail_project", kwargs={'pk': self.kwargs['pk']})
#
#
# class DeleteProject(HasPermissionsMixin, generic.DeleteView):
#     model = Project
#     template_name = 'tasks/confirm_project_delete.html'
#     required_permission = 'delete_project'
#
#     def get_success_url(self):
#         return reverse("tasks:all_projects")
#
#
# class CreateTask(HasPermissionsMixin, generic.CreateView):
#     model = Task
#     template_name = 'tasks/creation_form.html'
#     form_class = TaskForm
#     required_permission = 'create_task'
#
#     def form_valid(self, form):
#         project = Project.objects.get(pk=self.kwargs['project_pk'])
#         form.instance.project = project
#         return super(CreateTask, self).form_valid(form)
#
#     def get_context_data(self, **kwargs):
#         context = super(CreateTask, self).get_context_data(**kwargs)
#         context['object_name'] = Task.__name__.lower()
#         return context
#
#     def get_success_url(self):
#         return reverse("tasks:edit_project", kwargs={'pk': self.kwargs['project_pk']})
#
#
# class DetailTask(generic.DetailView):
#     model = Task
#     template_name = 'tasks/task.html'
#
#     def get_context_data(self, **kwargs):
#         context = super(DetailTask, self).get_context_data(**kwargs)
#         context['edit_task_permission'] = has_permission(self.request.user, 'edit_task')
#         return context
