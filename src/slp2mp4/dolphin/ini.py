# Logic for dolphin INIs
# https://github.com/dolphin-emu/fifoci/

import configparser
import contextlib
import pathlib

import slp2mp4.util as util


@contextlib.contextmanager
def make_ini_file(filename: pathlib.Path, contents: dict):
    filename.parent.mkdir(parents=True, exist_ok=True)
    with open(filename, "w") as ini_file:
        ini_parser = configparser.ConfigParser(
            allow_no_value=True, delimiters=("=",), strict=False
        )
        ini_parser.optionxform = lambda option: option
        for section, options in contents.items():
            ini_parser.add_section(section)
            for opt_name, opt_val in options.items():
                ini_parser.set(section, opt_name, opt_val)
        ini_parser.write(ini_file)
        ini_file.flush()
        yield filename, ini_file


@contextlib.contextmanager
def make_dolphin_file(userdir: pathlib.Path):
    # TODO: Try full screen / forced window size for Windows
    settings = {
        # Disables rumble, since it's annoying when rendering replays

        "Core": {
            "AdapterRumble0": "False",
            "AdapterRumble1": "False",
            "AdapterRumble2": "False",
            "AdapterRumble3": "False",
        # Sets emulation speed to unlimited, unlikely but why not?
            "EmulationSpeed" : "0.00000000",
        },
        # Enables dumping frames
        "Movie": {
            "DumpFrames": "True",
            "DumpFramesSlient": "True",
        },
        # Enables dumping audio
        "DSP": {
            "DumpAudio": "True",
            "DumpAudioSilent": "True",
            "Backend": "OpenAL",
            "Volume": "0",  # Mute playback audio; audio is still dumped
        },
        "Display": {
            "RenderToMain": "True",
            "RenderWindowWidth": None,
            "RenderWindowHeight": None,
            "RenderWindowAutoSize": "True",
        },
    }
    filename = userdir.joinpath("Config", "Dolphin.ini")
    with make_ini_file(filename, settings) as (name, handle):
        yield name


@contextlib.contextmanager
def make_gfx_file(userdir: pathlib.Path, user_settings):
    # Could use Settings.DumpFramesAsImages, then detect all-black images
    settings = {
        "Settings": {
            "AspectRatio": "0",
            "InternalResolutionFrameDumps": "True",
        },
    }
    util.update_dict(settings, user_settings)
    filename = userdir.joinpath("Config", "GFX.ini")
    with make_ini_file(filename, settings) as (name, handle):
        yield name


@contextlib.contextmanager
def make_gal_file(userdir: pathlib.Path, user_settings):
    settings = {}
    util.update_dict(settings, user_settings)
    filename = userdir.joinpath("GameSettings", "GAL.ini")
    with make_ini_file(filename, settings) as (name, handle):
        yield name


@contextlib.contextmanager
def make_hotkeys_file(userdir: pathlib.Path):
    settings = {
        "Hotkeys1": {
            "Device": "/0/",
        }
    }
    filename = userdir.joinpath("Config", "Hotkeys.ini")
    with make_ini_file(filename, settings) as (name, handle):
        yield name


@contextlib.contextmanager
def make_gecko_file(userdir: pathlib.Path, user_gecko):
    settings = {
        # Not exactly clean, but seems to work without issues 
        "Gecko": {
            "$Smaller Ready, GO! Text Graphics on Match Start [UnclePunch]\nC22F71E0 0000000D\n4800004D 7D8802A6\n8083000C 80840000\nC02C0000 D0240020\nD0240024 D0240028\nC02C0008 D0240030\n80830010 80840000\nC02C0004 D0240020\nD0240024 D0240028\nC02C0008 D0240030\n48000014 4E800021\n3F19999A 3ECCCCCD\n41200000 80030010\n60000000 00000000\n" : None,
            "$HUD Transparency v1.1 [UnclePunch]\nC22F6690 0000009D\n7C0802A6 90010004\n9421FF00 BE810008\n3860000E 3880000F\n38A00000 3D808039\n618C01F0 7D8903A6\n4E800421 7C7F1B78\n38600090 3D808037\n618CF1E4 7D8903A6\n4E800421 7C7E1B78\n38800090 3D808000\n618CC160 7D8903A6\n4E800421 7FC6F378\n7FE3FB78 38800004\n3CA08037 60A5F1B0\n3D808039 618C0B68\n7D8903A6 4E800421\n7FE3FB78 48000059\n7C8802A6 38A00013\n3D808038 618CFD54\n7D8903A6 4E800421\n4800040D 7C6802A6\n7FC4F378 38A00000\nC0230008 D0240000\nC023000C D0240008\nC0230010 D0240010\n38A50001 38840018\n2C050006 4180FFDC\n480003F8 4E800021\n7C0802A6 90010004\n9421FF00 BE810008\n83E3002C 480003B9\n7FC802A6 3A800000\n7FF5FB78 C03E0008\nD0350004 C03E000C\nD035000C C03E0010\nD0350014 3A940001\n3AB50018 2C140006\n4180FFDC 806DC18C\n82830020 480001D8\n82B4002C 8875221F\n54600673 408201C4\n8875221E 54600631\n408201B8 C03506F8\nC0550778 EC41102A\nD0410080 C0550780\nEC41102A D0410084\nC03506F4 C055078C\nEC41102A D0410088\nC0550784 EC41102A\nD041008C 3D808003\n618C0A50 7D8903A6\n4E800421 83A30028\n38600000 90610068\nC0210088 D0210060\nC0210080 D0210064\n7FA3EB78 38810060\n38A10070 38C00000\n3D808000 618CE210\n7D8903A6 4E800421\nC0210070 D0210088\nC0210074 D0210080\nC021008C D0210060\nC0210084 D0210064\n7FA3EB78 38810060\n38A10070 38C00000\n3D808000 618CE210\n7D8903A6 4E800421\nC0210070 D021008C\nC0210074 D0210084\n3AC00000 7EC3B378\n3D80802F 618C3424\n7D8903A6 4E800421\n7C641B78 3C60804A\n60630FD8 80630000\n80630028 38A10090\n38C00000 3D808000\n618CE210 7D8903A6\n4E800421 C0210090\nC05E0014 EC21102A\nC0410088 FC020840\n4080007C C0210090\nC05E0014 EC211028\nC041008C FC020840\n40810064 C0210094\nC05E0018 EC211028\nC0410084 FC020840\n4081004C C0210094\nC05E0018 EC21102A\nC0410080 FC020840\n40800034 1C760018\n7C63FA14 C05E0000\nC03E0008 EC2100B2\nD0230004 C03E000C\nEC2100B2 D023000C\nC03E0010 EC2100B2\nD0230014 3AD60001\n2C160006 4180FF28\n82940008 2C140000\n4082FE28 3A800000\n1C740018 7EA3FA14\n3C60804A 60631380\n1C940050 7C632214\n80630000 2C030000\n4182000C 38950000\n4800006D 3C60804A\n606310C8 1C940064\n7C632214 80630004\n2C030000 4182000C\n38950008 48000049\n3C60804A 606310C8\n1C940064 7C632214\n80630000 2C030000\n4182000C 38950010\n48000025 3A940001\n2C140006 4180FF84\nBA810008 80010104\n38210100 7C0803A6\n4E800020 7C0802A6\n90010004 9421FF00\nBE810008 83E30028\n7C9E2378 480000E9\n7FA802A6 C03E0000\nC05E0004 C07D0004\nFC011040 4182003C\n41810018 EC21182A\nFC011040 40810020\nFC201090 48000018\nEC211828 FC011040\n4080000C FC201090\n48000004 D03E0000\n7FE3FB78 48000019\nBA810008 80010104\n38210100 7C0803A6\n4E800020 7C0802A6\n90010004 9421FFE4\n93E10014 93C10018\n7C7F1B78 83DF0018\n48000024 807E0008\n2C030000 41820014\n8063000C 2C030000\n41820008 D023000C\n83DE0004 2C1E0000\n4082FFDC 807F0010\n2C030000 41820008\n4BFFFFAD 807F0008\n2C030000 41820008\n4BFFFF9D 83C10018\n83E10014 80010020\n3821001C 7C0803A6\n4E800020 4E800021\n3ECCCCCD 3DA3D70A\n3F7FBE77 3F32F1AA\n3F7FBE77 42820000\n42820000 40000000\nBA810008 80010104\n38210100 7C0803A6\n8001001C 00000000\n" : None,
        }
    }
    util.update_dict(settings, user_gecko)
    filename = userdir.joinpath("GameSettings", "GALE01.ini")
    with make_ini_file(filename, settings) as (name, handle):
        yield name
