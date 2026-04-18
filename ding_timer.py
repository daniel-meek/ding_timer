#!/usr/bin/env python3
"""
ding_timer

A Pomodoro timer utility for the Windows and Linux terminals.

Author: daniel-meek
Version: v0.0.2-experimental (18.04.2026)
Repository: https://github.com/daniel-meek/ding_timer
License: MIT
Copyright (c) 2026 daniel-meek

This software is released under the MIT License.
https://opensource.org/licenses/MIT
"""

import time
import os
import platform
import subprocess

# Import Windows-specific sound library if on Windows
if platform.system() == "Windows":
    import winsound

def clear_screen():
    # Linux ('clear') / Windows ('cls')
    os.system('cls' if os.name == 'nt' else 'clear')

def hide_cursor():
    """Hides the terminal cursor."""
    print('\033[?25l', end="", flush=True)

def show_cursor():
    """Restores the terminal cursor."""
    print('\033[?25h', end="", flush=True)

def countdown(t, block_header="", work_header=""):
    t = t * 60
    total_t = t
    while t >= 0:
        try:
            mins, secs = divmod(t, 60)
            timeformat = '{:02d}:{:02d}'.format(mins, secs)
            
            progress = int(((total_t - t) / total_t) * 50) if total_t > 0 else 50
            bar = '█' * progress + '-' * (50 - progress)
            
            print(f'[{bar}] {timeformat}', end='\r')
            
            if t == 0:
                break
                
            time.sleep(1)
            t -= 1
            
        except KeyboardInterrupt:
            # First Ctrl+C caught -> PAUSE
            show_cursor()
            print(f'\r[{bar}] {timeformat} - PAUSED\nPress ENTER to resume or Ctrl+C to quit.', end='')
            
            try:
                wait_for_enter = input() # Wait for the user to press Enter
                
                # Easter egg section >:3
                if wait_for_enter == "password123":
                    clear_screen()
                    print("That is a really bad password buddy...")
                    time.sleep(2)
                    print("Like... really really bad... do better...")
                    time.sleep(2)
                    print("Resuming...")
                    time.sleep(3)
                
                # Resuming! Re-draw the screen to keep the UI clean
                hide_cursor()
                clear_screen()
                print(block_header)
                print(work_header)
                
            except (KeyboardInterrupt, EOFError): 
                # Second Ctrl+C or EOF signal caught -> QUIT via the __main__ block
                raise KeyboardInterrupt from None
            
def play_sound(filename):
    os_name = platform.system()
    try:
        if os_name == "Windows":
            # Added SND_ASYNC to play the sound in the background
            winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif os_name == "Linux":
            # Popen spawns the process in the background and moves on immediately
            subprocess.Popen(["aplay", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    except Exception:
        print('\a', end='\r')

def main():
    while True:
        clear_screen()
        
        setup = True
        while setup:
            input_values = input("Enter 6 values separated by space, or press Enter for defaults (50 10 0 4 1 0): ")

            if not input_values.strip():
                work_minutes, short_break_minutes, long_break_minutes, num_sessions, num_blocks, wrap_up_minutes = 50, 10, 0, 4, 1, 0
                setup = False
            
            else:        
                try:
                    work_minutes, short_break_minutes, long_break_minutes, num_sessions, num_blocks, wrap_up_minutes = map(int, input_values.split())
                    if len(input_values.split(" ")) == 6:
                        setup = False
                    else:
                        print("Invalid input!")
                
                except Exception:
                    print("ERROR! Invalid input!")

        # filenames for ding and dingding
        short_break_sound = "short_break.wav"
        long_break_sound = "long_break.wav"

        hide_cursor()

        for block in range(num_blocks):
            for session in range(num_sessions):
                
                # Work Session
                block_header = f"Block {block + 1} of {num_blocks}"
                work_header = f"Work session {session + 1} of {num_sessions}"
                clear_screen()
                print(block_header)
                print(work_header)
                countdown(work_minutes, block_header, work_header)
                
                # Short break
                if session < num_sessions - 1:    
                    play_sound(short_break_sound)
                    work_header = "Short break"
                    clear_screen()
                    print(block_header)
                    print(work_header)
                    countdown(short_break_minutes, block_header, work_header)
                    play_sound(short_break_sound)

            # Long Break
            if block < num_blocks - 1:
                play_sound(long_break_sound)
                work_header = "Long break"
                clear_screen()
                print(block_header)
                print(work_header)
                countdown(long_break_minutes, block_header, work_header)
                play_sound(short_break_sound)
        
        # Wrap-up Timer
        if wrap_up_minutes > 0:
            play_sound(long_break_sound)
            block_header = "Timer Complete"
            work_header = "Wrap-up"
            clear_screen()
            print(block_header)
            print(work_header)
            countdown(wrap_up_minutes, block_header, work_header)
        
        # End of session
        play_sound(long_break_sound)
        clear_screen()
        show_cursor()
        print("Timer completed. Good job!\n")
        
        while True:
            reply = input("Would you like to start another session? (y/n): ").lower()
            if reply in ["y", "yes"]:
                break
            elif reply in ["n", "no"]:
                return

if __name__ == "__main__":
    try:
        main()
    
    # Catch exit signals (Ctrl+C)
    except (KeyboardInterrupt, EOFError):
        try:
            print("\n\nTimer stopped manually. See you next time!")
        
        except Exception:
            pass
        
        finally:
            os._exit(0)