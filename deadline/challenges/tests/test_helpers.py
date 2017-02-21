import random
from django.test import TestCase
from challenges.models import Challenge, Submission, TestCase
from accounts.models import User
from challenges.helper import grade_result, update_user_score


class GradeResultTests(TestCase):
    """
    Test the grade_results function, which should update the submission's score in accordance to the passed tests
    """

    def setUp(self):
        self.user = User(email="hello@abv.bg", password='123', username='me')
        self.user.save()
        self.challenge = Challenge(name='Hello World!', description='Say hello',
                                   rating=10, score=100, test_file_name='smth',
                                   test_case_count=5)
        self.challenge.save()
        self.submission = Submission(challenge=self.challenge, author=self.user,
                                     code='hack you', task_id='123', result_score=0)
        self.submission.save()
        # create the test cases
        self.test_cases = []
        for _ in range(self.challenge.test_case_count):
            tst_case = TestCase(submission=self.submission, pending=False, success=random.choice[True, False])
            tst_case.save()
            self.test_cases.append(tst_case)

    def test_grade_result(self):
        num_successful_tests = len([True for test_case in self.test_cases if not test_case.pending and test_case.success])
        expected_score = self.challenge.score / num_successful_tests

        grade_result(submission=self.submission)

        # Should have updated the submission's score
        self.assertEqual(self.submission.result_score, expected_score)


class UpdateUserScoreTests(TestCase):
    """
    the update_user_score function should update the user's overall score given a submission by him.
    Note: It should only update it if the user has a previous submission (or none at all) which has a lower score.
    """
    def setUp(self):
        self.user = User(email="hello@abv.bg", password='123', username='me')
        self.user.save()
        self.challenge = Challenge(name='Hello World!', description='Say hello',
                                   rating=10, score=100, test_file_name='smth',
                                   test_case_count=3)
        self.challenge.save()
        self.submission = Submission(challenge=self.challenge, author=self.user,
                                     code='hack you', task_id='123', result_score=20)
        self.submission.save()
        # add this submisssions score to him
        self.user.score = 20
        self.user.save()

    def test_submission_with_lower_score_should_not_update(self):
        lower_submission = Submission(challenge=self.challenge, author=self.user,
                                     code='hack you', task_id='123', result_score=10)
        lower_submission.save()

        result = update_user_score(user=self.user, submission=lower_submission)
        self.assertFalse(result)
        self.user.refresh_from_db()
        self.assertEqual(self.user, 20)  # should not have changed

    def test_submission_with_higher_score_should_update(self):
        higher_submission = Submission(challenge=self.challenge, author=self.user,
                                       code='hack you', task_id='123', result_score=30)
        higher_submission.save()

        result = update_user_score(user=self.user, submission=higher_submission)
        self.assertTrue(result)
        self.user.refresh_from_db()
        self.assertEqual(self.user, 30)  # should have changed

    def test_submission_other_challenge_should_update(self):
        """ Since the user does not have a submission for this challenge, it should update his score """
        new_challenge = Challenge(name='NEW MAN', description='NEW',
                                   rating=10, score=100, test_file_name='smth',
                                   test_case_count=3)
        new_challenge.save()
        new_submission = Submission(challenge=new_challenge, author=self.user,
                                      code='hack you', task_id='123', result_score=100)
        new_submission.save()

        result = update_user_score(user=self.user, submission=new_challenge)
        self.assertTrue(result)
        self.user.refresh_from_db()
        self.assertEqual(self.user, 120)  # should have updated it