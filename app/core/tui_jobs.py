import curses
import threading
import time
from datetime import datetime
from typing import Callable, Dict, List, Optional


class Job:
    def __init__(self, job_id: int, mode: str, targets: List[str], options: dict, runner: Callable):
        self.id = job_id
        self.mode = mode
        self.targets = targets
        self.options = options
        self.runner = runner

        self.status = "Running"
        self.start_time = datetime.now()
        self.end_time: Optional[datetime] = None
        self.log: List[str] = []
        self.thread: Optional[threading.Thread] = None
        self.cancel_flag = False

    def append_log(self, text: str):
        self.log.append(text)

    def cancel(self):
        self.cancel_flag = True


class JobManager:
    def __init__(self):
        self.jobs: Dict[int, Job] = {}
        self.next_id = 1

    def start_job(self, mode: str, targets: List[str], options: dict, runner: Callable):
        job_id = self.next_id
        self.next_id += 1

        job = Job(job_id, mode, targets, options, runner)
        self.jobs[job_id] = job

        t = threading.Thread(target=self._run_job, args=(job,), daemon=True)
        job.thread = t
        t.start()

        return job_id

    def _run_job(self, job: Job):
        try:
            for idx, target in enumerate(job.targets, start=1):
                if job.cancel_flag:
                    job.append_log("[CANCELLED]")
                    job.status = "Cancelled"
                    job.end_time = datetime.now()
                    return

                result = job.runner(job.mode, target, job.options)
                job.append_log(f"[{job.mode}] {target}\n{result}\n")

            job.status = "Done"
        except Exception as e:
            job.append_log(f"[ERROR] {str(e)}")
            job.status = "Error"

        job.end_time = datetime.now()


def draw_jobs_panel(screen, job_manager: JobManager):
    """
    Popup panel showing all jobs and allowing inspection/cancellation.
    """
    h, w = screen.getmaxyx()
    win_h = min(25, h - 4)
    win_w = min(80, w - 4)

    start_y = (h - win_h) // 2
    start_x = (w - win_w) // 2

    win = curses.newwin(win_h, win_w, start_y, start_x)
    win.keypad(True)

    job_ids = list(job_manager.jobs.keys())
    index = 0
    viewing_log = False
    log_scroll = 0

    while True:
        win.clear()
        win.border()

        if not viewing_log:
            win.addstr(0, 2, " Background Jobs ")

            for i, job_id in enumerate(job_ids):
                job = job_manager.jobs[job_id]
                label = f"#{job.id} [{job.status}] {job.mode} ({len(job.targets)} targets)"

                if i == index:
                    win.attron(curses.A_REVERSE)
                    win.addstr(i + 2, 2, label[: win_w - 4])
                    win.attroff(curses.A_REVERSE)
                else:
                    win.addstr(i + 2, 2, label[: win_w - 4])

            win.addstr(win_h - 2, 2, "ENTER: View log   K: Kill job   ESC: Close")

        else:
            job = job_manager.jobs[job_ids[index]]
            win.addstr(0, 2, f" Job #{job.id} Log ")

            visible_h = win_h - 4
            start = max(0, len(job.log) - visible_h - log_scroll)
            end = start + visible_h

            for i, line in enumerate(job.log[start:end]):
                win.addstr(i + 2, 2, line[: win_w - 4])

            win.addstr(win_h - 2, 2, "UP/DOWN: Scroll   ESC: Back")

        win.refresh()
        key = win.getch()

        if not viewing_log:
            if key == curses.KEY_UP:
                index = max(0, index - 1)
            elif key == curses.KEY_DOWN:
                index = min(len(job_ids) - 1, index + 1)
            elif key in (10, 13):  # ENTER
                viewing_log = True
                log_scroll = 0
            elif key == ord('k') or key == ord('K'):
                job_manager.jobs[job_ids[index]].cancel()
            elif key == 27:
                return
        else:
            if key == curses.KEY_UP:
                log_scroll = min(log_scroll + 1, len(job.log))
            elif key == curses.KEY_DOWN:
                log_scroll = max(log_scroll - 1, 0)
            elif key == 27:
                viewing_log = False
