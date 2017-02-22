from django.test import TestCase
from rest_framework.renderers import JSONRenderer

from challenges.models import ChallengeCategory, SubCategory, Challenge, User
from challenges.serializers import ChallengeCategorySerializer, SubCategorySerializer


class CategoryModelTest(TestCase):
    def setUp(self):
        self.c1 = ChallengeCategory(name='Test')
        self.sub1 = SubCategory(name='Unit', meta_category=self.c1)
        self.sub2 = SubCategory(name='Mock', meta_category=self.c1)
        self.sub3 = SubCategory(name='Patch', meta_category=self.c1)
        self.sub1.save();self.sub2.save();self.sub3.save()

    def test_relationships(self):
        """ The categories should be connected"""
        self.assertIn(self.sub1, self.c1.sub_categories.all())
        self.assertEqual(self.sub1.meta_category, self.c1)

    def test_serialize(self):
        """ the Category should show all its subcategories """
        expected_json = '{"name":"Test","sub_categories":["Unit","Mock","Patch"]}'
        received_data = JSONRenderer().render(ChallengeCategorySerializer(self.c1).data)

        self.assertEqual(received_data.decode('utf-8'), expected_json)


class CategoryViewTest(TestCase):
    def setUp(self):
        self.c1 = ChallengeCategory(name='Test')
        self.c2 = ChallengeCategory(name='Data')
        self.c3 = ChallengeCategory(name='Structures')
        self.c4 = ChallengeCategory(name='Rustlang')
        self.c5 = ChallengeCategory(name='Others')
        self.c1.save();self.c2.save();self.c3.save();self.c4.save();self.c5.save()

    def test_view_all_should_return_all_categories(self):
        response = self.client.get('/challenges/categories/all')
        print(response.data)
        self.assertEqual(response.data, ChallengeCategorySerializer([self.c1, self.c2, self.c3, self.c4, self.c5],
                                        many=True).data)


class SubCategoryModelTest(TestCase):
    def setUp(self):
        self.c1 = ChallengeCategory(name='Test')
        self.sub1 = SubCategory(name='Unit', meta_category=self.c1)
        self.sub2 = SubCategory(name='Mock', meta_category=self.c1)
        self.sub3 = SubCategory(name='Patch', meta_category=self.c1)
        self.sub1.save(); self.sub2.save(); self.sub3.save()

    def test_serialize(self):
        """ Ths Subcategory should show all its challenges"""
        c = Challenge(name='TestThis', rating=5, score=10, description='What up', test_case_count=5, category=self.sub1)
        c.save()
        expected_json = '{"name":"Unit","challenges":[{"id":1,"name":"TestThis","rating":5,"score":10}]}'
        received_data = JSONRenderer().render(SubCategorySerializer(self.sub1).data)
        self.assertEqual(received_data.decode('utf-8'), expected_json)


class SubCategoryViewTest(TestCase):
    def setUp(self):
        auth_user = User(username='123', password='123', email='123@abv.bg', score=123)
        auth_user.save()
        self.auth_token = 'Token {}'.format(auth_user.auth_token.key)
        self.c1 = ChallengeCategory(name='Test')
        self.sub1 = SubCategory(name='Unit Tests', meta_category=self.c1)
        self.sub1.save()
        c = Challenge(name='TestThis', rating=5, score=10, description='What up', test_case_count=5, category=self.sub1)
        c.save()

    def test_view_subcategory_detail_should_show(self):
        response = self.client.get('/challenges/subcategories/{}'.format(self.sub1.name),
                                   HTTP_AUTHORIZATION=self.auth_token)

        self.assertEqual(response.status_code, 200)
        # Should get the information about a specific subcategory
        self.assertEqual(response.data, SubCategorySerializer(self.sub1).data)

    def test_view_unauthorized_should_401(self):
        response = self.client.get('/challenges/subcategories/{}'.format(self.sub1.name))
        self.assertEqual(response.status_code, 401)

    def test_view_invalid_challenge_should_404(self):
        response = self.client.get('/challenges/subcategories/{}'.format('" OR 1=1;'),
                                   HTTP_AUTHORIZATION=self.auth_token)
        self.assertEqual(response.status_code, 404)
