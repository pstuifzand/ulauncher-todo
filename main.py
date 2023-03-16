from ulauncher.api.client.Extension import Extension
from ulauncher.api.client.EventListener import EventListener
from ulauncher.api.shared.event import KeywordQueryEvent, ItemEnterEvent
from ulauncher.api.shared.item.ExtensionResultItem import ExtensionResultItem
from ulauncher.api.shared.action.RenderResultListAction import RenderResultListAction
from ulauncher.api.shared.action.HideWindowAction import HideWindowAction
from ulauncher.api.shared.action.ExtensionCustomAction import ExtensionCustomAction
from ulauncher.api.shared.action.DoNothingAction import DoNothingAction
import requests
import logging

logger = logging.getLogger(__name__)

ICON_FILE = 'images/icon2.png'


class TodoExtension(Extension):

    def __init__(self):
        super().__init__()
        self.subscribe(KeywordQueryEvent, KeywordQueryEventListener())
        self.subscribe(ItemEnterEvent, ItemEnterEventListener())


class ItemEnterEventListener(EventListener):

    def on_event(self, event, extension):
        event_type, message = event.get_data()
        if event_type == "create":
            list = extension.preferences["todo_list"]
            token = extension.preferences["todo_token"]
            r = requests.post("https://cms.p83.nl/items/todo_items",
                              headers={"Authorization": f"Bearer {token}"},
                              json={"list": list, "title": message})
            logger.warning(r)
        else:
            logger.warning("unknown event: %r %r", event_type, message)


class KeywordQueryEventListener(EventListener):

    def get_action_to_render(self, name, description, on_enter=None):
        item = ExtensionResultItem(name=name,
                                   description=description,
                                   icon=ICON_FILE,
                                   on_enter=on_enter or DoNothingAction())
        return RenderResultListAction([item])

    def on_event(self, event, extension):
        query = event.get_argument() or ''
        if query:
            todo = query
            data = ("create", todo)
            return self.get_action_to_render(name="Create todo item",
                                             description="Todo: %s" % todo,
                                             on_enter=ExtensionCustomAction(data))
        else:
            return self.get_action_to_render(name="Type in your todo",
                                             description="Example: todo Buy milk")

if __name__ == '__main__':
    TodoExtension().run()
