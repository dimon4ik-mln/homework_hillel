import logging
import re
from typing import Optional

KEY = "TSTFEED0300|7E3E|0400"

LINE_RE = re.compile(r"Timestamp\s+(\d{2}:\d{2}:\d{2}).*?\bKey\s+([^\s]+)")


def _to_seconds(hms: str) -> int:
    h, m, s = map(int, hms.split(":"))
    return h * 3600 + m * 60 + s


def analyze_heartbeat(
        input_path: str,
        key: str = KEY,
        output_log_path: str = "hb_test.log",
) -> str:
    """
    1) Відбирає лише рядки з потрібним key
    2) Рахує heartbeat між сусідніми повідомленнями потоку
       (враховує, що лог найчастіше йде "зверху вниз" у спадному часі)
    3) Логує:
       - WARNING якщо heartbeat > 31 і < 33 (тобто 32s)
       - ERROR   якщо heartbeat >= 33
    4) В повідомлення додає час, коли стався збій (timestamp "пізнішого" запису),
       а також обидва timestamp і номери рядків для дебагу.
    Повертає шлях до output_log_path.
    """

    # ---- logger ----
    logger = logging.getLogger("hb_test")
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()

    fh = logging.FileHandler(output_log_path, mode="w", encoding="utf-8")
    fh.setFormatter(logging.Formatter("%(levelname)s %(message)s"))
    logger.addHandler(fh)

    # ---- read + filter ----
    rows = []  # (line_no, ts_str, seconds)
    with open(input_path, "r", encoding="utf-8", errors="ignore") as f:
        for line_no, line in enumerate(f, 1):
            m = LINE_RE.search(line)
            if not m:
                continue
            ts_str, k = m.group(1), m.group(2)
            if k != key:
                continue
            rows.append((line_no, ts_str, _to_seconds(ts_str)))

    if len(rows) < 2:
        logger.error(f"Not enough records for key={key}. Found: {len(rows)}")
        return output_log_path

        # ---- detect direction (descending vs ascending) ----
    sample_diffs = []
    for (ln1, ts1, s1), (ln2, ts2, s2) in zip(rows, rows[1:20]):
        sample_diffs.append(s1 - s2)

    descending = sum(1 for d in sample_diffs if d >= 0) >= sum(1 for d in sample_diffs if d < 0)

    # ---- analyze ----
    for (ln_prev, ts_prev, sec_prev), (ln_cur, ts_cur, sec_cur) in zip(rows, rows[1:]):
        if descending:
            delta = sec_prev - sec_cur
        else:
            delta = sec_cur - sec_prev

        if delta < 0:
            delta += 86400

        if 31 < delta < 33:
            logger.warning(
                f"Heartbeat {delta}s at {ts_prev} (prev line {ln_prev}) -> {ts_cur} (line {ln_cur})"
            )
        elif delta >= 33:
            logger.error(
                f"Heartbeat {delta}s at {ts_prev} (prev line {ln_prev}) -> {ts_cur} (line {ln_cur})"
            )

    return output_log_path


if __name__ == "__main__":
    analyze_heartbeat("hblog.txt", KEY, "hb_test.log")
