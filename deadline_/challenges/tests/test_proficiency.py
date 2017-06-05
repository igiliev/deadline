from django.test import TestCase
from challenges.models import Proficiency, MainCategory, SubCategory, UserSubcategoryProficiency, User, Challenge
from challenges.tests.factories import UserFactory, ChallengeFactory, ChallengeDescFactory


class ProficiencyModelTests(TestCase):
    def setUp(self):
        self.worst_prof = Proficiency.objects.create(name="worst", needed_percentage=1)
        self.middle_prof = Proficiency.objects.create(name="middle", needed_percentage=50)
        self.second_worst_prof = Proficiency.objects.create(name="second worst", needed_percentage=25)
        self.top_prof = Proficiency.objects.create(name="best", needed_percentage=100)

    def test_fetch_next_proficiency(self):
        """ Given a percentage, should return the next proficiency up the ladder """
        self.assertEqual(self.worst_prof.fetch_next_proficiency(), self.second_worst_prof)
        self.assertEqual(self.middle_prof.fetch_next_proficiency(), self.top_prof)

    def test_fetch_next_proficiency_returns_none_on_no_better_prof(self):
        self.assertIsNone(self.top_prof.fetch_next_proficiency())

    def test_fetch_next_proficiency_returns_strictly_higher_proficiency(self):
        """ Given two proficiencies with equal needed_percentage,
            the method should return one that strictly has a higher percentage"""
        self.middle_prof2 = Proficiency.objects.create(name="middle2", needed_percentage=50)
        self.assertNotEqual(self.middle_prof.fetch_next_proficiency(), self.middle_prof2)


class UserSubcategoryProficiencyModelTest(TestCase):
    def setUp(self):
        self.c1 = MainCategory.objects.create(name='Tank')
        self.sub1 = SubCategory.objects.create(name='Unit', meta_category=self.c1)
        # create two different challenges
        self.chal = Challenge.objects.create(name='Hello', difficulty=1, score=200, test_case_count=5, category=self.sub1,
                          description=ChallengeDescFactory(), test_file_name='tank')
        self.chal2 = Challenge.objects.create(name='Hello2', difficulty=1, score=200, test_case_count=5, category=self.sub1,
                          description=ChallengeDescFactory(), test_file_name='tank2')
        self.max_challenge_score = 400
        Proficiency.objects.create(name='starter', needed_percentage=0)
        Proficiency.objects.create(name='mid', needed_percentage=50)
        self.top_prof = Proficiency.objects.create(name='top', needed_percentage=100)
        self.user: User = UserFactory()
        self.user.save()

    def test_user_id_and_subcat_are_unique_together(self):
        # NOTE: One UserSubcategoryProficiency is already created on user model creation
        with self.assertRaises(Exception):
            sec_sub = UserSubcategoryProficiency(self.user.id, self.sub1.id, 0)
            sec_sub.save()

    def test_to_update_proficiency_works_correctly(self):
        subcat_proficiency: UserSubcategoryProficiency = self.user.fetch_subcategory_proficiency(self.sub1.id)
        subcat_proficiency.user_score = 200  # this places the user right at the 50% mark and should update his prof to mid
        subcat_proficiency.save()

        self.assertTrue(subcat_proficiency.to_update_proficiency())

    def test_to_update_proficiency_returns_false(self):
        subcat_proficiency: UserSubcategoryProficiency = self.user.fetch_subcategory_proficiency(self.sub1.id)
        subcat_proficiency.user_score = 199 # this places the user right at the 49% mark
        # meaning he should not update his proficiency
        subcat_proficiency.save()

        self.assertFalse(subcat_proficiency.to_update_proficiency())

    def test_to_update_proficiency_when_no_better_prof_exists(self):
        subcat_proficiency: UserSubcategoryProficiency = self.user.fetch_subcategory_proficiency(self.sub1.id)
        subcat_proficiency.proficiency = self.top_prof
        subcat_proficiency.user_score = 400 # 100% mark
        subcat_proficiency.save()

        self.assertFalse(subcat_proficiency.to_update_proficiency())

    def test_to_update_proficiency_user_has_high_prof_but_percentage_low_should_not_update(self):
        """
        This can be achieved when a user has scored a high proficiency in the best with a high percentage,
        but some time later more challenges have been added and his percentage is not as good anymore.
        Desired behavior is to have the user keep his high proficiency
        """
        subcat_proficiency: UserSubcategoryProficiency = self.user.fetch_subcategory_proficiency(self.sub1.id)
        subcat_proficiency.proficiency = self.top_prof
        subcat_proficiency.user_score = 202 # ~51% mark
        # top prof requires 100% but user's percentage is 51%

        subcat_proficiency.save()
        self.assertFalse(subcat_proficiency.to_update_proficiency())
