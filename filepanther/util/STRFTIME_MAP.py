STRFTIME_MAP = {
    "%a": "{dt_a:3w}",  # Weekday as locale's abbreviated name.   |  Mon
    "%A": "{dt_A:w}day",  # Weekday as locale's full name.   |  Monday
    # Weekday as a decimal number, where 0 is Sunday and 6 is Saturday.   |  1
    "%w": "{dt_w:01d}",
    # Day of the month as a zero-padded decimal number.   |  30
    "%d": "{dt_d:02d}",
    # Day of the month as a decimal number. (Platform specific)   |  30
    "%-d": "{dt_dd:d}",
    "%b": "{dt_b:3w}",  # Month as locale's abbreviated name.   |  Sep
    "%B": "{dt_B:w}",  # Month as locale's full name.   |  September
    "%m": "{dt_m:02d}",  # Month as a zero-padded decimal number.   |  09
    # Month as a decimal number. (Platform specific)   |  9
    "%-m": "{dt_mm:d}",
    # Year without century as a zero-padded decimal number.   |  13
    "%y": "{dt_y:02d}",
    "%Y": "{dt_Y:04d}",  # Year with century as a decimal number.   |  2013
    # Hour (24-hour clock) as a zero-padded decimal number.   |  07
    "%H": "{dt_H:02d}",
    # Hour (24-hour clock) as a decimal number. (Platform specific)   |  7
    "%-H": "{dt_HH:d}",
    # Hour (12-hour clock) as a zero-padded decimal number.   |  07
    "%I": "{dt_I:02d}",
    # Hour (12-hour clock) as a decimal number. (Platform specific)   |  7
    "%-I": "{dt_II:}",
    "%p": "{dt_p:2w}",  # Locale's equivalent of either AM or PM.   |  AM
    "%M": "{dt_M:02d}",  # Minute as a zero-padded decimal number.   |  06
    # Minute as a decimal number. (Platform specific)   |  6
    "%-M": "{dt_MM:d}",
    "%S": "{dt_S:02d}",  # Second as a zero-padded decimal number.   |  05
    # Second as a decimal number. (Platform specific)   |  5
    "%-S": "{dt_SS:d}",
    # Microsecond as a decimal number, zero-padded on the left.   |  000000
    "%f": "{dt_f:06d}",
    # UTC offset in the form +HHMM or -HHMM (empty string if object is naive).
    "%z": "{dt_z:4w}",
    "%Z": "{dt_Z:w}",  # Time zone name (empty string if the object is naive).
    # Day of the year as a zero-padded decimal number.   |  273
    "%j": "{dt_j:03d}",
    # Day of the year as a decimal number. (Platform specific)   |  273
    "%-j": "{dt_jj:d}",
    # Week number of the year (Sunday as the first day of the week)
    # as a zero padded decimal number. All days in a new year preceding the
    # first Sunday are considered to be in week 0.   |  39
    "%U": "{dt_U:}",
    # Week number of the year (Monday as the first day of the week)
    # as a decimal number. All days in a new year preceding the first
    # Monday are considered to be in week 0.   |  39
    "%W": "{dt_W:02d}",
    # Locale's appropriate date and time representation.
    # |  Mon Sep 30 07:06:05 2013
    "%c": "{dt_c}",
    "%x": "{dt_x}",  # Locale's appropriate date representation.   |  09/30/13
    "%X": "{dt_X}",  # Locale's appropriate time representation.   |  07:06:05
    "%%": "%"  # A literal '%' character.   |  %
}
