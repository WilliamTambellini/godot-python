{% from 'property.tmpl.pyx' import render_property -%}
{% from 'method.tmpl.pyx' import render_method -%}

{% macro render_class(cls) -%}

{%- if not cls["singleton"] %}
cdef godot_class_constructor __{{ cls["name"] }}_constructor = godot_get_class_constructor("{{ cls['name'] }}")
{% endif -%}

cdef class {{ cls["name"] }}({{ cls["base_class"] }}):
{%- if not cls["base_class"] %}
    cdef godot_object *_ptr
    cdef bint _ptr_owner

    def __dealloc__(self):
        # De-allocate if not null and flag is set
        if self._ptr is not NULL and self._ptr_owner is True:
            godot_object_destroy(self._ptr)
            self._ptr = NULL
{%- endif %}

    def __init__(self):
{%- if cls["singleton"] %}
        raise RuntimeError(f"{type(self)} is a singleton, cannot initialize it.")
{%- else %}
        self._ptr = __{{ cls["name"] }}_constructor()
        if self._ptr is NULL:
            raise MemoryError
        self._ptr_owner = True
{%- endif %}

    @staticmethod
    cdef {{ cls["name"] }} from_ptr(godot_object *_ptr, bint owner=False):
        # Call to __new__ bypasses __init__ constructor
        cdef {{ cls["name"] }} wrapper = {{ cls["name"] }}.__new__()
        wrapper._ptr = _ptr
        wrapper._ptr_owner = owner
        return wrapper

    # Constants
{% for key, value in cls["constants"].items() %}
    {{key}} = {{value}}
{%- endfor %}

    # Methods
{# TODO: Use typing for params&return #}
{% for method in cls["methods"] %}
{{ render_method(method) | indent(first=True, width=4) }}
{% endfor %}
    # Properties
{% for prop in cls["properties"] %}
{{ render_property(prop) | indent(first=True, width=4) }}
{% endfor %}

{%- endmacro -%}