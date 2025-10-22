from app.posts.models import Post
from app.users.models import User
from app.votes.policies import VotePolicy
from tests.shared.test_helpers import random_user_id


class TestVotePolicy:
    def test_can_vote_active_user_not_owner(self):
        """
        Should allow voting if user is active and not the owner of the post.
        """
        post = Post(owner_id=random_user_id())
        active_non_owner_user = User(id=random_user_id(), is_active=True)

        assert VotePolicy.can_vote(post, active_non_owner_user) is True

    def test_can_vote_inactive_user(self):
        """
        Should not allow voting if user is inactive, even if not the owner.
        """
        post = Post(owner_id=random_user_id())
        inactive_non_owner_user = User(id=random_user_id(), is_active=False)

        assert VotePolicy.can_vote(post, inactive_non_owner_user) is False

    def test_can_vote_owner(self):
        """
        Should not allow voting if user is the owner, even if active.
        """
        user_id = random_user_id()
        post = Post(owner_id=user_id)
        active_owner_user = User(id=user_id, is_active=True)

        assert VotePolicy.can_vote(post, active_owner_user) is False

    def test_can_vote_owner_inactive(self):
        """
        Should not allow voting if user is the owner and inactive.
        """
        user_id = random_user_id()
        post = Post(owner_id=user_id)
        inactive_owner_user = User(id=user_id, is_active=False)

        assert VotePolicy.can_vote(post, inactive_owner_user) is False
