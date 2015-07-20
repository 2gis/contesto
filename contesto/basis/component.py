from time import sleep

from contesto.utils.extending import AutoExtendingSelectors
from contesto.utils.log import trace
from contesto.utils import Enum
from contesto.exceptions import SwipeError
from contesto.basis import LoadableObject

from appium.webdriver.common.touch_action import TouchAction


class BaseComponent(LoadableObject):
    __metaclass__ = AutoExtendingSelectors

    def __init__(self, driver, element=None):
        """
        :type driver: ContestoDriver
        :type element: ContestoWebElement
        """
        self.driver = driver
        self.element = element
        trace(self.__class__)
        super(BaseComponent, self).__init__(driver)


Directions = Enum("down", "up", "left", "right")


class MobileComponent(BaseComponent):
    _swipe_offset = 25
    _swipe_duration = 1000
    _swipe_pause = 1

    @staticmethod
    def _calculate_scrolls_nums(size, direction, to_element):
        if to_element:
            width, height = size.get('width'), size.get('height')
            if direction == Directions.down or direction == Directions.up:
                element_y = to_element.location.get('y')
                return int(element_y / height)
            elif direction == Directions.left or direction == Directions.left:
                element_x = to_element.location.get('x')
                return int(element_x / width)
        else:
            return None

    def _calculate_coordinates(self, location, size, direction):
        width, height = size.get('width'), size.get('height')
        left_corner_x, left_corner_y = location.get('x'), location.get('y')
        offset = self._swipe_offset

        if direction in [Directions.down, Directions.up]:
            if 2 * offset > height:
                raise SwipeError("Element's height %s is not enough to swipe it with offset %s" % (height, offset))
        elif direction in [Directions.left, Directions.right]:
            if 2 * offset > width:
                raise SwipeError("Element's width %s is not enough to swipe it with offset %s" % (width, offset))

        d_start_x, d_start_y, d_end_x, d_end_y = 0, 0, 0, 0
        if direction == Directions.down:
            d_start_x, d_start_y, d_end_x, d_end_y = width/2, height - offset, width/2, offset
        elif direction == Directions.up:
            d_start_x, d_start_y, d_end_x, d_end_y = width/2, offset, width/2, height - offset
        elif direction == Directions.left:
            d_start_x, d_start_y, d_end_x, d_end_y = width - offset, height / 2, offset, height / 2
        elif direction == Directions.right:
            d_start_x, d_start_y, d_end_x, d_end_y = offset, height / 2, width - offset, height / 2

        start_x = left_corner_x + d_start_x
        start_y = left_corner_y + d_start_y
        end_x = left_corner_x + d_end_x
        end_y = left_corner_y + d_end_y
        return start_x, start_y, end_x, end_y

    def swipe(self, direction=Directions.down, scroll_num=1, to_element=None):
        if type(direction) is not Enum and direction not in Directions:
            raise SwipeError("Unknown direction to swipe to")

        location = self.element.location
        size = self.element.size

        scroll_num = self._calculate_scrolls_nums(size, direction, to_element) or scroll_num
        start_x, start_y, end_x, end_y = self._calculate_coordinates(location, size, direction)

        for num in xrange(scroll_num):
            action = TouchAction(self.driver)
            action \
                .press(x=start_x, y=start_y) \
                .wait(ms=self._swipe_duration) \
                .move_to(x=end_x, y=end_y) \
                .release()
            action.perform()
            sleep(self._swipe_pause)

    def swipe_down(self, scroll_num=1):
        self.swipe(direction=Directions.down, scroll_num=scroll_num)

    def swipe_up(self, scroll_num=1):
        self.swipe(direction=Directions.up, scroll_num=scroll_num)

    def swipe_left(self, scroll_num=1):
        self.swipe(direction=Directions.left, scroll_num=scroll_num)

    def swipe_right(self, scroll_num=1):
        self.swipe(direction=Directions.right, scroll_num=scroll_num)

    def swipe_to_element(self, to_element):
        self.swipe(to_element=to_element)

    def swipe_discover_locator(self, locator, max_scroll_num):
        raise NotImplementedError
