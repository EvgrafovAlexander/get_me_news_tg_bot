from db import add_subscriber, get_all_subscribers, remove_subscriber


class SubscriberService:
    @staticmethod
    def subscribe(chat_id: str):
        add_subscriber(chat_id)

    @staticmethod
    def unsubscribe(chat_id: str):
        remove_subscriber(chat_id)

    @staticmethod
    def get_all() -> list[str]:
        return get_all_subscribers()
