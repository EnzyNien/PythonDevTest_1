import csv
import os
from io import StringIO

from functools import wraps
from django.shortcuts import render, HttpResponse
from django.http import StreamingHttpResponse
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core import serializers
from django.core.files import File
from django.views.generic.list import ListView
from django.views.generic import UpdateView
from django.views.generic.detail import DetailView, SingleObjectMixin
from django.views.generic.edit import DeleteView, CreateView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse_lazy
from django.db.models import Q

from django.shortcuts import get_object_or_404

from mainapp.models import Clients
from mainapp.forms import ClientsEditForm, ClientsAddForm


class BaseView(SingleObjectMixin):

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', -1)
        obj = get_object_or_404(Clients, pk=pk)
        return obj


class Main(ListView):

    model = Clients
    template_name = 'mainapp/index.html'
    paginate_by = 10

    # def get_queryset(self):
    #    return Clients.objects.all()

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super(Main, self).get_context_data(**kwargs)
        page = self.request.GET.get('page', None)
        search = self.request.GET.get('search', None)

        name__regex = r'^.*{}.*$'.format(search)

        if search:
            clients_list = Clients.objects.filter(
                Q(
                    name__regex=name__regex) | Q(
                    company__name__regex=name__regex) | Q(
                    email__regex=name__regex) | Q(
                    phone__regex=name__regex) | Q(
                        interests__regex=name__regex))
        else:
            clients_list = Clients.objects.all()
        paginator = Paginator(clients_list, self.paginate_by)

        try:
            clients_list = paginator.page(page)
        except PageNotAnInteger:
            clients_list = paginator.page(1)
        except EmptyPage:
            clients_list = paginator.page(paginator.num_pages)

        context['clients_list'] = clients_list

        context['col_names'] = Clients.get_field_names_gen()
        return context


class Add(CreateView):

    model = Clients
    form_class = ClientsAddForm
    template_name = 'mainapp/add.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return super().get_object(queryset=None)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        self.context = super().get_context_data(*args, **kwargs)
        return self.context


class Delete(BaseView, DeleteView):

    model = Clients
    form_class = ClientsEditForm
    success_url = '/'

    def get_object(self, queryset=None):
        return super().get_object(queryset=None)


class Edit(BaseView, UpdateView):

    model = Clients
    form_class = ClientsEditForm
    template_name = 'mainapp/edit.html'
    success_url = '/'

    def get_object(self, queryset=None):
        return super().get_object(queryset=None)

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        self.context = super().get_context_data(*args, **kwargs)
        return self.context


class Details(BaseView, DetailView):

    model = Clients
    template_name = 'mainapp/details.html'

    def get_object(self, queryset=None):
        return super().get_object(queryset=None)

    def get_context_data(self, *args, **kwargs):
        self.context = super().get_context_data(*args, **kwargs)
        self.context['referer'] = self.request.META.get('HTTP_REFERER', '/')
        return self.context


def to_json(requests, *agrs, **kwargs):
    qs = Clients.objects.all()
    qs_json = serializers.serialize('json', qs)
    response = HttpResponse(qs_json, content_type='application/json')
    response['Content-Disposition'] = 'attachment; filename="file.json"'
    return response


def to_csv(requests, *agrs, **kwargs):
    qs = Clients.objects.all()
    model = Clients
    full_path = os.path.join(settings.MEDIA_ROOT, 'fils.csv')

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="file.csv"'
    writer = csv.writer(response)

    headers = []
    for field in model._meta.fields:
        headers.append(field.name)
    writer.writerow(headers)
    for obj in qs:
        row = []
        for field in headers:
            if field in headers:
                val = getattr(obj, field)
                if callable(val):
                    val = val()
                row.append(val)
        writer.writerow(row)
    return response


def from_json(requests, *agrs, **kwargs):
    pass


def from_csv(requests, *agrs, **kwargs):
    pass
