import sys
import traceback
from app.main import create_app
from app.core.crash_reporter import write_crash_report
from app.core.health_bootstrap import wait_for_dependencies
import uvicorn


def main() -> int:
    try:
        wait_for_dependencies()

        app = create_app()

        uvicorn.run(
            app,
            host="0.0.0.0",
            port=8000,
            reload=False,
            workers=1,
            proxy_headers=True,
            forwarded_allow_ips="*",
        )
        return 0

    except Exception as exc:
        tb = traceback.format_exc()
        write_crash_report(exc, tb, context="run.py main()")
        print("[FATAL] Backend crashed. See crash report for details.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
