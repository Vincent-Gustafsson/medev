from django.test import TestCase
from django.urls import reverse
from django.core import mail
from django.contrib.auth import get_user_model

from rest_framework.authtoken.models import Token


User = get_user_model()


class TestRegistration(TestCase):
    """ Test cases for registration. """
    # TODO WRITE TEST FOR S3 PROFILE UPLOADING //https://github.com/spulec/moto
    def setUp(self):
        self.test_user = User(
            username='User',
            email='test2@mail.com',
            password='oxbuint1'
        )

        self.test_data = {
            'username': 'User2',
            'email': 'test@mail.com',
            'password1': 'oxbuint1',
            'password2': 'oxbuint1'
        }

    def test_can_register(self):
        """ Registers user with valid data """

        response = self.client.post(reverse('rest_register'), self.test_data)

        self.assertIn('key', response.data)
        self.assertEqual(
            Token.objects.get().user.username,
            self.test_data['username']
        )

    def test_can_not_register_username_taken(self):
        """ Can't register because username is already taken. """

        self.test_data['username'] = 'User'

        self.test_user.save()

        response = self.client.post(reverse('rest_register'), self.test_data)

        self.assertEqual(
            response.data['username'][0],
            'User with this username already exists.'
        )

    def test_can_not_register_email_taken(self):
        """ Can't register because email is already taken. """

        self.test_data['email'] = 'test2@mail.com'

        self.test_user.save()

        response = self.client.post(reverse('rest_register'), self.test_data)

        self.assertEqual(
            response.data['email'][0],
            'A user is already registered with this e-mail address.'
        )

    def test_can_not_register_passwords_different(self):
        """ Can't register because passwords are different. """

        self.test_data['password2'] = 'oxbuint2'

        response = self.client.post(reverse('rest_register'), self.test_data)

        self.assertEqual(
            response.data['non_field_errors'][0],
            'The two password fields didn\'t match.'
        )


class TestLogin(TestCase):
    """ Test cases for login. """

    def test_can_login(self):
        """ Can login with valid data """

        data = {
            'username': 'User',
            'password': 'oxbuint1'
        }

        User.objects.create_user(
            username='User',
            email='test@mail.com',
            password='oxbuint1'
        )

        response = self.client.post(reverse('rest_login'), data)

        self.assertIn('key', response.data)
        self.assertEqual(
            Token.objects.get().user.username,
            data['username']
        )


class TestLogout(TestCase):
    """ Test cases for logout. """

    def test_can_login(self):
        """ Can logout with valid data """

        user = User.objects.create_user(
            username='User',
            email='test@mail.com',
            password='oxbuint1'
        )

        self.client.force_login(user)
        response = self.client.post(reverse('rest_logout'))

        self.assertEquals(
            response.data['detail'],
            'Successfully logged out.'
        )


class TestUserDetail(TestCase):
    """ Test cases for user details view. """

    def test_can_get_details(self):
        """ The user can fetch their details. """
        user = User.objects.create_user(
            username='User',
            email='test@mail.com',
            password='oxbuint1'
        )

        self.client.force_login(user)
        response = self.client.get(reverse('rest_user_details'))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 7)


class TestChangePassword(TestCase):
    """ Test cases for password change view. """

    def test_can_change_password(self):
        """ Can update password with valid data. """
        user = User.objects.create_user(
            username='User',
            email='test@mail.com',
            password='oxbuint1'
        )

        data = {
            'new_password1': 'buxuint123',
            'new_password2': 'buxuint123'
        }

        self.client.force_login(user)
        response = self.client.post(reverse('rest_password_change'), data)

        self.assertEquals(response.status_code, 200)

    def test_can_not_change_password_different_passwords(self):
        """ Can't update password with different passwords. """
        user = User.objects.create_user(
            username='User',
            email='test@mail.com',
            password='oxbuint1'
        )

        data = {
            'new_password1': 'buxuint123',
            'new_password2': 'buxuint1234'
        }

        self.client.force_login(user)
        response = self.client.post(reverse('rest_password_change'), data)

        self.assertEquals(response.status_code, 400)


# TODO CREATE TESTS FOR PASSWORD RESETTING
class TestResetPassword(TestCase):
    """ Test cases for password reset views. """

    def test_can_reset_password(self):
        """ The user can reset their password. From start, to finish. """
        user = User.objects.create_user(
            username='User',
            email='test@mail.com',
            password='oxbuint1'
        )

        # get the email with UID and TOKEN.
        data = {
            'email': user.email
        }

        self.client.force_login(user)
        response = self.client.post(reverse('rest_password_reset'), data)

        self.assertEqual(
            response.data['detail'],
            'Password reset e-mail has been sent.'
        )
        self.assertEqual(len(mail.outbox), 1)

        confirmation_link = mail.outbox[0].body.split('\n')[5]
        uid = confirmation_link.split('/')[6]
        token = confirmation_link.split('/')[7]

        # Change the password.
        confirmation_data = {
            'new_password1': 'newpassword123',
            'new_password2': 'newpassword123',
            'uid': uid,
            'token': token
        }

        self.client.force_login(user)
        response = self.client.post(
            reverse(
                'password_reset_confirm',
                kwargs={'uidb64': uid, 'token': token}
            ),
            confirmation_data
        )

        self.assertEquals(
            response.data['detail'],
            'Password has been reset with the new password.'
        )
