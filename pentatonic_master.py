from __future__ import annotations
import random
import tkinter
from tkinter import ttk


class FretBoard:
    def __init__(self, master: tkinter.Misc, width: int, height: int, note_size: int) -> None:
        self._note_size = note_size
        self._board = tkinter.Canvas(
            master, width=width, height=height, highlightthickness=0)
        self._notes = []
        self._emphasized_note = None

    def plot_note(self, fret_number: int, string_number: int) -> None:
        note = self._board.create_oval(fret_number*self._note_size, string_number*self._note_size,
                                       (fret_number+1) *self._note_size, (string_number+1) *self._note_size,
                                       fill="black")
        self._notes.append(note)

    def plot_notes(self, note_positions: list[list[int]]) -> None:
        for string_number, fret_numbers in enumerate(note_positions):
            for fret_number in fret_numbers:
                self.plot_note(fret_number, string_number)

    def delete_notes(self) -> None:
        for note in self._notes:
            self._board.delete(note)
        self._notes.clear()

    def emphasize_note(self, note: tkinter._CanvasItemId) -> None:
        if self._emphasized_note is not None:
            self._board.itemconfig(self._emphasized_note, fill="black")

        self._board.itemconfig(note, fill="red")
        self._emphasized_note = note

    def choose_note_randomly(self) -> tkinter._CanvasItemId:
        return random.choice(self._notes)

    def choose_and_emphasize_note_randomly(self) -> None:
        while True:
            emphasized_note_new = self.choose_note_randomly()
            if (self._emphasized_note is None) or (self._emphasized_note is not emphasized_note_new):
                self.emphasize_note(emphasized_note_new)
                break

    def pack(self) -> None:
        self._board.pack()


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("Pentatonic Master")
    root.geometry("500x300")


    fretboard_panel = tkinter.Frame(root, pady=30)
    fretboard_panel.pack()

    pentatonic_positions = [[[0, 3],
                            [0, 3],
                            [0, 2],
                            [0, 2],
                            [0, 2],
                            [0, 3]],

                            [[1, 3],
                            [1, 3],
                            [0, 2],
                            [0, 3],
                            [0, 3],
                            [1, 3]],

                            [[1, 3],
                            [1, 4],
                            [0, 3],
                            [1, 3],
                            [1, 3],
                            [1, 3]],

                            [[0, 3],
                            [1, 3],
                            [0, 2],
                            [0, 2],
                            [0, 3],
                            [0, 3]],

                            [[1, 3],
                            [1, 3],
                            [0, 3],
                            [0, 3],
                            [1, 3],
                            [1, 3]]]

    pentatonic_pattern = tkinter.IntVar(root, value=0)
    fretboard = FretBoard(fretboard_panel, 101, 121, 20)
    fretboard.plot_notes(pentatonic_positions[pentatonic_pattern.get()])
    fretboard.pack()


    control_panel = tkinter.Frame(root)
    control_panel.pack()

    def change_pentatonic_pattern(event: tkinter.Event) -> None:
        fretboard.delete_notes()
        fretboard.plot_notes(pentatonic_positions[pentatonic_pattern.get()])

    pentatonic_pattern_pulldown = ttk.Combobox(control_panel,
                                               values=[0, 1, 2, 3, 4], textvariable=pentatonic_pattern, state="readonly", width=5)
    pentatonic_pattern_pulldown.bind(
        "<<ComboboxSelected>>", change_pentatonic_pattern)
    pentatonic_pattern_pulldown.pack(side=tkinter.LEFT)

    sleep_time_milli = tkinter.IntVar(control_panel, value=1000)
    sleep_time_scale = tkinter.Scale(control_panel, variable=sleep_time_milli, orient=tkinter.HORIZONTAL,
                                     from_=100, to=2000, resolution=100, tickinterval=200, length=300)
    sleep_time_scale.pack(side=tkinter.LEFT)


    def start_roulette() -> None:
        fretboard.choose_and_emphasize_note_randomly()
        root.after(sleep_time_milli.get(), start_roulette)

    start_roulette()

    root.mainloop()
