# functions.py
# Template from https://aierlab.tech/MultiverseNote/docs/en/getting_started.html

from __future__ import annotations

import typing as tp
import threading
import os

import mido

def playAccompanimentTrackRealtimeTempo(*_, **__):
    print('Time for Yuxuan to bring it on!')
    return 'Success. Now shut up and don\'t say a word.'

class MidiPlayer:
    singleton: MidiPlayer | None = None

    def __new__(cls) -> MidiPlayer:
        if cls.singleton is None:
            cls.singleton = super().__new__(cls)
        return cls.singleton
    
    def __init__(self):
        # ask for output port
        outputs = mido.get_output_names()   # type: ignore
        for i, name in enumerate(outputs):
            print(i, name, sep = '\t')
        selected = outputs[int(input('> '))]
        print(f'{selected = }')
        self.output_name = selected
    
    @classmethod
    def startPlaying(cls, filename: str):
        if cls.singleton is None:
            raise ValueError('MidiPlayer is not initialized. You need to call MidiPlayer() at the start of everything.')
        if not os.path.isfile(filename):
            print('Error. The file does not exist.')
            return 'Error. The file does not exist.'
        thread = threading.Thread(target=cls.singleton.play, args=(filename, ))
        thread.start()
        return 'Success. The player piano has started playing the MIDI file. Silently wait for it to finish.'

    @staticmethod
    def any2zero(x: int):   # an example channel remap
        return 0

    @staticmethod
    def identity(x: int):
        return x
    
    def play(
        self, 
        filename: str, 
        channel_remap: tp.Callable[[int], int | None] = identity,
        scale_velocity: float = 1.0, 
        discard_meta: bool = True, 
        verbose: bool = True, 
    ):
        '''
        This is blocking.
        `channel_remap`: return None to discard message.  
        '''
        with mido.open_output(self.output_name) as port:    # type: ignore
            down_keys = set()
            with mido.MidiFile(filename) as mid:
                if verbose:
                    print('playing...')
                try:
                    for msg in mid.play(meta_messages = not discard_meta):
                        if verbose:
                            print(msg)
                        try:
                            msg.velocity = round(msg.velocity * scale_velocity)
                            new_channel = channel_remap(msg.channel)
                            if new_channel is None:
                                continue
                            msg.channel = new_channel
                        except AttributeError:
                            pass    # allow control_change
                        port.send(msg)
                        if msg.type == 'note_on' and msg.velocity != 0:
                            down_keys.add(msg.note)
                        elif msg.type == 'note_off' or (msg.type == 'note_on' and msg.velocity == 0):
                            down_keys.discard(msg.note)
                except KeyboardInterrupt:
                    if verbose:
                        print('Stop. ')
                finally:
                    port.panic()
                    # in case the MIDI device did not implement panic
                    for note in down_keys:
                        port.send(mido.Message('note_off', note=note))
        if verbose:
            print('ok')

FUNCTION_MAPPING = {
    "playAccompanimentTrackRealtimeTempo": playAccompanimentTrackRealtimeTempo,
    "playMidiOnPiano": MidiPlayer.startPlaying,
}

TOOLS_DEFINE = [
    {
        "type": "function",
        "function": {
            "name": "playAccompanimentTrackRealtimeTempo",
            "description": "Enter the phase to play the accompaniment track on the piano, attending and adapting to the human player's tempo.",
            "parameters": {
                "type": "object",
                "properties": {
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "playMidiOnPiano",
            "description": "Starts to play a MIDI file on the player piano.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {
                        "type": "string",
                        "description": "The Midi file to play."
                    }
                },
                "required": ["filename"]
            }
        }
    }
]
