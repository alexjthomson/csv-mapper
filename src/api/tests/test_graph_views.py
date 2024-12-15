from django.contrib.auth.models import User, Group, Permission
from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from api.models import Source, Graph, GraphDataset

class GraphListViewTests(TestCase):
    databases = {'default', 'graph'}
    
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user_with_perms = User.objects.create_user(username="permuser", password="password")

        # Assign permissions
        permissions = ['view_graph', 'add_graph']
        for perm in permissions:
            self.user_with_perms.user_permissions.add(Permission.objects.get(codename=perm))

        # Authenticate the user with permissions
        self.client.login(username="permuser", password="password")

        # Create test data
        self.graph = Graph.objects.create(name="Graph 1", description="Test Graph 1")
        Graph.objects.create(name="Graph 2", description="Test Graph 2")

    def test_get_graphs_success(self):
        response = self.client.get(reverse('api:graph_list'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 2)

    def test_get_graphs_no_permission(self):
        self.client.logout()
        self.client.login(username="testuser", password="password")
        response = self.client.get(reverse('api:graph_list'))
        self.assertEqual(response.status_code, 403)

    def test_create_graph_success(self):
        data = {
            "name": "Graph 3",
            "description": "Newly created graph"
        }
        response = self.client.post(reverse('api:graph_list'), data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Graph.objects.filter(name="Graph 3").exists())

    def test_create_graph_no_permission(self):
        self.client.logout()
        self.client.login(username="testuser", password="password")
        data = {
            "name": "Graph 3",
            "description": "Newly created graph"
        }
        response = self.client.post(reverse('api:graph_list'), data, format="json")
        self.assertEqual(response.status_code, 403)

class GraphDetailViewTests(TestCase):
    databases = {'default', 'graph'}
    
    @classmethod
    def setUpTestData(cls):
        # Shared setup for all test cases
        cls.graph = Graph.objects.create(name="Graph 1", description="Test Graph 1")
        cls.client = APIClient()
    
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user_with_perms = User.objects.create_user(username="permuser", password="password")

        permissions = ['view_graph', 'delete_graph', 'change_graph']
        for perm in permissions:
            self.user_with_perms.user_permissions.add(Permission.objects.get(codename=perm))

        self.client.login(username="permuser", password="password")

    def test_get_graphs_success(self):
        response = self.client.get(f'/api/graph/{self.graph.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['name'], "Graph 1")

    def test_update_graph_success(self):
        payload = {
            "name": "Updated Graph",
            "location": "http://example.com/updated_location",
            "has_header": True
        }
        response = self.client.put(
            f'/api/graph/{self.graph.id}/',
            payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        self.graph.refresh_from_db()
        self.assertEqual(self.graph.name, "Updated Graph")

    def test_delete_graph_success(self):
        response = self.client.delete(f'/api/graph/{self.graph.id}/')
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(Graph.DoesNotExist):
            Graph.objects.get(id=self.graph.id)

class GraphDatasetListViewTests(TestCase):
    databases = {'default', 'graph'}
    
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user_with_perms = User.objects.create_user(username="permuser", password="password")

        # Assign permissions
        permissions = ['view_graphdataset', 'add_graphdataset']
        for perm in permissions:
            self.user_with_perms.user_permissions.add(Permission.objects.get(codename=perm))

        # Authenticate the user with permissions
        self.client.login(username="permuser", password="password")

        # Create test data
        self.graph = Graph.objects.create(name="Graph 1", description="Test Graph 1")
        self.source = Source.objects.create(name="Source 1", location="http://example.com", has_header=True)
        GraphDataset.objects.create(graph=self.graph, label="Dataset 1", plot_type="line", source=self.source, column=0)

    def test_get_datasets_success(self):
        response = self.client.get(reverse('api:graph_dataset_list', args=[self.graph.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()['data']), 1)

    def test_create_dataset_success(self):
        data = {
            "label": "New Dataset",
            "plot_type": "bar",
            "is_axis": False,
            "source_id": self.source.id,
            "column_id": 1
        }
        response = self.client.post(reverse('api:graph_dataset_list', args=[self.graph.id]), data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(GraphDataset.objects.filter(label="New Dataset").exists())

class GraphDatasetDetailViewTests(TestCase):
    databases = {'default', 'graph'}
    
    def setUp(self):
        self.client = APIClient()

        # Create test users
        self.user = User.objects.create_user(username="testuser", password="password")
        self.user_with_perms = User.objects.create_user(username="permuser", password="password")

        # Assign permissions
        permissions = ['view_graphdataset', 'delete_graphdataset', 'change_graphdataset']
        for perm in permissions:
            self.user_with_perms.user_permissions.add(Permission.objects.get(codename=perm))

        # Authenticate the user with permissions
        self.client.login(username="permuser", password="password")

        # Create test data
        self.graph = Graph.objects.create(name="Graph 1", description="Test Graph 1")
        self.source = Source.objects.create(name="Source 1", location="http://example.com", has_header=True)
        self.dataset = GraphDataset.objects.create(
            graph=self.graph, label="Dataset 1", plot_type="line", source=self.source, column=0
        )

    def test_get_dataset_success(self):
        response = self.client.get(reverse('api:graph_dataset_detail', args=[self.graph.id, self.dataset.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['data']['label'], "Dataset 1")

    def test_delete_dataset_success(self):
        response = self.client.delete(reverse('api:graph_dataset_detail', args=[self.graph.id, self.dataset.id]))
        self.assertEqual(response.status_code, 200)
        self.assertFalse(GraphDataset.objects.filter(id=self.dataset.id).exists())
