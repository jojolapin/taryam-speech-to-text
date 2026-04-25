from pathlib import Path

from PIL import Image, ImageDraw


def generate_icon(path: Path) -> None:
    canvas = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(canvas)
    draw.ellipse((16, 16, 240, 240), fill=(26, 115, 232, 255))
    draw.rounded_rectangle((104, 64, 152, 156), radius=22, fill=(255, 255, 255, 255))
    draw.rounded_rectangle((92, 148, 164, 172), radius=8, fill=(255, 255, 255, 255))
    draw.rectangle((122, 168, 134, 200), fill=(255, 255, 255, 255))
    draw.rounded_rectangle((94, 198, 162, 212), radius=6, fill=(255, 255, 255, 255))
    canvas.save(path, format="ICO", sizes=[(256, 256), (128, 128), (64, 64), (48, 48), (32, 32), (16, 16)])
