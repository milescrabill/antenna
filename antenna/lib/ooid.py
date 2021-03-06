# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This is based on socorrolib's socorrolib/lib/ooid.py module.

# OOID is "Our opaque ID"
import uuid
from datetime import datetime

from antenna.lib.datetimeutil import utc_now, UTC


DEFAULT_DEPTH = 2
OLD_HARD_DEPTH = 4


def create_new_ooid(timestamp=None, depth=None):
    """Create a new Ooid for a given time, to be stored at a given depth

    :arg timestamp: the year-month-day is encoded in the ooid. If none, use
        current day.

    :arg depth: the expected storage depth is encoded in the ooid. If non, use
        the DEFAULT_DEPTH returns a new opaque id string holding 24 random hex
        digits and encoded date and depth info

    """
    if not timestamp:
        timestamp = utc_now().date()
    if not depth:
        depth = DEFAULT_DEPTH
    assert depth <= 4 and depth >= 1
    id_ = str(uuid.uuid4())
    return "%s%d%02d%02d%02d" % (
        id_[:-7], depth, timestamp.year % 100, timestamp.month, timestamp.day
    )


def uuid_to_ooid(uuid, timestamp=None, depth=None):
    """Create an ooid from a 32-hex-digit string in regular uuid format.

    :arg uuid: must be uuid in expected format:
        ``xxxxxxxx-xxxx-xxxx-xxxx-xxxxx7777777``

    :arg timestamp: the year-month-day is encoded in the ooid. If none, use
        current day

    :arg depth: the expected storage depth is encoded in the ooid. If non, use
        the DEFAULT_DEPTH returns a new opaque id string holding the first 24
        digits of the provided uuid and encoded date and depth info

    """
    if not timestamp:
        timestamp = utc_now().date()
    if not depth:
        depth = DEFAULT_DEPTH
    assert depth <= 4 and depth >= 1
    return "%s%d%02d%02d%02d" % (
        uuid[:-7], depth, timestamp.year % 100, timestamp.month, timestamp.day
    )


def date_and_depth_from_ooid(ooid):
    """Extract the encoded date and expected storage depth from an ooid.

    :arg ooid: The ooid from which to extract the info

    :returns: ``(datetime(yyyy, mm, dd), depth)`` if the ooid is in expected
    format else ``(None, None)``

    """
    year = month = day = None
    try:
        day = int(ooid[-2:])
    except Exception:
        return None, None
    try:
        month = int(ooid[-4:-2])
    except Exception:
        return None, None
    try:
        year = 2000 + int(ooid[-6:-4])
        depth = int(ooid[-7])
        if not depth:
            depth = OLD_HARD_DEPTH
        return (datetime(year, month, day, tzinfo=UTC), depth)
    except Exception:
        return None, None
    return None, None


def depth_from_ooid(ooid):
    """Extract the encoded expected storage depth from an ooid.

    :arg ooid: The ooid from which to extract the info

    :returns: expected depth if the ooid is in expected format else None

    """
    return date_and_depth_from_ooid(ooid)[1]


def date_from_ooid(ooid):
    """Extract the encoded date from an ooid.

    :arg ooid: The ooid from which to extract the info

    :returns: encoded date if the ooid is in expected format else None

    """
    return date_and_depth_from_ooid(ooid)[0]
