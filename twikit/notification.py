from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .client.client import Client
    from .tweet import Tweet
    from .user import User


class Notification:
    """
    Attributes
    ----------
    id : :class:`str`
        The unique identifier of the notification.
    timestamp_ms : :class:`int`
        The timestamp of the notification in milliseconds.
    icon : :class:`dict`
        Dictionary containing icon data for the notification.
    message : :class:`str`
        The message text of the notification.
    tweet : :class:`.Tweet`
        The tweet associated with the notification.
    from_user : :class:`.User`
        The first user who triggered the notification. For merged
        notifications ("X and 3 others liked your post"), this is only
        one of possibly several users — see `from_users` for the full list.
    from_users : list[:class:`.User`]
        All users who triggered this notification. For a single-actor
        notification this is a one-element list equal to [from_user].
        For merged/aggregated notifications, X's API caps this list at
        10 entries even when the notification text reports a larger
        total (e.g. "and 13 others followed you") — the discrepancy is
        a platform-side truncation, not a parsing bug.
    """
    def __init__(
        self, client: Client, data: dict, tweet: Tweet,
        from_user: User, from_users: list[User] | None = None
    ) -> None:
        self._client = client
        self.tweet = tweet
        self.from_user = from_user
        self.from_users = from_users if from_users is not None else (
            [from_user] if from_user is not None else []
        )

        self.id: str = data['id']
        self.timestamp_ms: int = int(data['timestampMs'])
        self.icon: dict = data['icon']
        self.message: str = data['message']['text']

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Notification) and self.id == __value.id

    def __ne__(self, __value: object) -> bool:
        return not self == __value

    def __repr__(self) -> str:
        return f'<Notification id="{self.id}">'
