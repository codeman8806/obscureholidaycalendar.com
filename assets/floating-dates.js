// Resolves a holidays.json "floatingHolidays[*].dateRule" into a concrete
// {month, day} for a given year. Covers the 4 dateRule types the Firebase
// migration defined: nth-weekday-of-month, solstice, equinox, relative-to-event.
//
// Solstice/equinox anchor dates are a verified lookup table (not a formula):
// source astropixels.com/ephemeris/soleq2001.html (Fred Espenak), UTC times
// converted to US Eastern calendar-day (America/New_York, DST-aware) since
// that's the convention this site's existing holiday dates use (e.g.
// winter-solstice's originalDate is 12-21, which is the ET date every year in
// this range even though the UTC date is sometimes 12-22). Covers 2024-2050;
// resolves to null outside that range rather than guessing.
(function (global) {
  "use strict";

  var SEASONAL_MARKERS = {
    2024: [[3, 19], [6, 20], [9, 22], [12, 21]],
    2025: [[3, 20], [6, 20], [9, 22], [12, 21]],
    2026: [[3, 20], [6, 21], [9, 22], [12, 21]],
    2027: [[3, 20], [6, 21], [9, 23], [12, 21]],
    2028: [[3, 19], [6, 20], [9, 22], [12, 21]],
    2029: [[3, 20], [6, 20], [9, 22], [12, 21]],
    2030: [[3, 20], [6, 21], [9, 22], [12, 21]],
    2031: [[3, 20], [6, 21], [9, 23], [12, 21]],
    2032: [[3, 19], [6, 20], [9, 22], [12, 21]],
    2033: [[3, 20], [6, 20], [9, 22], [12, 21]],
    2034: [[3, 20], [6, 21], [9, 22], [12, 21]],
    2035: [[3, 20], [6, 21], [9, 23], [12, 21]],
    2036: [[3, 19], [6, 20], [9, 22], [12, 21]],
    2037: [[3, 20], [6, 20], [9, 22], [12, 21]],
    2038: [[3, 20], [6, 21], [9, 22], [12, 21]],
    2039: [[3, 20], [6, 21], [9, 22], [12, 21]],
    2040: [[3, 19], [6, 20], [9, 22], [12, 21]],
    2041: [[3, 20], [6, 20], [9, 22], [12, 21]],
    2042: [[3, 20], [6, 21], [9, 22], [12, 21]],
    2043: [[3, 20], [6, 21], [9, 22], [12, 21]],
    2044: [[3, 19], [6, 20], [9, 22], [12, 21]],
    2045: [[3, 20], [6, 20], [9, 22], [12, 21]],
    2046: [[3, 20], [6, 21], [9, 22], [12, 21]],
    2047: [[3, 20], [6, 21], [9, 22], [12, 21]],
    2048: [[3, 19], [6, 20], [9, 22], [12, 21]],
    2049: [[3, 20], [6, 20], [9, 22], [12, 21]],
    2050: [[3, 20], [6, 20], [9, 22], [12, 21]]
  };

  // index into each SEASONAL_MARKERS row
  var EVENT_INDEX = {
    "march-equinox": 0,
    "june-solstice": 1,
    "september-equinox": 2,
    "december-solstice": 3
  };

  var SEASON_TO_EVENT = {
    solstice: { summer: "june-solstice", winter: "december-solstice" },
    equinox: { spring: "march-equinox", fall: "september-equinox" }
  };

  function resolveSeasonalMarker(year, eventKey) {
    var row = SEASONAL_MARKERS[year];
    if (!row || !eventKey) return null;
    var idx = EVENT_INDEX[eventKey];
    if (idx === undefined) return null;
    var pair = row[idx];
    return { month: pair[0], day: pair[1] };
  }

  // weekday: 0=Sun..6=Sat (matches Date#getDay()); ordinal: 1-4, or -1 for "last"
  function resolveNthWeekday(year, month, weekday, ordinal) {
    if (ordinal === -1) {
      var last = new Date(year, month, 0); // day 0 of "next" month = last day of `month`
      var diff = (last.getDay() - weekday + 7) % 7;
      return { month: month, day: last.getDate() - diff };
    }
    var first = new Date(year, month - 1, 1);
    var offset = (weekday - first.getDay() + 7) % 7;
    return { month: month, day: 1 + offset + (ordinal - 1) * 7 };
  }

  function resolveRelativeToEvent(year, event, weekday, direction) {
    var anchor = resolveSeasonalMarker(year, event);
    if (!anchor) return null;
    var d = new Date(year, anchor.month - 1, anchor.day);
    var step = direction === "before" ? -1 : 1;
    do {
      d.setDate(d.getDate() + step);
    } while (d.getDay() !== weekday);
    return { month: d.getMonth() + 1, day: d.getDate() };
  }

  function resolveDateRule(dateRule, year) {
    if (!dateRule || !dateRule.type) return null;
    switch (dateRule.type) {
      case "nth-weekday-of-month":
        return resolveNthWeekday(year, dateRule.month, dateRule.weekday, dateRule.ordinal);
      case "solstice":
        return resolveSeasonalMarker(year, (SEASON_TO_EVENT.solstice || {})[dateRule.season]);
      case "equinox":
        return resolveSeasonalMarker(year, (SEASON_TO_EVENT.equinox || {})[dateRule.season]);
      case "relative-to-event":
        return resolveRelativeToEvent(year, dateRule.event, dateRule.weekday, dateRule.direction);
      default:
        return null;
    }
  }

  global.FloatingDates = {
    resolveDateRule: resolveDateRule
  };
})(window);
