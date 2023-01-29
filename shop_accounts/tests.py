from rest_framework.test import APITestCase, APIRequestFactory, force_authenticate

from .models import User
from .views import *

class UserTest(APITestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
            email='user@gmail.com',
            password='123456',
            is_active= True,
        )

    def test_register(self):
        data = {
            'email':'new_user@gmail.com',
            'password':'4567',
            'password_confirm': '4567',
            'name':'test',
            'last_name':'TEST'
        }
        request = self.factory.post('register/', data, format='json')
        # print(request)
        view = RegistrationView.as_view()
        response = view(request)
        # print(response)
        # assert response.status_code == 201
        assert User.objects.filter(email=data['email']).exists()

    def test_login(self):
        data = {
            'email':'user@gmail.com',
            'password':'123456'
        }
        request = self.factory.post('login/', data, format='json')
        view = LoginView.as_view()
        response = view(request)
        # print(response.data)
        # 92266f9a9e77f444aa160fbb5b5092007857ddaf
        # 42241f0e1f5e4b69fb0b189ece91e1de6b29e050
        assert response.status_code == 200
        assert 'token' in response.data


    def test_change_password(self):
        data = {
            'old_password':'123456',
            'new_password':'654321',
            'new_password_confirm':'654321'
        }
        request = self.factory.post('changepass/', data, format='json')
        force_authenticate(request, user=self.user)
        view = ChangePasswordView.as_view()
        response = view(request)
        
        assert response.status_code == 200


    def test_forgot_password(self):
        data={
            'email':'user@gmail.com'
        }
        request = self.factory.post('forgotpass/', data, format='json')
        view = ForgotPasswordView.as_view()
        response = view(request)
        print(response.data)

        assert response.status_code == 200

    def test_logout(self):
        request = self.factory.post('logout/', format='json')
        force_authenticate(request,user=self.user)
        view = LogoutView.as_view()
        response = view(request)
        print(response.data)