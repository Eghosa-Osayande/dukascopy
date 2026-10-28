import json
import re
from datetime import datetime
from pathlib import Path
from pprint import pformat

from dukascopy_python.core.http import create_session

from ..impl.v2 import ApiV2


def generate_instruments(data: dict) -> None:
    constants = []
    instrument_map = {}
    exports = []
    seen = set()

    for instrument in data["instruments"]:
        code = instrument["code"]

        identifier = re.sub(
            r"[^A-Za-z0-9]+", "_", code
        ).strip("_").upper()

        variable_name = f"I_{identifier}"

        if variable_name in seen:
            raise ValueError(
                f"Duplicate constant: {variable_name}"
            )

        seen.add(variable_name)
        exports.append(variable_name)

        constants.append(
            f"{variable_name} = {code!r}\n"
        )

        # Preserve the full instrument metadata
        instrument_map[variable_name] = instrument

    exports.append("INSTRUMENT_CODE_TO_DATA")

    lines = [
        "# Auto-generated instrument constants and metadata\n",
        "# Do not edit manually.\n\n",
        "__all__ = [\n",
        f"    {'INSTRUMENT_CODE_TO_DATA'!r},\n",
        *(f"    {name!r},\n" for name in exports),
        "]\n\n",
        *constants,
        "\n",
        "INSTRUMENT_CODE_TO_DATA = {\n",
    ]

    for key, instrument in instrument_map.items():
        formatted = pformat(
            instrument,
            indent=4,
            sort_dicts=False,
        )

        lines.append(
            f"    {key}: {formatted},\n"
        )

    lines.append("}\n")

    current_dir = Path(__file__).resolve().parent

    (current_dir / "instruments.py").write_text(
        "".join(lines),
        encoding="utf-8",
    )


if __name__ == "__main__":
    current_dir = Path(__file__).resolve().parent

    date = datetime.now().strftime("%Y_%m_%d")
    json_file = current_dir / f"{date}.json"

    if not json_file.exists():
        with create_session() as session:
            data = ApiV2(session).get_instruments()

        with json_file.open("w", encoding="utf-8") as f:
            json.dump(
                data,
                f,
                indent=4,
                ensure_ascii=False,
            )

    with json_file.open(encoding="utf-8") as f:
        data = json.load(f)

    generate_instruments(data)