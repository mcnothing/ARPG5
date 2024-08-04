import pygame as pg
import math
import os
from settings import *

_mixer = pg.mixer
_mixer.init()
music = _mixer.music
music.set_volume(MUSIC_VOLUME)
music_enabled = True
audio_enabled = True
sound_clips = {}
MUSIC_TRACKS = {}

def initialize_music():
    for track in os.listdir(MUSIC_FOLDER):
        track_name = track.split('.')[0]
        file_name = f'{MUSIC_FOLDER}/{track}'
        MUSIC_TRACKS[track_name] = file_name

def initialize_sounds():        
    for clip in os.listdir(SOUNDS_FOLDER):
        clip_name = clip.split('.')[0]
        file_name = f'{SOUNDS_FOLDER}/{clip}'
        load_sound(file_name, clip_name)

def load_sound(audio_file, sound_name):
    sound_clips[sound_name] = _mixer.Sound(audio_file)
    sound_clips[sound_name].set_volume(0.1)

def play_sound(sound_name, origin=None):
    global audio_enabled
    if not audio_enabled:
        return
    if origin is not None:
        if distance_to_listener(origin) > 10:
            return
        else:
            sound_clips[sound_name].play()    
    else:
        sound_clips[sound_name].play()

def distance_to_listener(point):
    return math.dist()

def toggle_sound():
    global audio_enabled
    audio_enabled = not audio_enabled

#Only one music track can be loaded at once since it streams
def load_music_track(track_name):
    _mixer.music.load(MUSIC_TRACKS[track_name])

def toggle_music() -> None:
    global music_enabled
    if music.get_busy():
        music_enabled = False
        music.stop()
    else:
        music_enabled = True
        play_music_track(True)

def play_music_track(loop=False):
    global music_enabled
    if music_enabled:
        if loop:
            music.play(-1)
        else:
            music.play()

initialize_music()
initialize_sounds()
