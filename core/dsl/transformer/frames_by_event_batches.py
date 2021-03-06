import numpy as np

from core.constants.colors import BLACK, WHITE, BLUE
from core.dsl.transformer.module import Transformer


class EventBatchToFrames(Transformer):

    def __init__(self,
                 void_color=BLACK,
                 pos_color=WHITE,
                 neg_color=BLUE):

        super().__init__()

        self.frame_buffer = None

        self.void_color = void_color
        self.pos_color = pos_color
        self.neg_color = neg_color

    def late_init(self, height, width, **kwargs):
        self.frame_buffer = np.zeros((height, width, 3), dtype=np.ubyte)

    def process_data(self, events, **kwargs):

        # Partition event indicis based on polarity.
        ones = np.argwhere(events['p'] == 1)
        zeroes = np.argwhere(events['p'] == 0)

        # Setting screen color based on polarity with the computed indicis.
        self.frame_buffer[events['y'][ones], events['x'][ones]] = self.pos_color
        self.frame_buffer[events['y'][zeroes], events['x'][zeroes]] = self.neg_color

        # Transferring frame.
        self.callback(self.frame_buffer, **kwargs)

        # Clearing frame-buffer.
        self.frame_buffer[:, :] = self.void_color
