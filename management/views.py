from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import DeleteView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from accounts.models import Accounts


class Profile(LoginRequiredMixin, ListView):
    paginate_by = 5

    def get_queryset(self):
        query = Accounts.objects.filter(parent_id=self.request.user.id)
        return query

    def get_template_names(self):
        if self.request.user.is_admin:
            return 'management/admin_profile.html'
        else:
            return 'management/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_user'] = Accounts.objects.filter(is_active=True).count()
        context['total_user'] = Accounts.objects.all().count()
        context['pending_user'] = context['total_user'] - context['active_user']

        context['parent'] = Accounts.objects.get(id=self.request.user.parent_id)
        return context


class ListOfUser(LoginRequiredMixin, ListView):
    queryset = Accounts.objects.all()
    template_name = 'management/user_list.html'


class ApproveList(LoginRequiredMixin, ListView):
    paginate_by = 10
    template_name = 'management/approve_list.html'
    queryset = Accounts.objects.filter(is_active=False)


class DeleteUser(LoginRequiredMixin, DeleteView):
    model = Accounts
    success_url = reverse_lazy('management:approve')
    template_name = 'management/delete.html'



@login_required
def approveUser(request, pk):
    user = get_object_or_404(Accounts, id=pk)
    user.activate_user()
    return redirect('management:approve')
