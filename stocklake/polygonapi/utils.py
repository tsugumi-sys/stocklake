import time

from stocklake.core.stdout import PrettyStdoutPrint


def avoid_request_limit(
    threshold: int, current_request_count: int, stdout: PrettyStdoutPrint
):
    if current_request_count < threshold:
        return
    if current_request_count % 5 != 0:
        return
    stdout.normal_message("Waiting for 70 seconds to avoid request limit")
    time.sleep(70)
