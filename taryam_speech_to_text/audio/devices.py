from __future__ import annotations

import sounddevice as sd


def list_input_devices() -> list[str]:
    names: list[str] = []
    for dev in sd.query_devices():
        if dev.get("max_input_channels", 0) > 0:
            names.append(dev["name"])
    return names


def resolve_device_index(name: str) -> int | None:
    if not name:
        return None
    for idx, dev in enumerate(sd.query_devices()):
        if dev.get("max_input_channels", 0) > 0 and dev["name"] == name:
            return idx
    return None
