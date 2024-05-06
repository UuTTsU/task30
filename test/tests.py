from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Name
from django.test import TestCase, Client
from django.urls import reverse
from .forms import NameForm

class NameTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.sample_name_data = {
            'name': 'gio',
            'last_name': 'utsu'
        }

    def test_create_name(self):
        response = self.client.post('/api/names/', self.sample_name_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Name.objects.count(), 1)
        self.assertEqual(Name.objects.get().name, 'gio')
        self.assertEqual(Name.objects.get().last_name, 'utsu')

    def test_retrieve_name(self):
        name = Name.objects.create(name='tatia', last_name='tabatadze')
        response = self.client.get(f'/api/names/{name.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'tatia')
        self.assertEqual(response.data['last_name'], 'tabatadze')

    def test_update_name(self):
        name = Name.objects.create(name='tatia', last_name='tabatadze')
        updated_data = {'name': 'tatia Updated', 'last_name': 'tabatadze Updated'}
        response = self.client.put(f'/api/names/{name.id}/', updated_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Name.objects.get(id=name.id).name, 'tatia Updated')
        self.assertEqual(Name.objects.get(id=name.id).last_name, 'tabatadze Updated')

    def test_delete_name(self):
        name = Name.objects.create(name='tatia', last_name='tabatadze')
        response = self.client.delete(f'/api/names/{name.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Name.objects.count(), 0)




class NameListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.name1 = Name.objects.create(name="gio", last_name="utsu")
        self.name2 = Name.objects.create(name="tatia", last_name="tabatadze")
        self.url = reverse('name_list')

    def test_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_queryset(self):
        response = self.client.get(self.url)
        queryset = response.context['names']
        self.assertEqual(len(queryset), 2)
        self.assertIn(self.name1, queryset)
        self.assertIn(self.name2, queryset)
        
        

class NameFormTests(TestCase):
    def test_valid_form(self):
        form_data = {'name': 'gio', 'last_name': 'utsu'}
        form = NameForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form_missing_name(self):
        form_data = {'last_name': 'utsu'}
        form = NameForm(data=form_data)
        self.assertFalse(form.is_valid())

    def test_invalid_form_missing_last_name(self):
        form_data = {'name': 'gio'}
        form = NameForm(data=form_data)
        self.assertFalse(form.is_valid())




class NameUpdateViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.name = Name.objects.create(name="gio", last_name="utsu")
        self.url = reverse('name_update', kwargs={'pk': self.name.pk})
        self.valid_form_data = {'name': 'UpdatedName', 'last_name': 'UpdatedLastName'}
        self.invalid_form_data = {'name': '', 'last_name': ''}

    def test_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_view_updates_object(self):
        response = self.client.post(self.url, self.valid_form_data)
        self.name.refresh_from_db()
        self.assertEqual(self.name.name, 'UpdatedName')
        self.assertEqual(self.name.last_name, 'UpdatedLastName')
        
class NameDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.name = Name.objects.create(name="gio", last_name="utsu")
        self.url = reverse('name_delete', kwargs={'pk': self.name.pk})

    def test_view_status_code(self):
        response = self.client.post(self.url)
        self.assertEqual(response.status_code, 302)

    def test_view_deletes_object(self):
        response = self.client.post(self.url)
        self.assertEqual(Name.objects.filter(pk=self.name.pk).exists(), False)
