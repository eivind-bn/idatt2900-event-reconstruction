import cv2

from core.constants.colors import BLACK, WHITE, BLUE
from core.event.subjects import CLOSING, OPENING, BROADCASTER_JOINED
from core.sink.module import Sink


class Window(Sink):

    def __init__(self,
                 title,
                 void_color=BLACK,
                 pos_color=WHITE,
                 neg_color=BLUE):

        super().__init__()

        self.height = None
        self.width = None

        self.title = title
        self.void_color = void_color
        self.pos_color = pos_color
        self.neg_color = neg_color

        self.msg_dispatcher.subscribe(OPENING, lambda: cv2.namedWindow(title))
        self.msg_dispatcher.subscribe(CLOSING, lambda: cv2.destroyWindow(title))
        self.msg_dispatcher.subscribe(BROADCASTER_JOINED, lambda: self.msg_dispatcher.notify(OPENING))

    def late_init(self, height, width, **kwargs):
        self.height = height
        self.width = width

    def process_data(self, image, **kwargs):

        if not image.shape == (self.height, self.width, 3):
            self.msg_dispatcher.notify(CLOSING)
            raise TypeError

        is_visible = cv2.getWindowProperty(self.title, cv2.WND_PROP_VISIBLE) == 1
        if not is_visible:
            self.msg_dispatcher.notify(CLOSING)
            return

        cv2.imshow(self.title, image)

        keypress = cv2.pollKey()
        if keypress != -1:
            self.msg_dispatcher.notify('keypress', key=chr(keypress))