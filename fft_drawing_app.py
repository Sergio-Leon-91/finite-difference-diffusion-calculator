"""
Interactive 2D discrete Fourier transform visualizer.

Use the Tkinter canvas to sketch a grayscale drawing. When you click
"Compute FFT" the app converts the drawing to an array, runs a centered
2D FFT and opens a matplotlib window to show both the spatial drawing
and its log-magnitude spectrum.
"""
import tkinter as tk
from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw


class FourierDrawingApp:
    """Simple Tkinter application to draw and visualize a 2D FFT."""

    def __init__(self, size: int = 256) -> None:
        self.size = size
        self.root = tk.Tk()
        self.root.title("2D Finite Fourier Transform Drawer")

        self.canvas = tk.Canvas(
            self.root,
            width=self.size,
            height=self.size,
            bg="white",
            highlightthickness=1,
            highlightbackground="#888",
        )
        self.canvas.grid(row=0, column=0, columnspan=3, padx=10, pady=10)

        self._create_controls()
        self._create_drawing_buffer()
        self._bind_drawing()

    def _create_controls(self) -> None:
        """Add buttons and labels for user interaction."""
        ttk.Label(
            self.root,
            text=(
                "Draw with the left mouse button. Click 'Compute FFT' to"
                " view the spectrum."
            ),
            wraplength=self.size + 140,
        ).grid(row=1, column=0, columnspan=3, padx=10, pady=(0, 6))

        ttk.Button(self.root, text="Compute FFT", command=self.compute_fft).grid(
            row=2, column=0, padx=10, pady=6, sticky="ew"
        )
        ttk.Button(self.root, text="Clear Canvas", command=self.clear).grid(
            row=2, column=1, padx=10, pady=6, sticky="ew"
        )
        ttk.Button(self.root, text="Quit", command=self.root.destroy).grid(
            row=2, column=2, padx=10, pady=6, sticky="ew"
        )

    def _create_drawing_buffer(self) -> None:
        """Create an in-memory image mirroring the Tk canvas."""
        self.image = Image.new("L", (self.size, self.size), color=255)
        self.draw = ImageDraw.Draw(self.image)
        self.last_pos: tuple[int, int] | None = None

    def _bind_drawing(self) -> None:
        self.canvas.bind("<ButtonPress-1>", self._start_draw)
        self.canvas.bind("<B1-Motion>", self._draw)
        self.canvas.bind("<ButtonRelease-1>", self._end_draw)

    def _start_draw(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        self.last_pos = (event.x, event.y)

    def _draw(self, event: tk.Event) -> None:  # type: ignore[type-arg]
        if self.last_pos is None:
            self.last_pos = (event.x, event.y)
            return
        current_pos = (event.x, event.y)
        self.canvas.create_line(self.last_pos, current_pos, fill="black", width=4)
        self.draw.line([self.last_pos, current_pos], fill=0, width=4)
        self.last_pos = current_pos

    def _end_draw(self, _event: tk.Event) -> None:  # type: ignore[type-arg]
        self.last_pos = None

    def clear(self) -> None:
        """Erase the drawing on both the canvas and the backing image."""
        self.canvas.delete("all")
        self._create_drawing_buffer()

    def compute_fft(self) -> None:
        """Compute and display the centered 2D FFT of the drawing."""
        array = np.asarray(self.image, dtype=float) / 255.0
        array = 1.0 - array  # invert so drawn strokes are bright features
        spectrum = np.fft.fftshift(np.fft.fft2(array))
        magnitude = np.abs(spectrum)
        log_magnitude = np.log1p(magnitude)

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))
        fig.suptitle("2D Finite Fourier Transform")

        ax1.imshow(array, cmap="gray", origin="upper")
        ax1.set_title("Drawing (brightness)")
        ax1.axis("off")

        ax2.imshow(log_magnitude, cmap="magma", origin="lower")
        ax2.set_title("Log magnitude spectrum")
        ax2.axis("off")

        fig.tight_layout()
        plt.show(block=False)

    def run(self) -> None:
        """Start the Tkinter main loop."""
        self.root.mainloop()


def main() -> None:
    app = FourierDrawingApp(size=256)
    app.run()


if __name__ == "__main__":
    main()
