import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

import asyncio  # noqa: E402
from src.presentation import main  # noqa: E402

if __name__ == "__main__":
    asyncio.run(main())
