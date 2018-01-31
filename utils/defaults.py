class CurrentUserIDDefault:
    def set_context(self, serializer_field):
        self.id = serializer_field.context['request'].user.id

    def __call__(self):
        return self.id

    def __repr__(self):
        return '%s()' % self.__class__.__name__
