"""
mode_template.py
Utility for generating new SSRF Command Console mode modules.

Creates a new file in modes/ with:
- MODE_NAME
- run() function stub
- docstring
- options placeholder
"""

import os
from datetime import datetime


TEMPLATE = '''"""
{mode_name}.py
Auto-generated SSRF mode.

Description:
    TODO: Describe what this mode does.

Useful for:
    - TODO: Add use cases

"""

MODE_NAME = "{mode_name}"

def run(target, options):
    """
    Execute the {mode_name} mode.

    Parameters:
        target (str): Target URL or placeholder.
        options (dict): Mode-specific options.

    Returns:
        dict: Structured results.
    """

    # TODO: Implement mode logic
    return {{
        "mode": MODE_NAME,
        "target": target,
        "options": options,
        "message": "Mode '{mode_name}' is not implemented yet."
    }}
'''


class ModeTemplateGenerator:

    def __init__(self, base_path=None):
        self.base_path = base_path or os.path.dirname(__file__)
        self.modes_path = os.path.join(self.base_path, "modes")

    def create_mode(self, mode_name):
        """
        Create a new mode file with the given name.
        """
        filename = f"{mode_name}.py"
        filepath = os.path.join(self.modes_path, filename)

        if os.path.exists(filepath):
            return {
                "error": f"Mode '{mode_name}' already exists.",
                "path": filepath
            }

        with open(filepath, "w") as f:
            f.write(TEMPLATE.format(mode_name=mode_name))

        return {
            "created": True,
            "mode_name": mode_name,
            "path": filepath,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
