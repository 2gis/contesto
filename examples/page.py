from contesto import Page, Component, find_element, by, step, Step


class SearchResults(Component):
    _header = by.class_name("mixedResults__header")

    def header(self):
        return find_element(self.element, self._header)

    def results_count(self):
        header_text = self.header().text
        count = ''.join(x for x in header_text if x.isdigit())
        return int(count)


class SearchBar(Component):
    _search_field = by.css_selector(".searchBar__textfield._directory .suggest__input")
    _search_submit_button = by.css_selector(".searchBar__submit._directory")

    def __init__(self, driver, element):
        self.register_onload_elements([
            self._search_field,
            self._search_submit_button
        ])
        super(SearchBar, self).__init__(driver, element)

    def search_field(self):
        return find_element(self.element, self._search_field)

    def search_submit_button(self):
        return find_element(self.element, self._search_submit_button)

    @step("searching for {text}")
    def search(self, text):
        with Step("entering text %s" % text):
            self.search_field().send_keys(text)

        with Step("submitting search"):
            self.search_submit_button().click()


class CityPage(Page):
    _search_bar = by.class_name("online__searchBar")
    _search_results = by.class_name("mixedResults")

    def __init__(self, driver):
        self.register_onload_elements([self._search_bar])
        super(CityPage, self).__init__(driver)

    def search_bar(self):
        return SearchBar(self.driver, find_element(self.driver, self._search_bar))

    def search_results(self):
        return SearchResults(self.driver, find_element(self.driver, self._search_results))
