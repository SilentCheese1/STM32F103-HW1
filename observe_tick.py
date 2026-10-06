"""Read the homework tick variable from a running STM32 over CMSIS-DAP.

Run on the Mac after stopping the pyOCD GDB server so the probe is free.
This attaches without resetting or halting the microcontroller.
"""

import argparse
import time

from pyocd.core.helpers import ConnectHelper
from pyocd.core.target import Target


TICK_ADDRESS = 0x2000007C  # From arm-none-eabi-nm on both homework ELFs.


def main() -> None:
    parser = argparse.ArgumentParser(description="Observe STM32 homework tick")
    parser.add_argument("--seconds", type=int, default=8)
    parser.add_argument("--pack", required=True, help="Path to STM32F1 device pack")
    parser.add_argument("--address", type=lambda value: int(value, 0), default=TICK_ADDRESS)
    args = parser.parse_args()

    options = {
        "target_override": "stm32f103c8",
        "pack": args.pack,
        "connect_mode": "attach",
    }
    session = ConnectHelper.session_with_chosen_probe(options=options)
    if session is None:
        raise SystemExit("No CMSIS-DAP probe found")

    print(f"STM32F103C8T6 tick at {args.address:#010x} (1-second samples)", flush=True)
    print("sample   tick       change", flush=True)
    previous = None
    with session:
        if session.target.get_state() == Target.State.HALTED:
            session.target.resume()
        for sample in range(args.seconds + 1):
            value = session.target.read32(args.address)
            change = "—" if previous is None else str(value - previous)
            print(f"{sample:>6}   {value:>10}   {change:>10}", flush=True)
            previous = value
            if sample < args.seconds:
                time.sleep(1)


if __name__ == "__main__":
    main()
