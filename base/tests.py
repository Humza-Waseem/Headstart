from django.test import TestCase
import pytest
from django.urls import reverse
# Create your tests here.

def TestUserLogin(TestCase):
        
        if (request.user):
            return True
        else:
            return False
        
        
        


@pytest.mark.django_db
def test_login_view(client):
    
    user = User.objects.create_user(username='testuser', password='testpassword')

    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'testpassword'})
    assert response.status_code == 302  
    assert response.url == reverse('home')

    response = client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
    assert response.status_code == 200  
    assert 'Invalid credentials' in response.content.decode()
    
class SimpleTest(TestCase):
    def test_basic_addition(self):
        self.assertEqual(1 + 1, 2)
        
        
    
def func(x):
    return x + 1


def test_answer():
    assert func(3) == 5





import pytest


def f():
    raise SystemExit(1)


def test_mytest():
    with pytest.raises(SystemExit):
        f()