from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from django.urls import reverse
from faker import Faker
from faker.providers import internet
from random import choices

def get_user_url(user: User) -> str:
  return reverse('user-detail', args=[user.id])
def create_password(length: int) -> str:
  chars = "1234567890qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM<>,.-_$%&()[]"
  return "".join(choices(chars, k=length))

def create_user(username=None, email=None, password=None, password_length=15) -> User:
  fake = Faker()
  fake.add_provider(internet)
  
  if not username:
    username = fake.user_name()
  if not email:
    email = fake.ascii_safe_email()
  if not password:
    password = create_password(password_length)
  return User.objects.create(username=username, email=email, password=password)
  
class UsersViewsListTests(APITestCase):
  def test_read_user_displays_correctly(self):
    """
    GET to /users and /users/<id> return status 200
    """
    response = self.client.get(reverse('user-list'))
    self.assertEqual(response.status_code, 200)
    user = create_user()
    response = self.client.get(reverse('user-detail', args=[user.id]))
    self.assertEqual(response.status_code, 200)
  
  def test_post_forbidden(self):
    """
    POST shouldn't be reached by any user
    """
    user = create_user()
    new_username = "new-username"
    body = {
      "username": new_username,
      "email": user.email,
      "password": create_password(15)
    }
    response = self.client.post(
      reverse('user-list'),
      data=body
    )
    self.assertEqual(response.status_code, 401, 'post in /users need credentials')
    self.client.force_authenticate(user=user)
    response = self.client.post(
      reverse('user-list'),
      data=body
    )
    self.assertEqual(response.status_code, 403, 'post in /users is forbidden for authenticated users')
    
  def test_put_allowed_to_self(self):
    """
    PUT method only allowed for self.
    """
    owner_user = create_user()
    new_username = "new-username"
    body = {
      "username": new_username,
      "email": owner_user.email,
      "password": create_password(15)
    }
    # PUT from non auth user
    response = self.client.put(get_user_url(owner_user), data=body)
    self.assertEqual(response.status_code, 401, 'put in /users/id need credentials')
    
    # PUT from auth user but not self
    other_user = create_user()
    self.client.force_authenticate(user=other_user)
    response = self.client.put(get_user_url(owner_user), data=body)
    self.assertEqual(response.status_code, 403, 'put in /users/id is forbidden for non self user')
    
    # PUT from auth self
    self.client.force_authenticate(user=owner_user)
    response = self.client.put(get_user_url(owner_user), data=body)
    self.assertEqual(response.status_code, 200)
    updated_user = User.objects.get(id=owner_user.id)
    self.assertEqual(updated_user.username, new_username, 'changes not applied')
  
  def test_patch_allowed_to_self(self):
    """
    PATCH method only allowed for self.
    """
    user = create_user()
    new_username = "new-username"
    body = {
      "username": new_username
    }
    # patch from non auth users
    response = self.client.patch(get_user_url(user), data=body)
    self.assertEqual(response.status_code, 401, 'patch to /users/id need credentials')
    
    # patch from other auth users
    other_user = create_user()
    self.client.force_authenticate(user=other_user)
    response = self.client.patch(get_user_url(user), data=body)
    self.assertEqual(response.status_code, 403, 'patch to /users/id is forbidden for non self user')
    
    # patch from self
    self.client.force_authenticate(user=user)
    response = self.client.patch(get_user_url(user), data=body)
    self.assertEqual(response.status_code, 200)
    updated_user = User.objects.get(id=user.id)
    self.assertEqual(updated_user.username, new_username, 'changes not applied')
    
  def test_delete_allowed_to_self(self):
    """
    DELETE method only allowed for self.
    """
    user = create_user()
    
    # delete from non auth
    response = self.client.delete(get_user_url(user))
    self.assertEqual(response.status_code, 401, 'delete to /users/id need credentials')
    
    # delete from other auth user
    other_user = create_user()
    self.client.force_authenticate(user=other_user)
    response = self.client.delete(get_user_url(user))
    self.assertEqual(response.status_code, 403, 'delete to /users/id is forbidden for non self user')
    
    self.client.force_authenticate(user=user)
    response = self.client.delete(get_user_url(user))
    self.assertEqual(response.status_code, 204)
    with self.assertRaises(User.DoesNotExist):
      User.objects.get(id=user.id)

class LoginAndRegistrationTests(APITestCase):
  def test_unique_username_and_email(self):
    """
    Usernames and emails must be unique
    """
    pass
  def test_password(self):
    """
    Passwords must be in X format
    """
    pass
  def test_login_for_non_registered(self):
    """
    Login to non registered should redirect to register
    """
  def test_success_register_and_login(self):
    """
    Testing happy path for users
    """
    pass
  def test_register_for_already_registered(self):
    """
    Users already registered should be redirected to login
    """