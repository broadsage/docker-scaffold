#!/usr/bin/env python3
"""
Pre-generation hook for cookiecutter template.
Validates inputs before project generation.
"""

import re
import sys


def validate_project_name(name: str) -> bool:
    """
    Validate project name format.
    
    Args:
        name: Project name to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If name format is invalid
    """
    if not name:
        raise ValueError("Project name cannot be empty")
    
    if not re.match(r'^[a-zA-Z0-9][a-zA-Z0-9-_]*$', name):
        raise ValueError(
            "Project name must start with alphanumeric character and "
            "contain only alphanumeric characters, hyphens, or underscores"
        )
    
    if len(name) > 100:
        raise ValueError("Project name must be less than 100 characters")
    
    return True


def validate_email(email: str) -> bool:
    """
    Validate email format.
    
    Args:
        email: Email address to validate
        
    Returns:
        bool: True if valid
        
    Raises:
        ValueError: If email format is invalid
    """
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(email_pattern, email):
        raise ValueError(f"Invalid email format: {email}")
    return True


def main() -> None:
    """Run pre-generation validations."""
    # Get cookiecutter variables
    project_name = "{{ cookiecutter.project_name }}"
    maintainer_email = "{{ cookiecutter.maintainer_email }}"
    organization = "{{ cookiecutter.organization }}"
    
    try:
        # Validate inputs
        validate_project_name(project_name)
        validate_email(maintainer_email)
        
        # Display info
        print("\n" + "="*60)
        print("✅ Pre-generation validation successful!")
        print("="*60)
        print(f"  Project:     {project_name}")
        print(f"  Email:       {maintainer_email}")
        print(f"  Organization: {organization or 'Not specified'}")
        print("="*60 + "\n")
        
    except ValueError as e:
        print(f"\n❌ ERROR: {e}\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}\n", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
