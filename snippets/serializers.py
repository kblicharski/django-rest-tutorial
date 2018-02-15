from rest_framework import serializers

from .models import LANGUAGE_CHOICES, STYLE_CHOICES, Snippet


class SnippetSerializer(serializers.Serializer):
    """A serializer responsible for serializing and deserializing `Snippet` objects.

    Serializers are how we turn native Python objects into popular data representations
    for the web, like json or xml. The first part declares the fields that are to be
    serialized and deserialized, while the `create()` and `update()` methods define
    how instances are created or modified whenever we call `serializer.save()`.

    The syntax of declaring serializers mirrors the syntax of Django's forms very
    closely, containing similar validation flags. Some flags can control how the
    serializer is displayed in different contexts, like when rendering HTML.
    The `{'base_template': 'textarea.html'}` flag is equivalent to
    `widget=widgets.TextArea` on a Django `Form` class.

    "Under the hood", this is what serializers are actually doing:

    Serialization:
        >>> from snippets.models import Snippet
        >>> from snippets.serializers import SnippetSerializer
        >>> from rest_framework.renderers import JSONRenderer
        >>> from rest_framework.parsers import JSONParser
        >>> snippet = Snippet(code='print("Hello World!")')
        >>> snippet.save()
        >>> serializer = SnippetSerializer(snippet)
        >>> serializer.data  # We translate the model into Python native datatypes
        {'id': 2, 'title': '', 'code': 'print "hello, world"\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
        >>> content = JSONRenderer().render(serializer.data)  # Then render it as json
        >>> content
        b'{"id":2,"title":"","code":"print \\"hello, world\\"\\n","linenos":false,"language":"python","style":"friendly"}'

    Deserialization:
        >>> from django.utils.six import BytesIO
        >>> stream = BytesIO(content)
        >>> data = JSONParser().parse(stream)  # Parse the stream into Python datatypes
        >>> data
        {'id': 4, 'title': '', 'code': 'print "hello, world"\n', 'linenos': False, 'language': 'python', 'style': 'friendly'}
        >>> serializer = SnippetSerializer(data=data)  # Restore datatypes as objects
        >>> serializer.is_valid()
        True
        >>> serializer.validated_data
        OrderedDict([('title', ''), ('code', 'print "hello, world"'), ('linenos', False), ('language', 'python'), ('style', 'friendly')])
        >>> serializer.save()
        <Snippet: Snippet object>

    Serializing querysets is the same as serializing individual objects, but you
    must pass the `many=True` flag into the serializer.

    Serializing Querysets:
        >>> serializer = SnippetSerializer(Snippet.objects.all(), many=True)
        >>> serializer.data

    """

    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(required=False, allow_blank=True, max_length=100)
    code = serializers.CharField(style={'base_template': 'textarea.html'})
    linenos = serializers.BooleanField(required=False)
    language = serializers.ChoiceField(choices=LANGUAGE_CHOICES, default='python')
    style = serializers.ChoiceField(choices=STYLE_CHOICES, default='friendly')

    def create(self, validated_data: dict) -> Snippet:
        """Create and return a new `Snippet` instance, given the validated data.

        Args:
            validated_data: A dict of the validated attributes of a `Snippet` instance.

        Returns:
            A constructed `Snippet` instance.

        """
        return Snippet.objects.create(**validated_data)

    def update(self, instance: Snippet, validated_data: dict) -> Snippet:
        """Update and return an existing `Snippet` instance, given the validated data.

        Args:
            instance: The `Snippet` instance we are updating.
            validated_data: A dict of the validated attributes of a `Snippet` instance.

        """
        instance.title = validated_data.get('title', default=instance.title)
        instance.code = validated_data.get('code', default=instance.code)
        instance.language = validated_data.get('language', default=instance.language)
        instance.style = validated_data.get('style', default=instance.style)
        instance.save()
        return instance


class SnippetModelSerializer(serializers.ModelSerializer):
    """A more concise, but functionally equivalent, `SnippetSerializer`.

    In the above example, there is a lot of duplicated information
    from the `Snippet` model itself. Because serializers are paired with
    models extremely often, the `ModelSerializer` was created. This is analogous
    to Django providing both a `Form` and a `ModelForm` class.

    `ModelSerializers` aren't magic -- they just automatically determine a
    set of fields and provide simple default implementations for `create()`
    and `update()`.

    Additionally, you can inspect all of the fields in a serializer (whether its
    a `ModelSerializer` or a regular `Serializer) by calling `repr()` on it.

    Examples:
        >>> from snippets.serializers import SnippetSerializer
        >>> serializer = SnippetSerializer()
        >>> print(repr(serializer))
        # SnippetSerializer():
        #    id = IntegerField(label='ID', read_only=True)
        #    title = CharField(allow_blank=True, max_length=100, required=False)
        #    code = CharField(style={'base_template': 'textarea.html'})
        #    linenos = BooleanField(required=False)
        #    language = ChoiceField(choices=[('Clipper', 'FoxPro'), ...
        #    style = ChoiceField(choices=[('autumn', 'autumn'), ...

    """

    class Meta:
        model = Snippet
        fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
