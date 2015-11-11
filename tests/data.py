import unittest

import sqlalchemy as sqla

from anodyne import data

TestTable = sqla.Table(
  'test_table', sqla.MetaData(),
  sqla.Column('foo', sqla.Integer)
)


class DataTransferTest(unittest.TestCase):

  def test_basic(self):
    """
    Test that basic DataClass instantiation works.
    The class should be read-only and throw value errors for values that aren't
    in a dict-like.
    """
    # create a basic data object.
    basic_data = data.DataClass(TestTable, name='test_table_basic')

    # test that it requires a dict-like to instantiate.
    self.assertRaises(
      ValueError,
      basic_data,
      {'foo'}
    )

    # test instance is read-only.
    instance = basic_data({'foo': 'bar'})
    self.assertRaises(
      AttributeError,
      instance.__setattr__,
      'foo',
      'bar'
    )

    self.assertTrue(hasattr(instance, 'foo'))
    self.assertEqual('bar', instance.foo)

  def test_extras(self):
    """
    Test that DataClass with "extras" directive allows values that weren't
    explicitly defined on the sqlalchemy table.
    """
    # create with non-defaulted extras
    extras_data = data.DataClass(
      TestTable,
      name='test_table_extras',
      extras=['bar']
    )
    # test instance is read-only.
    instance = extras_data({'foo': 'bar'})
    self.assertTrue(hasattr(instance, 'bar'))
    self.assertIsNone(instance.bar)

    # now instantiate with the extra.
    instance = extras_data({
      'foo': 'bar',
      'bar': 'baz'
    })

    self.assertTrue(hasattr(instance, 'bar'))
    self.assertEqual('baz', instance.bar)

    # test it with keyword extras
    instance = extras_data({'foo': 'bar'}, bar='fizz')

    self.assertTrue(hasattr(instance, 'bar'))
    self.assertEqual('fizz', instance.bar)

  def test_extras_with_defaults(self):
    """Tests that extras can be used with default values."""
    # create with non-defaulted extras
    extras_data = data.DataClass(
      TestTable,
      name='test_table_extras_defaults',
      extras={'bar': 'baz'}
    )
    # test instance is read-only.
    instance = extras_data({'foo': 'bar'})
    self.assertTrue(hasattr(instance, 'bar'))
    self.assertEqual('baz', instance.bar)

    # now instantiate with the extra.
    instance = extras_data({
      'foo': 'bar',
      'bar': 'fizz'
    })

    self.assertTrue(hasattr(instance, 'bar'))
    self.assertEqual('fizz', instance.bar)

  def test_cached(self):
    """Test that already created class objects are cached."""
    # create a basic data object.
    cached0 = data.DataClass(TestTable, name='test_table_cached')
    cached1 = data.DataClass(TestTable, name='test_table_cached')
    # test it's the same thing.
    self.assertIs(cached0, cached1)
