from django.test import TestCase

from education.models import Course, Lesson, Homework, HomeworkTask, HomeworkTaskTest
from education.tests.factories import HomeworkTaskDescriptionFactory


class HomeworkTaskTestTests(TestCase):
    def setUp(self):
        self.course = Course.objects.create(name='tank', difficulty=1, is_under_construction=False)
        self.lesson = Lesson.objects.create(lesson_number=1, course=self.course, intro='', content='',
                                            annexation='', is_under_construction=False)
        self.hw = Homework.objects.create(is_mandatory=False, lesson=self.lesson)
        self.hw_task = HomeworkTask.objects.create(test_case_count=1, description=HomeworkTaskDescriptionFactory(), is_mandatory=True, consecutive_number=1, difficulty=10,
                                                   homework=self.hw)

    def test_creation(self):
        hw_t_test = HomeworkTaskTest.objects.create(input_file_path='hello', output_file_path='bye', consecutive_number=1, task=self.hw_task)
        # should not raise anything

    def test_cannot_create_if_given_inconsecutive_number(self):
        HomeworkTaskTest.objects.create(input_file_path='hello', output_file_path='bye', consecutive_number=1, task=self.hw_task)

        # there is already one test that is #1, as such we cannot put in another #1
        with self.assertRaises(Exception):
            HomeworkTaskTest.objects.create(input_file_path='hello', output_file_path='bye', consecutive_number=1, task=self.hw_task)