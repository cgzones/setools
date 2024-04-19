# Derived from tests/portconquery.py
#
# SPDX-License-Identifier: GPL-2.0-only
#
import pytest
import setools


@pytest.mark.obj_args("tests/library/pirqconquery.conf", xen=True)
class TestPirqconQuery:

    def test_unset(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with no criteria"""
        # query with no parameters gets all PCI irqs.
        rules = sorted(compiled_policy.pirqcons())

        q = setools.PirqconQuery(compiled_policy)
        q_rules = sorted(q.results())

        assert rules == q_rules

    def test_user_exact(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context user exact match"""
        q = setools.PirqconQuery(compiled_policy, user="user10", user_regex=False)

        irq = sorted(p.irq for p in q.results())
        assert [(10)] == irq

    def test_user_regex(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context user regex match"""
        q = setools.PirqconQuery(compiled_policy, user="user11(a|b)", user_regex=True)

        irq = sorted(p.irq for p in q.results())
        assert [(11), (11000)] == irq

    def test_role_exact(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context role exact match"""
        q = setools.PirqconQuery(compiled_policy, role="role20_r", role_regex=False)

        irq = sorted(p.irq for p in q.results())
        assert [(20)] == irq

    def test_role_regex(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context role regex match"""
        q = setools.PirqconQuery(compiled_policy, role="role21(a|c)_r", role_regex=True)

        irq = sorted(p.irq for p in q.results())
        assert [(21), (21001)] == irq

    def test_type_exact(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context type exact match"""
        q = setools.PirqconQuery(compiled_policy, type_="type30", type_regex=False)

        irq = sorted(p.irq for p in q.results())
        assert [(30)] == irq

    def test_type_regex(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context type regex match"""
        q = setools.PirqconQuery(compiled_policy, type_="type31(b|c)", type_regex=True)

        irq = sorted(p.irq for p in q.results())
        assert [(31000), (31001)] == irq

    def test_range_exact(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range exact match"""
        q = setools.PirqconQuery(compiled_policy, range_="s0:c1 - s0:c0.c4")

        irq = sorted(p.irq for p in q.results())
        assert [(40)] == irq

    def test_range_overlap1(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range overlap match (equal)"""
        q = setools.PirqconQuery(compiled_policy, range_="s1:c1 - s1:c0.c4", range_overlap=True)

        irq = sorted(p.irq for p in q.results())
        assert [(41)] == irq

    def test_range_overlap2(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range overlap match (subset)"""
        q = setools.PirqconQuery(compiled_policy, range_="s1:c1,c2 - s1:c0.c3", range_overlap=True)

        irq = sorted(p.irq for p in q.results())
        assert [(41)] == irq

    def test_range_overlap3(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range overlap match (superset)"""
        q = setools.PirqconQuery(compiled_policy, range_="s1 - s1:c0.c4", range_overlap=True)

        irq = sorted(p.irq for p in q.results())
        assert [(41)] == irq

    def test_range_overlap4(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range overlap match (overlap low level)"""
        q = setools.PirqconQuery(compiled_policy, range_="s1 - s1:c1,c2", range_overlap=True)

        irq = sorted(p.irq for p in q.results())
        assert [(41)] == irq

    def test_range_overlap5(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range overlap match (overlap high level)"""
        q = setools.PirqconQuery(compiled_policy, range_="s1:c1,c2 - s1:c0.c4", range_overlap=True)

        irq = sorted(p.irq for p in q.results())
        assert [(41)] == irq

    def test_range_subset1(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range subset match"""
        q = setools.PirqconQuery(compiled_policy, range_="s2:c1,c2 - s2:c0.c3", range_overlap=True)

        irq = sorted(p.irq for p in q.results())
        assert [(42)] == irq

    def test_range_subset2(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range subset match (equal)"""
        q = setools.PirqconQuery(compiled_policy, range_="s2:c1 - s2:c1.c3", range_overlap=True)

        irq = sorted(p.irq for p in q.results())
        assert [(42)] == irq

    def test_range_superset1(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range superset match"""
        q = setools.PirqconQuery(compiled_policy, range_="s3 - s3:c0.c4", range_superset=True)

        irq = sorted(p.irq for p in q.results())
        assert [(43)] == irq

    def test_range_superset2(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range superset match (equal)"""
        q = setools.PirqconQuery(compiled_policy, range_="s3:c1 - s3:c1.c3", range_superset=True)

        irq = sorted(p.irq for p in q.results())
        assert [(43)] == irq

    def test_range_proper_subset1(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range proper subset match"""
        q = setools.PirqconQuery(compiled_policy, range_="s4:c1,c2", range_subset=True,
                                 range_proper=True)

        irq = sorted(p.irq for p in q.results())
        assert [(44)] == irq

    def test_range_proper_subset2(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range proper subset match (equal)"""
        q = setools.PirqconQuery(compiled_policy, range_="s4:c1 - s4:c1.c3", range_subset=True,
                                 range_proper=True)

        irq = sorted(p.irq for p in q.results())
        assert [] == irq

    def test_range_proper_subset3(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range proper subset match (equal low only)"""
        q = setools.PirqconQuery(compiled_policy, range_="s4:c1 - s4:c1.c2", range_subset=True,
                                 range_proper=True)

        irq = sorted(p.irq for p in q.results())
        assert [(44)] == irq

    def test_range_proper_subset4(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range proper subset match (equal high only)"""
        q = setools.PirqconQuery(compiled_policy, range_="s4:c1,c2 - s4:c1.c3", range_subset=True,
                                 range_proper=True)

        irq = sorted(p.irq for p in q.results())
        assert [(44)] == irq

    def test_range_proper_superset1(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range proper superset match"""
        q = setools.PirqconQuery(compiled_policy, range_="s5 - s5:c0.c4", range_superset=True,
                                 range_proper=True)

        irq = sorted(p.irq for p in q.results())
        assert [(45)] == irq

    def test_range_proper_superset2(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range proper superset match (equal)"""
        q = setools.PirqconQuery(compiled_policy, range_="s5:c1 - s5:c1.c3", range_superset=True,
                                 range_proper=True)

        irq = sorted(p.irq for p in q.results())
        assert [] == irq

    def test_range_proper_superset3(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range proper superset match (equal low)"""
        q = setools.PirqconQuery(compiled_policy, range_="s5:c1 - s5:c1.c4", range_superset=True,
                                 range_proper=True)

        irq = sorted(p.irq for p in q.results())
        assert [(45)] == irq

    def test_range_proper_superset4(self, compiled_policy: setools.SELinuxPolicy) -> None:
        """Pirqcon query with context range proper superset match (equal high)"""
        q = setools.PirqconQuery(compiled_policy, range_="s5 - s5:c1.c3", range_superset=True,
                                 range_proper=True)

        irq = sorted(p.irq for p in q.results())
        assert [(45)] == irq
