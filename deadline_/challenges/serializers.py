from collections import OrderedDict

from rest_framework import serializers
from challenges.models import Challenge, Submission, TestCase, MainCategory, SubCategory, ChallengeDescription, \
    Language, UserSubcategoryProficiency, SubmissionComment, ChallengeComment
from challenges.models import User


class ChallengeDescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChallengeDescription
        exclude = ('id', )


class ChallengeCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ChallengeComment
        fields = ('id', 'author', 'content')


class ChallengeSerializer(serializers.ModelSerializer):
    description = ChallengeDescriptionSerializer()
    category = serializers.StringRelatedField()
    supported_languages = serializers.StringRelatedField(many=True)
    comments = ChallengeCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Challenge
        fields = ('id', 'name', 'difficulty', 'score', 'description', 'test_case_count',
                  'category', 'supported_languages', 'comments')


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Language
        fields = '__all__'


class LimitedChallengeSerializer(serializers.ModelSerializer):
    """
    Returns the main information about a Challenge
        and the current user's max score (this requires the challenge object to have user_max_score attached to it).
    Used, for example, when listing challenges.
    """
    category = serializers.StringRelatedField()

    class Meta:
        model = Challenge
        fields = ('id', 'name', 'difficulty', 'score', 'category')  # user_max_score is added as well but more implicitly

    def to_representation(self, instance):
        """
        Modification to add the user_max_score to the serialized data
        """
        result = super().to_representation(instance)

        user = getattr(self.context.get('request', None), 'user', None)
        if user is None:
            result['user_max_score'] = 0
        else:
            result['user_max_score'] = user.fetch_max_score_for_challenge(challenge_id=instance.id)

        return result


class SubmissionCommentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = SubmissionComment
        fields = ('id', 'author', 'content')


class SubmissionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    challenge = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    result_score = serializers.IntegerField(read_only=True)
    pending = serializers.BooleanField(read_only=True)
    comments = SubmissionCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Submission
        fields = ('id', 'challenge', 'author', 'code', 'result_score', 'pending', 'created_at',
                  'compiled', 'compile_error_message', 'language', 'timed_out', 'comments')

    def to_representation(self, instance: Submission):
        """
        Modification to add four variables to the serialized data
            - user_has_voted - Boolean indicating if the user has voted at all for this
            - user_has_upvoted - Boolean indicating if the user has upvoted the submission (user_has_voted must be true)
            - upvote_count - int showing the amount of upvotes this submission has
            - downvote_count - int showing the amount of downvotes this submission has
        """
        from accounts.models import User
        result = super().to_representation(instance)
        user: User = getattr(self.context.get('request', None), 'user', None)
        # TODO: Move to helper

        result['language'] = Language.objects.get(id=result['language']).name
        if user is None:
            result['user_has_voted'] = False
            result['user_has_upvoted'] = False
        else:
            user_vote = user.get_vote_for_submission(submission_id=instance.id)
            if user_vote is None:
                result['user_has_voted'] = False
                result['user_has_upvoted'] = False
            else:
                result['user_has_voted'] = True
                result['user_has_upvoted'] = user_vote.is_upvote

        upvote_count, downvote_count = instance.get_votes_count()
        result['upvote_count'] = upvote_count
        result['downvote_count'] = downvote_count

        return result


class LimitedSubmissionSerializer(serializers.ModelSerializer):
    """ Serializes everything about a submission except its code """
    id = serializers.IntegerField(read_only=True)
    challenge = serializers.PrimaryKeyRelatedField(read_only=True)
    author = serializers.StringRelatedField(read_only=True)
    result_score = serializers.IntegerField(read_only=True)
    pending = serializers.BooleanField(read_only=True)

    class Meta:
        model = Submission
        fields = ('id', 'challenge', 'author', 'result_score', 'pending', 'created_at',
                  'compiled', 'compile_error_message', 'language', 'timed_out')

    def to_representation(self, instance: Submission):
        """
        Modification to add four variables to the serialized data
            - user_has_voted - Boolean indicating if the user has voted at all for this
            - user_has_upvoted - Boolean indicating if the user has upvoted the submission (user_has_voted must be true)
            - upvote_count - int showing the amount of upvotes this submission has
            - downvote_count - int showing the amount of downvotes this submission has
        """
        from accounts.models import User
        result = super().to_representation(instance)
        user:User = getattr(self.context.get('request', None), 'user', None)
        # TODO: Move to helper

        result['language'] = Language.objects.get(id=result['language']).name
        if user is None:
            result['user_has_voted'] = False
            result['user_has_upvoted'] = False
        else:
            user_vote = user.get_vote_for_submission(submission_id=instance.id)
            if user_vote is None:
                result['user_has_voted'] = False
                result['user_has_upvoted'] = False
            else:
                result['user_has_voted'] = True
                result['user_has_upvoted'] = user_vote.is_upvote

        upvote_count, downvote_count = instance.get_votes_count()
        result['upvote_count'] = upvote_count
        result['downvote_count'] = downvote_count

        return result


class TestCaseSerializer(serializers.ModelSerializer):
    submission = serializers.PrimaryKeyRelatedField(read_only=True)
    success = serializers.BooleanField(read_only=True)
    pending = serializers.BooleanField(read_only=True)
    time = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    traceback = serializers.CharField(read_only=True)
    error_message = serializers.CharField(read_only=True)

    class Meta:
        model = TestCase
        fields = ('submission', 'pending', 'success', 'time', 'description', 'traceback', 'error_message', 'timed_out')


class MainCategorySerializer(serializers.ModelSerializer):
    sub_categories = serializers.StringRelatedField(many=True)

    class Meta:
        model = MainCategory
        fields = ('name', 'sub_categories')


class SubCategorySerializer(serializers.ModelSerializer):
    challenges = LimitedChallengeSerializer(many=True)

    class Meta:
        model = SubCategory
        fields = ('name', 'challenges', 'max_score')

    def to_representation(self, instance):
        result = super().to_representation(instance)

        # attach the current user's proficiency
        user: User = getattr(self.context.get('request', None), 'user', None)
        user_proficiency: UserSubcategoryProficiency = user.fetch_subcategory_proficiency(subcategory_id=instance.id)
        proficiency_object = OrderedDict()
        proficiency_object['name'] = user_proficiency.proficiency.name
        max_score = sum(ch.score for ch in instance.challenges.all())  # TODO: Store somewhere
        proficiency_object['percentage_progress'] = int((user_proficiency.user_score / max_score) * 100)
        result['proficiency'] = proficiency_object

        return result
