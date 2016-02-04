try:
    from mock import Mock
except ImportError:
    from unittest.mock import Mock
from contesto.basis.component import BaseComponent
import unittest


class TestComponent(BaseComponent):
    def __init__(self, test, element):
        super(TestComponent, self).__init__(test, element)
        self.test = self.driver


class PageTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = Mock()
        self.element = Mock()

    def test_component_without_element(self):
        component = BaseComponent(self.driver)
        self.assertEqual(component.element, None)

    def test_component_with_element(self):
        component = BaseComponent(self.driver, self.element)
        self.assertEqual(component.element, self.element)

    def test_extend_component(self):
        component = TestComponent(self.driver, self.element)
        self.assertEqual(component.element, self.element)
        self.assertEqual(component.test, self.driver)
