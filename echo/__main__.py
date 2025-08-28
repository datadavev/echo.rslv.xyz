"""
Module script for echo.

echo.rslv.xyz  Copyright (C) 2024 Dave Vieglais
This program comes with ABSOLUTELY NO WARRANTY.
This is free software, and you are welcome to redistribute it
under certain conditions; see LICENSE details.

"""

import sys
import uvicorn


def serve() -> int:
    uvicorn.run(
        "echo.fapi:app", host="127.0.0.1", port=3000, log_level="info", reload=True
    )
    return 0


def main() -> int:
    print(__doc__)
    return serve()


if __name__ == "__main__":
    sys.exit(main())
