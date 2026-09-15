from dogram.separating_view_family import frozen_specimen


def test_full_family_separates_all_items():
    s = frozen_specimen()
    assert s["full_collisions"] == ()
    assert s["signatures"] == {
        "x0": (0, 0, 0),
        "x1": (1, 0, 0),
        "x2": (1, 1, 0),
        "x3": (1, 1, 1),
    }


def test_every_declared_view_is_necessary_in_this_family():
    s = frozen_specimen()
    assert s["minimum_subfamilies"] == (("t1", "t2", "t3"),)
    assert s["omission_collisions"] == {
        "t1": (("x0", "x1"),),
        "t2": (("x1", "x2"),),
        "t3": (("x2", "x3"),),
    }
