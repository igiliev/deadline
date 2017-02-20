from django.db import models

from accounts.models import User


# Create your models here.
class Challenge(models.Model):
    name = models.CharField(unique=True, max_length=30)
    description = models.CharField(max_length=3000)
    rating = models.IntegerField()
    score = models.IntegerField()
    # TODO: Add category once ready

    def get_absolute_url(self):
        return '/challenges/{}'.format(self.id)


class Submission(models.Model):
    challenge = models.ForeignKey(Challenge)
    author = models.ForeignKey(User)
    code = models.CharField(max_length=4000, blank=False)

    def get_absolute_url(self):
        return '/challenges/{}/submissions/{}'.format(self.challenge_id, self.id)


class TestCase(models.Model):
    submission = models.ForeignKey(Submission)
    time = models.CharField(default='0.00s', max_length=5)
    success = models.BooleanField(default=False)
    pending = models.BooleanField(default=True)

    def get_absolute_url(self):
        return '/challenges/{}/submissions/{}/test/{}'.format(
            self.submission.challenge_id, self.submission.id, self.id)