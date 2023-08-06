#
# Copyright (c) nexB Inc. and others. All rights reserved.
# SPDX-License-Identifier: Apache-2.0 AND MIT
# See http://www.apache.org/licenses/LICENSE-2.0 for the license text.
# See https://github.com/nexB/debian-inspector for support or download.
# See https://aboutcode.org for more information about nexB OSS projects.
# Copyright (c) 2018 Peter Odding
# Author: Peter Odding <peter@peterodding.com>
# URL: https://github.com/xolox/python-deb-pkg-tools


import re
import unittest

from debian_inspector import deps


class DepsTestCase(unittest.TestCase):

    def test_relationship_parsing(self):
        relationship_set = deps.parse_depends('foo, bar (>= 1) | baz')
        expected = deps.AndRelationships(relationships=(
            deps.Relationship(name='foo'),
            deps.OrRelationships(relationships=(
                deps.VersionedRelationship(name='bar', operator='>=', version='1'),
                deps.Relationship(name='baz')))))
        assert relationship_set == expected

    def test_relationship_parsing_single_relationship(self):
        expected = deps.AndRelationships(relationships=(
            deps.VersionedRelationship(name='foo', operator='=', version='1.0'),))
        assert deps.parse_depends('foo (=1.0)') == expected

    def test_relationship_parsing_raise_valueerror_for_invalid_relationship(self):
        self.assertRaises(ValueError, deps.parse_depends, 'foo (bar) (baz)')
        self.assertRaises(ValueError, deps.parse_depends, 'foo (bar baz qux)')

    def test_parse_depends(self):
        depends = deps.parse_depends('python (>= 2.6), python (<< 3)')
        expected = deps.AndRelationships(relationships=(
            deps.VersionedRelationship(name='python', operator='>=', version='2.6'),
            deps.VersionedRelationship(name='python', operator='<<', version='3'))
        )
        assert depends == expected
        assert not depends.matches('python', '2.5')
        assert depends.matches('python', '2.6')
        assert depends.matches('python', '2.7')

    def test_parse_alternatives_with_no_alternative(self):
        depends = deps.parse_alternatives('python2.6')
        expected = deps.Relationship(name='python2.6')
        assert depends == expected

    def test_parse_alternatives(self):
        depends = deps.parse_alternatives('python2.6 | python2.7')
        expected = deps.OrRelationships(relationships=(
            deps.Relationship(name='python2.6'),
            deps.Relationship(name='python2.7'))
        )
        assert depends == expected

    def test_architecture_restriction_parsing(self):
        relationship_set = deps.parse_depends('qux [i386 amd64]')
        assert 'qux' == relationship_set.relationships[0].name
        assert 2 == len(relationship_set.relationships[0].architectures)
        assert 'i386' in relationship_set.relationships[0].architectures
        assert 'amd64' in relationship_set.relationships[0].architectures

    def test_relationships_objects_as_strings(self):

        def strip(text):
            return re.sub(r'\s+', '', text)

        relationship_set = deps.parse_depends('foo, bar(>=1)|baz[i386]')
        expected = 'foo, bar (>= 1) | baz [i386]'
        assert str(relationship_set) == expected

        expected = deps.AndRelationships(relationships=(
            deps.Relationship(name='foo'),
            deps.OrRelationships(relationships=(
                deps.VersionedRelationship(name='bar', operator='>=', version='1'),
                deps.Relationship(name='baz', architectures=('i386',))))))
        assert relationship_set == expected

    def test_relationship_evaluation_works_without_version(self):
        relationship_set = deps.parse_depends('python')
        assert relationship_set.matches('python')
        assert not relationship_set.matches('python2.7')
        assert ['python'] == list(relationship_set.names)

    def test_relationship_evaluation_alternative_OR_works_without_version(self):
        relationship_set = deps.parse_depends('python2.6 | python2.7')
        assert not relationship_set.matches('python2.5')
        assert relationship_set.matches('python2.6')
        assert relationship_set.matches('python2.7')
        assert not relationship_set.matches('python3.0')
        assert ['python2.6', 'python2.7'] == sorted(relationship_set.names)

    def test_relationship_evaluation_works_without_version_against_versioned(self):
        # Testing for matches without providing a version is valid (should not
        # raise an error) but will never match a relationship with a version.
        relationship_set = deps.parse_depends('python (>= 2.6), python (<< 3)')
        assert relationship_set.matches('python', '2.7')
        assert not relationship_set.matches('python')
        assert ['python'] == list(relationship_set.names)

    def test_relationship_evaluation_combination_AND_works_with_version(self):
        # Distinguishing between packages whose name was matched but whose
        # version didn't match vs packages whose name wasn't matched.
        relationship_set = deps.parse_depends('python (>= 2.6), python (<< 3) | python (>= 3.4)')
        # name matched, version didn't
        assert relationship_set.matches('python', '2.5') is False
        # name didn't match
        assert relationship_set.matches('python2.6') is None
        # name in alternative matched, version didn't
        assert relationship_set.matches('python', '3.0') is False

        # name and version match
        assert relationship_set.matches('python', '2.7') is True
        assert relationship_set.matches('python', '2.6')
        assert relationship_set.matches('python', '3.4')
        assert ['python'] == list(relationship_set.names)

    def test_parse_depends_misc(self):
        dependencies = deps.parse_depends('python (>= 2.6), python (<< 3) | python (>= 3.4)')
        expected = deps.AndRelationships(relationships=(
            deps.VersionedRelationship(name='python', operator='>=', version='2.6'),
            deps.OrRelationships(relationships=(
                deps.VersionedRelationship(name='python', operator='<<', version='3'),
                deps.VersionedRelationship(name='python', operator='>=', version='3.4')
            ,))
        ,))
        assert dependencies == expected

        expected = 'python (>= 2.6), python (<< 3) | python (>= 3.4)'
        assert str(dependencies) == expected

    def test_parse_relationship(self):
        rel = deps.parse_relationship('python')
        assert rel == deps.Relationship(name='python')
        rel = deps.parse_relationship('python (<< 3)')
        assert rel == deps.VersionedRelationship(name='python', operator='<<', version='3')
