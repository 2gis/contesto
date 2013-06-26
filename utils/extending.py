class AutoExtendingSelectors(type):
    def __new__(cls, name, bases, attrs):
        selectors = {}
        for base in bases:
            try:
                selectors.update(getattr(base, 'selectors'))
            except AttributeError:
                pass
        try:
            selectors.update(attrs.pop('selectors'))
        except KeyError:
            pass
        attrs['selectors'] = selectors
        return type.__new__(cls, name, bases, attrs)
