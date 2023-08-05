import argparse
import functools
import json
from dataclasses import dataclass
from dataclasses import field
from io import TextIOWrapper
from pathlib import Path
from typing import Any
from typing import Dict
from typing import List
from typing import Union


__version__ = "1.1.0"


def main():
    parser = _create_parser()
    args = parser.parse_args()

    if hasattr(args, "handler"):
        return args.handler(args)

    parser.print_help()


def _create_parser() -> argparse.ArgumentParser:
    description = "Combine multiple dcm2bids config files into a single config file."
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        "in_file",
        nargs="+",
        type=Path,
        help="The JSON config files to combine",
    )
    parser.add_argument(
        "-o",
        "--out-file",
        type=argparse.FileType("w", encoding="utf8"),
        default="-",
        help="The file to write the combined config file to. If not "
        "specified outputs are written to stdout.",
    )
    parser.add_argument("-v", "--version", action="version", version=__version__)
    parser.set_defaults(handler=_handler)

    return parser


def _handler(args: argparse.Namespace):
    in_files: list[Path] = args.in_file
    out_file: TextIOWrapper = args.out_file
    # load all the config files passed as arguments
    configs = [json.loads(fp.read_text()) for fp in in_files]
    # combine the config files into one config
    combined_config = combine_config(configs)
    # write the combined config file to disk
    with out_file as f:
        # we output like this because json.dump(obj, f) doesn't add a trailing new-line
        f.write(json.dumps(combined_config, indent=2) + "\n")


def combine_config(input_configs: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Combine multiple dcm2bids config dicts into a single config dict.

    Args:
        input_configs (list[dict[str, Any]]): A list of dcm2bids configs (dicts)

    Returns:
        dict[str, Any]: The combined/merged config dict.
    """
    res = functools.reduce(_reduce_callback, input_configs, _ReduceResult())
    return {"descriptions": res.descriptions}


@dataclass
class _ReduceResult:
    offset: int = 0
    descriptions: List[Dict[str, Any]] = field(default_factory=list)


TIntendedFor = Union[int, str, List[Union[int, str]], None]


def _reduce_callback(agg: _ReduceResult, config: Dict[str, Any]) -> _ReduceResult:
    descriptions: List[Dict[str, Any]] = config["descriptions"]

    for description in descriptions:
        intended_for: TIntendedFor = description.get("IntendedFor")
        if intended_for is None:
            continue
        elif isinstance(intended_for, str):
            description["IntendedFor"] = intended_for
        elif isinstance(intended_for, int):
            description["IntendedFor"] = intended_for + agg.offset
        elif isinstance(intended_for, list):
            _intended_for: List[Union[int, str]] = []
            for i in intended_for:
                if isinstance(i, str):
                    _intended_for.append(i)
                elif isinstance(i, int):
                    _intended_for.append(i + agg.offset)
                else:
                    m = f"IntendedFor must be 'int' or 'str'. Found [{_intended_for}]"
                    raise ValueError(m)
            description["IntendedFor"] = _intended_for
        else:
            m = f"IntendedFor must be int, str or (int | str)[]. Found [{intended_for}]"
            raise ValueError(m)

    agg.descriptions.extend(descriptions)
    agg.offset = agg.offset + len(descriptions)

    return agg


if __name__ == "__main__":
    exit(main())
