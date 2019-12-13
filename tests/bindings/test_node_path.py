import pytest

from godot import Vector3, NodePath


class TestNodePath:
    def test_equal(self):
        v1 = NodePath("parent/child")
        v2 = NodePath("parent/child")
        assert v1 == v2
        other = NodePath("parent/other_child")
        assert not v1 == other  # Force use of __eq__

    @pytest.mark.parametrize(
        "arg", [None, 0, "parent/child", NodePath("parent/other_child")]
    )
    def test_bad_equal(self, arg):
        basis = NodePath("parent/child")
        assert basis != arg

    def test_repr(self):
        v = NodePath("/root/leaf")
        assert repr(v) == "<NodePath(/root/leaf)>"

    @pytest.mark.parametrize("args", [(), (42,), (None,)])
    def test_bad_build(self, args):
        with pytest.raises(TypeError):
            NodePath(*args)

    @pytest.mark.parametrize(
        "field,ret_type,params",
        [
            ["get_name", str, (0,)],
            ["get_name_count", int, ()],
            ["get_concatenated_subnames", str, ()],
            ["get_subname", str, (0,)],
            ["get_subname_count", int, ()],
            ["is_absolute", bool, ()],
            ["is_empty", bool, ()],
        ],
        ids=lambda x: x[0],
    )
    def test_methods(self, field, ret_type, params):
        v = NodePath("/foo")
        # Don't test methods' validity but bindings one
        assert hasattr(v, field)
        method = getattr(v, field)
        assert callable(method)
        ret = method(*params)
        assert isinstance(ret, ret_type)

    def test_as_binding_return_value(self, current_node):
        ret = current_node.get_path()
        assert isinstance(ret, NodePath)

        ret2 = current_node.get_path()
        assert ret == ret2

        assert str(ret) == "/root/main"

    def test_as_binding_param(self, current_node):
        root = current_node.get_parent()
        path = current_node.get_path()
        dummy_path = NodePath("/foo/bar")

        assert root.has_node(path) is True
        assert root.has_node(dummy_path) is False
