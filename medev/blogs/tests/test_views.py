import os
from django.http import response

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from ..models import Post


User = get_user_model()


class TestCreatePost(TestCase):
    """ Test cases for creating Posts. """

    def setUp(self):
        self.user = User.objects.create_user(
            username='User',
            email='test@mail.com',
            password='oxbuint1'
        )

    def test_can_create_post(self):
        """ Creates post with valid data. """
        data = {
            'title': 'Test title',
            'content': 'test content'
        }

        self.client.force_login(self.user)
        response = self.client.post(reverse('post-list'), data, format='multipart')
        
        self.assertEquals(response.status_code, 201)
        self.assertEquals(
            response.data,
            {
                'title': 'Test title',
                'content': 'test content',
                'slug': 'test-title',
                'author': {
                    'username': 'User',
                    'first_name': '',
                    'last_name': ''
                }
            }
        )

    def test_title_cannot_be_empty(self):
        """ Invalid data, title can't be empty. """
        data = {
            'content': 'test content'
        }

        self.client.force_login(self.user)
        response = self.client.post(reverse('post-list'), data)

        self.assertEquals(response.status_code, 400)
        self.assertEquals(response.data['title'][0], 'This field is required.')

    def test_must_be_logged_in_to_create_post(self):
        """ Can't create post, must be logged in. """
        data = {
            'title': 'Test title',
            'content': 'test content'
        }

        response = self.client.post(reverse('post-list'), data, format='multipart')
        
        self.assertEquals(response.status_code, 401)


class TestReadPost(TestCase):
    """ Test cases for creating Posts. """

    def setUp(self):
        self.user = User.objects.create_user(
            username='User',
            email='test@mail.com',
            password='oxbuint1'
        )

        self.user2 = User.objects.create_user(
            username='User2',
            email='test2@mail.com',
            password='oxbuint1'
        )

        self.post = Post.objects.create(
            title='Test title',
            content='test content',
            author=self.user
        )

        self.post2 = Post.objects.create(
            title='Test title2',
            content='test content',
            author=self.user
        )

        self.post3 = Post.objects.create(
            title='Test title2',
            content='test content',
            author=self.user2
        )

    def test_can_get_post_by_slug(self):
        """ Gets post with its slug. """

        response = self.client.get(reverse('post-detail', kwargs={'slug': self.post.slug}))

        self.assertEquals(response.status_code, 200)
        self.assertEquals(
            response.data,
            {
                'title': 'Test title',
                'content': 'test content',
                'slug': 'test-title',
                'author': {
                    'username': 'User',
                    'first_name': '',
                    'last_name': ''
                }
            }
        )

    def test_can_get_all_of_one_users_posts(self):
        """ Gets all posts by a user with the users slug. """

        url = f'{reverse("post-list")}?user={self.user.slug}'
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)
        self.assertEquals(len(response.data), 2)
        self.assertEquals(
            response.data[0],
            {
                'title': 'Test title',
                'content': 'test content',
                'slug': 'test-title',
                'author': {
                    'username': 'User',
                    'first_name': '',
                    'last_name': ''
                }
            }
        )

    def test_cant_get_post_must_provide_user(self):
        """ Cant get posts, must provide users. """

        response = self.client.get(reverse("post-list"))
        
        self.assertEquals(response.status_code, 400)
        self.assertEquals(
            response.data,
            {'error': 'must specify a user.'}
        )


class TestUpdatePost(TestCase):
    """ Test cases for updating Posts. """
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@mail.com',
            password='oxbuint1'
        )

        self.other_user = User.objects.create_user(
            username='other_user',
            email='other_user@mail.com',
            password='oxbuint1'
        )

        self.post = Post.objects.create(
            title='test_post',
            content='test123',
            author=self.owner
        )

    def test_can_update_own_article(self):
        """ Updates the user's article. """
        url = reverse('post-detail', kwargs={'slug': self.post.slug})

        data = {
            'title': 'updated title',
            'content': 'new content'
        }

        self.client.force_login(self.owner)
        response = self.client.patch(url, data, content_type='application/json')

        self.assertEquals(response.status_code, 200)
        self.assertEquals(response.data['title'], 'updated title')
        self.assertEquals(response.data['content'], 'new content')

    def test_cant_update_others_articles(self):
        """ Can't update someone else's article. """
        url = reverse('post-detail', kwargs={'slug': self.post.slug})

        data = {
            'title': 'updated title',
            'content': 'new content'
        }

        self.client.force_login(self.other_user)
        response = self.client.patch(url, data, content_type='application/json')

        self.assertEquals(response.status_code, 403)


class TestDeletePost(TestCase):
    """ Test cases for deleting Posts. """
    
    def setUp(self):
        self.owner = User.objects.create_user(
            username='owner',
            email='owner@mail.com',
            password='oxbuint1'
        )

        self.other_user = User.objects.create_user(
            username='other_user',
            email='other_user@mail.com',
            password='oxbuint1'
        )

        self.post = Post.objects.create(
            title='test_post',
            content='test123',
            author=self.owner
        )

    def test_can_delete_own_post(self):
        """ Updates the user's article. """
        url = reverse('post-detail', kwargs={'slug': self.post.slug})

        self.client.force_login(self.owner)
        response = self.client.delete(url)

        self.assertEquals(response.status_code, 204)
        self.assertEquals(Post.objects.all().count(), 0)

    def test_cant_update_others_articles(self):
        """ Can't update someone else's article. """
        url = reverse('post-detail', kwargs={'slug': self.post.slug})

        self.client.force_login(self.other_user)
        response = self.client.patch(url)

        self.assertEquals(response.status_code, 403)
        self.assertEquals(
            response.data['detail'],
            'You do not have permission to perform this action.'
        )