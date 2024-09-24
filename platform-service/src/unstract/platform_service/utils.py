import logging
import os
import re
from typing import Optional


class EnvManager:
    missing_settings: list[str] = []

    @classmethod
    def get_required_setting(
        cls, setting_key: str, default: Optional[str] = None
    ) -> Optional[str]:
        """Get the value of an environment variable specified by the given key.
        Add missing keys to `missing_settings` so that exception can be raised
        at the end.

        Args:
            key (str): The key of the environment variable
            default (Optional[str], optional): Default value to return incase of
                env not found. Defaults to None.

        Returns:
            Optional[str]: The value of the environment variable if found,
                otherwise the default value.
        """
        data = os.environ.get(setting_key, default)
        if not data:
            cls.missing_settings.append(setting_key)
        return data

    @classmethod
    def raise_for_missing_envs(cls) -> None:
        """Raises an error if some settings are not configured.

        Raises:
            ValueError: Error mentioning envs which are not configured.
        """
        if cls.missing_settings:
            ERROR_MESSAGE = "Below required settings are missing.\n" + ",\n".join(
                cls.missing_settings
            )
            raise ValueError(ERROR_MESSAGE)


def format_float_positional(value: float, precision: int = 10) -> str:
    """Format floats to a string.

    Formats a floating-point number to a string with the specified precision,
    removing trailing zeros and the decimal point if not needed.

    Args:
        value (float): The floating-point number to format.
        precision (int, optional): The number of decimal places to
            include in the formatted output. Defaults to 10.

    Returns:
        str: The formatted string representation of the float,
            with unnecessary trailing zeros and the decimal point
            removed if the float is an integer.
    """
    formatted: str = f"{value:.{precision}f}"
    return formatted.rstrip("0").rstrip(".") if "." in formatted else formatted


class RemoveAccessLogTimestamp(logging.Filter):
    # '127.0.0.1 - - [24/Sep/2024 06:57:35] "%s" %s %s' -> '192.168.0.102 - "%s" %s %s'
    pattern: re.Pattern = re.compile(r' - - \[.+?] "')

    def filter(self, record: logging.LogRecord) -> bool:
        record.msg = self.pattern.sub(' - "', record.msg)
        return True
