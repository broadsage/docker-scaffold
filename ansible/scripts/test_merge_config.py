#!/usr/bin/env python3
"""
Unit tests for merge_config.py

Run with: python3 test_merge_config.py
"""

import sys
import unittest
from typing import Any, Dict

try:
    import yaml as _  # noqa: F401  # Required for PyYAML dependency check
except ImportError:
    print("❌ Error: PyYAML is not installed")
    print("   Install with: pip install pyyaml")
    sys.exit(1)

from merge_config import deep_merge, activate_feature_bundles, validate_config


class TestDeepMerge(unittest.TestCase):
    """Test deep merge functionality."""

    def test_simple_merge(self) -> None:
        base: Dict[str, int] = {'a': 1, 'b': 2}
        override: Dict[str, int] = {'b': 3, 'c': 4}
        result: Dict[str, Any] = deep_merge(base, override)  # type: ignore

        self.assertEqual(result['a'], 1)
        self.assertEqual(result['b'], 3)  # Override wins
        self.assertEqual(result['c'], 4)

    def test_nested_merge(self) -> None:
        base: Dict[str, Dict[str, bool]] = {
            'github': {
                'workflows': True,
                'issues': True
            }
        }
        override: Dict[str, Dict[str, bool]] = {
            'github': {
                'issues': False
            }
        }
        result: Dict[str, Any] = deep_merge(base, override)  # type: ignore

        self.assertEqual(result['github']['workflows'], True)  # Preserved
        self.assertEqual(result['github']['issues'], False)    # Overridden

    def test_deep_nested_merge(self) -> None:
        base: Dict[str, Any] = {
            'github': {
                'projects': {
                    'enabled': False,
                    'number': 1
                }
            }
        }
        override: Dict[str, Any] = {
            'github': {
                'projects': {
                    'enabled': True
                }
            }
        }
        result: Dict[str, Any] = deep_merge(base, override)  # type: ignore

        self.assertEqual(result['github']['projects']['enabled'], True)
        self.assertEqual(result['github']['projects']['number'], 1)


class TestFeatureActivation(unittest.TestCase):
    """Test feature bundle activation."""

    def test_github_feature_activation(self) -> None:
        defaults: Dict[str, Any] = {
            'github': {
                'workflows': True,
                'issues': True
            }
        }
        project: Dict[str, Any] = {
            'features': {
                'github': True
            }
        }

        result: Dict[str, Any] = activate_feature_bundles(defaults, project)  # type: ignore

        self.assertIn('github', result)
        self.assertEqual(result['github']['workflows'], True)
        self.assertEqual(result['github']['issues'], True)

    def test_github_feature_disabled(self) -> None:
        defaults: Dict[str, Any] = {
            'github': {
                'workflows': True,
                'issues': True
            }
        }
        project: Dict[str, Any] = {
            'features': {
                'github': False
            }
        }

        result: Dict[str, Any] = activate_feature_bundles(defaults, project)  # type: ignore

        self.assertNotIn('github', result)

    def test_feature_with_override(self) -> None:
        defaults: Dict[str, Any] = {
            'github': {
                'workflows': True,
                'issues': True,
                'projects': {
                    'enabled': False,
                    'number': 1
                }
            }
        }
        project: Dict[str, Any] = {
            'features': {
                'github': True
            },
            'github': {
                'issues': False,
                'projects': {
                    'enabled': True,
                    'number': 6
                }
            }
        }

        result: Dict[str, Any] = activate_feature_bundles(defaults, project)  # type: ignore

        # From defaults
        self.assertEqual(result['github']['workflows'], True)
        # Overridden
        self.assertEqual(result['github']['issues'], False)
        self.assertEqual(result['github']['projects']['enabled'], True)
        self.assertEqual(result['github']['projects']['number'], 6)

    def test_multiple_features(self) -> None:
        defaults: Dict[str, Any] = {
            'github': {'workflows': True},
            'security': {'scan': {'enabled': True}}
        }
        project: Dict[str, Any] = {
            'features': {
                'github': True,
                'security': True
            }
        }

        result: Dict[str, Any] = activate_feature_bundles(defaults, project)  # type: ignore

        self.assertIn('github', result)
        self.assertIn('security', result)

    def test_core_sections_always_included(self) -> None:
        defaults: Dict[str, Any] = {
            'organization': 'broadsage',
            'metadata': {'license': 'Apache-2.0'}
        }
        project: Dict[str, Any] = {
            'image': {'name': 'test', 'description': 'Test'}
        }

        result: Dict[str, Any] = activate_feature_bundles(defaults, project)  # type: ignore

        self.assertEqual(result['organization'], 'broadsage')
        self.assertEqual(result['metadata']['license'], 'Apache-2.0')
        self.assertEqual(result['image']['name'], 'test')


class TestValidation(unittest.TestCase):
    """Test configuration validation."""

    def test_valid_config(self) -> None:
        config: Dict[str, Any] = {
            'image': {
                'name': 'test-image',
                'description': 'Test description'
            }
        }

        errors = validate_config(config)  # type: ignore
        self.assertEqual(len(errors), 0)

    def test_missing_name(self) -> None:
        config: Dict[str, Any] = {
            'image': {
                'description': 'Test description'
            }
        }

        errors = validate_config(config)  # type: ignore
        self.assertTrue(any('name' in err.lower() for err in errors))

    def test_missing_description(self) -> None:
        config: Dict[str, Any] = {
            'image': {
                'name': 'test-image'
            }
        }

        errors = validate_config(config)  # type: ignore
        self.assertTrue(any('description' in err.lower() for err in errors))

    def test_empty_name(self) -> None:
        config: Dict[str, Any] = {
            'image': {
                'name': '',
                'description': 'Test description'
            }
        }

        errors = validate_config(config)  # type: ignore
        self.assertTrue(any('empty' in err.lower() for err in errors))

    def test_invalid_platform(self) -> None:
        config: Dict[str, Any] = {
            'image': {
                'name': 'test-image',
                'description': 'Test description'
            },
            'build': {
                'platforms': ['linux/invalid']
            }
        }

        errors = validate_config(config)  # type: ignore
        self.assertTrue(any('invalid' in err.lower() for err in errors))

    def test_valid_platforms(self) -> None:
        config: Dict[str, Any] = {
            'image': {
                'name': 'test-image',
                'description': 'Test description'
            },
            'build': {
                'platforms': ['linux/amd64', 'linux/arm64']
            }
        }

        errors = validate_config(config)  # type: ignore
        # Should only have platform-unrelated errors if any
        self.assertFalse(any('platform' in err.lower() for err in errors))


if __name__ == '__main__':
    print("Running merge_config.py unit tests...")
    print("=" * 70)
    unittest.main(verbosity=2)
