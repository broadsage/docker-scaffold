#!/usr/bin/env python3

# SPDX-FileCopyrightText: Copyright (c) 2025 Broadsage <opensource@broadsage.com>
#
# SPDX-License-Identifier: Apache-2.0

"""
Unit tests for config.py

Test Coverage:
  - Deep merge functionality with nested dicts
  - Feature bundle detection and activation
  - Safe default generation for disabled features
  - Configuration validation

Run with: python3 test_config.py
"""

import unittest
from typing import Any, Dict, List

from config import (
    deep_merge,
    get_feature_bundles,
    make_safe_default,
    activate_feature_bundles,
    validate_config,
)


class TestDeepMerge(unittest.TestCase):
    """Test deep merge functionality."""

    def test_simple_merge(self) -> None:
        """Test basic merge of dictionaries."""
        base = {"a": 1, "b": 2}
        override = {"b": 3, "c": 4}
        expected = {"a": 1, "b": 3, "c": 4}

        result = deep_merge(base, override)
        self.assertEqual(result, expected)

    def test_nested_merge(self) -> None:
        """Test nested dictionary merge."""
        base = {"x": {"y": 1, "z": 2}}
        override = {"x": {"y": 10}}
        expected = {"x": {"y": 10, "z": 2}}

        result = deep_merge(base, override)
        self.assertEqual(result, expected)

    def test_no_mutation(self) -> None:
        """Test that original dicts are not mutated."""
        base = {"a": {"b": 1}}
        base_copy = {"a": {"b": 1}}
        override = {"a": {"b": 2}}

        deep_merge(base, override)
        self.assertEqual(base, base_copy)


class TestFeatureBundles(unittest.TestCase):
    """Test feature bundle detection."""

    def test_detect_bundles(self) -> None:
        """Test automatic detection of feature bundles."""
        defaults: Dict[str, Any] = {
            "organization": "test",
            "build": {"platforms": []},
            "image": {"name": "test"},
            "github": {"workflows": True},
            "security": {"scan": True},
        }

        bundles: List[str] = get_feature_bundles(defaults)
        self.assertIn("github", bundles)
        self.assertIn("security", bundles)
        self.assertNotIn("organization", bundles)
        self.assertNotIn("build", bundles)


class TestMakeSafeDefault(unittest.TestCase):
    """Test safe default conversion."""

    def test_bool_conversion(self) -> None:
        """Test boolean values become False."""
        self.assertFalse(make_safe_default(True))
        self.assertFalse(make_safe_default(False))

    def test_list_conversion(self) -> None:
        """Test lists become empty lists."""
        self.assertEqual(make_safe_default([1, 2, 3]), [])

    def test_dict_conversion(self) -> None:
        """Test dicts are recursively converted."""
        result = make_safe_default({"a": True, "b": [1, 2]})
        self.assertEqual(result, {"a": False, "b": []})


class TestFeatureActivation(unittest.TestCase):
    """Test feature bundle activation."""

    def test_enable_feature(self) -> None:
        """Test enabling a feature bundle."""
        defaults = {"github": {"workflows": True, "issues": True}}
        project = {"features": {"github": True}}

        result = activate_feature_bundles(defaults, project)

        self.assertIn("github", result)
        self.assertEqual(result["github"]["workflows"], True)
        self.assertEqual(result["github"]["issues"], True)

    def test_disable_feature(self) -> None:
        """Test disabling a feature bundle."""
        defaults = {"github": {"workflows": True, "issues": True}}
        project = {"features": {"github": False}}

        result = activate_feature_bundles(defaults, project)

        self.assertIn("github", result)
        self.assertFalse(result["github"]["workflows"])
        self.assertFalse(result["github"]["issues"])

    def test_override_enabled_feature(self) -> None:
        """Test overriding specific settings in an enabled feature."""
        defaults = {"github": {"workflows": True, "issues": True}}
        project = {
            "features": {"github": True},
            "github": {"issues": False},
        }

        result = activate_feature_bundles(defaults, project)

        self.assertEqual(result["github"]["workflows"], True)
        self.assertEqual(result["github"]["issues"], False)


class TestValidation(unittest.TestCase):
    """Test configuration validation."""

    def test_valid_config(self) -> None:
        """Test that valid config has no errors."""
        config: Dict[str, Any] = {
            "image": {"name": "myapp"},
            "build": {"platforms": ["linux/amd64"]},
        }

        errors = validate_config(config)
        self.assertEqual(errors, [])

    def test_missing_image_section(self) -> None:
        """Test that missing image section is allowed (optional)."""
        config: Dict[str, Any] = {
            "build": {"platforms": ["linux/amd64"]},
        }

        errors = validate_config(config)
        # Image section is optional - no error expected
        self.assertEqual(errors, [])

    def test_empty_image_name(self) -> None:
        """Test that empty image name is caught if image section exists."""
        config: Dict[str, Any] = {
            "image": {"name": ""},
            "build": {"platforms": ["linux/amd64"]},
        }

        errors = validate_config(config)
        self.assertTrue(any("image" in e for e in errors))

    def test_empty_platforms_list(self) -> None:
        """Test that empty platforms list is caught."""
        config: Dict[str, Any] = {
            "image": {"name": "myapp"},
            "build": {"platforms": []},
        }

        errors = validate_config(config)
        self.assertTrue(any("platforms" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
