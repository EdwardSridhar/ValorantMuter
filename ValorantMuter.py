import win32gui
import win32process
import time
from pycaw.pycaw import AudioUtilities, ISimpleAudioVolume

# Set the name of the program you want to auto-mute
program_name = "VALORANT-Win64-Shipping.exe"

# Store the previous state of the volume for the program
previous_volume = {}

try:
    while True:
        # Get the process ID of the currently focused window
        fg_win = win32gui.GetForegroundWindow()
        fg_thread, fg_process =  win32process.GetWindowThreadProcessId(fg_win)

        # Get the audio session for the program
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session._ctl.QueryInterface(ISimpleAudioVolume)
            if session.Process and session.Process.name() == program_name:
                session_identifier = session._ctl.GetSessionIdentifier()
                # Mute the audio if the program is out of focus
                if fg_process != session.ProcessId:
                    previous_volume[session_identifier] = volume.GetMasterVolume()
                    volume.SetMute(1, None)  # Set mute
                # Unmute the audio if the program is in focus
                else:
                    if session_identifier in previous_volume:
                        volume.SetMute(0, None)  # Unmute

        # Wait for 0.1 seconds before checking again
        time.sleep(1)

except KeyboardInterrupt:
    print("Script stopped by user")
