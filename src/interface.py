from asciimatics.effects import Print, Scroll, Julia
from asciimatics.renderers import ColourImageFile, FigletText, ImageFile
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from asciimatics.exceptions import ResizeScreenError, NextScene, StopApplication, InvalidFields
from asciimatics.widgets import Frame, Text, TextBox, Layout, Label, Divider, Widget, Button, PopUpDialog, ListBox, \
    RadioButtons
import os.path as op
import sys

from .padberg import Padberg

LABEL_DISCR = ["\nThis is a python implementation of Harriet Padberg's 1964 Thesis,",
               "\n\"Computer Composed Canon and Free Fugue\".\n",
               "Enter a body of text below, and the program will convert it into the perfect piece of music."]
PADBERG = Padberg()
DIRNAME = op.dirname(op.abspath(__file__))


class TextFormFrame(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                         int(screen.height),
                         int(screen.width),
                         has_shadow=True,
                         title="PyPadberg")

        layout_discr = Layout([1, 10, 1])
        self.add_layout(layout_discr)
        layout_discr.add_widget(Label("\n".join(LABEL_DISCR), height=8, align="^"), 1)

        layout_div_1 = Layout([100])
        self.add_layout(layout_div_1)
        layout_div_1.add_widget(Divider())

        layout_textbox = Layout([1, 18, 1], fill_frame=True)
        self.add_layout(layout_textbox)
        layout_textbox.add_widget(TextBox(Widget.FILL_FRAME, name="IT", label="Write Something!",
            on_change=self._on_change), 1)

        layout_div_2 = Layout([100])
        self.add_layout(layout_div_2)
        layout_div_2.add_widget(Divider())

        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        self._reset_button = Button("Reset", self._reset)
        layout2.add_widget(self._reset_button, 0)
        layout2.add_widget(Button("Submit", self._submit), 1)
        layout2.add_widget(Button("Quit", self._quit), 2)

        self.fix()

    def _on_change(self):
        self.save() # changed = False
        # for key, value in self.data.items():
        #     if key not in form_data or form_data[key] != value:
        #         changed = True
        #         break
        # self._reset_button.disabled = not changed

    def _reset(self):
        self.reset()
        raise NextScene("text_entry")

    def _submit(self):
        self.save(validate=True)
        PADBERG.process_text(self.data["IT"][0])
        raise NextScene()

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        on_close=self._quit_on_yes))

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")


class ProcessingFrame(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                        int(screen.height),
                        int(screen.width),
                        on_load=self._reload_list,
                        hover_focus=True,
                        can_scroll=False,
                        title="PyPadberg")

        layout_discr = Layout([1, 10, 1])
        self.add_layout(layout_discr)
        layout_discr.add_widget(Label("\nProcessing Logs", height=3, align="^"), 1)

        layout_div_1 = Layout([100])
        self.add_layout(layout_div_1)
        layout_div_1.add_widget(Divider())
        # Create the form for displaying the list of contacts.
        self._list_view = ListBox(
            Widget.FILL_FRAME,
            PADBERG.get_summary(),
            name="processing-log",
            add_scroll_bar=True,
        )
        layout = Layout([1, 15, 1], fill_frame=True)
        self.add_layout(layout)
        layout.add_widget(self._list_view, 1)

        layout2 = Layout([1, 1, 1])
        self.add_layout(layout2)
        layout2.add_widget(Button("Continue", self._continue), 1)

        self.fix()
        # self._on_pick()

    def _reload_list(self, new_value=None):
        self._list_view.options = PADBERG.get_summary()
        self._list_view.value = new_value

    def _continue(self):
        raise NextScene()


# a button what sound to use
# save midi
# number of voices
# play button
form_data = {'sound_choice': "one",
             'num_voices': 1,
             'fname': 'output'}

class FinalFrame(Frame):
    def __init__(self, screen):
        super().__init__(screen,
                        int(screen.height * 2 // 3),
                        int(screen.width * 2 // 3),
                        data=form_data,
                        has_shadow=True,
                       title="PyPadberg")
        layout_discr = Layout([1, 10, 1])
        self.add_layout(layout_discr)
        layout_discr.add_widget(Label("\nSelect instrument and number of voices for you piece below.\
", height=3, align="^"), 1)

        layout_div_1 = Layout([100])
        self.add_layout(layout_div_1)
        layout_div_1.add_widget(Divider())

        layout = Layout([1, 18, 1])
        self.add_layout(layout)
        layout.add_widget(RadioButtons([("one", "one"), ("two", "two"), ("three", "three")],
                                       label="Choose a Sound:",
                                       name="sound_choice",
                                       on_change=self._on_change), 1)

        layout_spacer = Layout([1, 18, 1])
        self.add_layout(layout_spacer)
        layout_spacer.add_widget(Label(" "*100, height=2, align="^"), 1)

        layout2 = Layout([1, 18, 1])
        self.add_layout(layout2)
        layout2.add_widget(RadioButtons([("1", 1), ("2", 2), ("3", 3), ("4", 4)],
                                       label="How Many Voices?:",
                                       name="num_voices",
                                       on_change=self._on_change), 1)

        layout_spacer2 = Layout([1, 18, 1])
        self.add_layout(layout_spacer2)
        layout_spacer2.add_widget(Label(" "*100, height=2, align="^"), 1)

        layout_label = Layout([1, 10, 1])
        self.add_layout(layout_label)
        layout_spacer2.add_widget(Label("You may optionally enter a name to save your melody under in the box below.",
                                  height=3, align="^"), 1)

        layout3 = Layout([1, 18, 1], fill_frame=True)
        self.add_layout(layout3)
        layout3.add_widget(Text(label="Filename: ", name="fname", on_change=self._on_change), 1)

        layout_div_2 = Layout([100])
        self.add_layout(layout_div_2)
        layout_div_2.add_widget(Divider())

        layout_buttons = Layout([1, 6, 6, 6, 1])
        self.add_layout(layout_buttons)
        layout_buttons.add_widget(Button("Play", self._play), 1)
        layout_buttons.add_widget(Button("Save Audio", self._save_audio), 2)
        layout_buttons.add_widget(Button("Save CSV", self._save_csv), 3)

        layout_buttons2 = Layout([1, 3, 3, 1])
        self.add_layout(layout_buttons2)
        layout_buttons2.add_widget(Button("Make Another", self._make_another), 1)
        layout_buttons2.add_widget(Button("Quit", self._quit), 2)
        self.fix()

    def _on_change(self):
        self.save()

    def _play(self):
        PADBERG.play(self.data["sound_choice"], self.data["num_voices"])

    def _save_audio(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Save audio as .wav file?",
                        ["Yes", "No"],
                        on_close=self._saveit_audio))

    def _save_csv(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Save melody as .csv file?",
                        ["Yes", "No"],
                        on_close=self._saveit_csv))

    def _saveit_audio(self, selected):
        if selected == 0:
            PADBERG.save_audio(self.data["sound_choice"], title=self.data["fname"])

    def _saveit_csv(self, selected):
        if selected == 0:
            PADBERG.save_csv(title=self.data["fname"])

    def _make_another(self):
        raise NextScene("text_entry")

    def _quit(self):
        self._scene.add_effect(
            PopUpDialog(self._screen,
                        "Are you sure?",
                        ["Yes", "No"],
                        on_close=self._quit_on_yes))

    @staticmethod
    def _quit_on_yes(selected):
        # Yes is the first button
        if selected == 0:
            raise StopApplication("User requested exit")


class Interface:

    def __init__(self):
        pass

    def _seq(self, screen, scene):
        scenes = []
        banner_pos = (screen.width - 100) // 2 + 20
        static_image = [
            Print(screen,
                  ColourImageFile(screen, op.join(DIRNAME, "assets", "images", "ibm1620.jpg"), screen.height, uni=screen.unicode_aware),
                  y=0,
                  speed=1,
                  stop_frame=(21 + screen.height)*2),
            Print(screen,
                  FigletText("PyPadberg", "banner"),
                  screen.height - 8, x=banner_pos,
                  colour=Screen.COLOUR_BLACK,
                  bg=Screen.COLOUR_BLACK,
                  speed=1),
            Print(screen,
                  FigletText("PyPadberg", "banner"),
                  screen.height - 9, x=(banner_pos + 1),
                  colour=Screen.COLOUR_WHITE,
                  bg=Screen.COLOUR_WHITE,
                  speed=1),
        ]
        scenes.append(Scene(static_image, name="intro2"))
        scenes.append(Scene([TextFormFrame(screen)], -1, name="text_entry"))
        scenes.append(Scene([ProcessingFrame(screen)], -1, name="display_processing"))
        final_frame = [Julia(screen), FinalFrame(screen)]
        scenes.append(Scene(final_frame, -1, name="end_menu"))
        screen.play(scenes, stop_on_resize=True, start_scene=scene)

    def run(self):
        last_scene = None
        while True:
            try:
                Screen.wrapper(self._seq, catch_interrupt=False, arguments=[last_scene])
                sys.exit(0)
            except ResizeScreenError as e:
                last_scene = e.scene
