import time
import os
import platform
import subprocess

# Import Windows-specific sound library if on Windows
if platform.system() == "Windows":
    import winsound

def clear_screen():
    # Mac/Linux ('clear') / Windows ('cls')
    os.system('cls' if os.name == 'nt' else 'clear')

def countdown(t):
    total_t = t 
    while t >= 0:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        
        # Calculate progress, avoiding division by zero just in case
        progress = int(((total_t - t) / total_t) * 50) if total_t > 0 else 50
        bar = '█' * progress + '-' * (50 - progress)
        
        print(f'[{bar}] {timeformat}', end='\r')
        
        if t == 0:
            break
            
        time.sleep(1)
        t -= 1

def play_sound(filename):
    os_name = platform.system()
    try:
        if os_name == "Windows":
            # Added SND_ASYNC to play the sound in the background
            winsound.PlaySound(filename, winsound.SND_FILENAME | winsound.SND_ASYNC)
        elif os_name == "Darwin": # macOS
            # Popen spawns the process in the background and moves on immediately
            subprocess.Popen(["afplay", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        elif os_name == "Linux":
            # Popen spawns the process in the background and moves on immediately
            subprocess.Popen(["aplay", filename], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    except Exception:
        print('\a', end='\r')

def main():
    session = True
    while session:
        clear_screen()

        setup = True
        while setup:
            input_values = input("Enter 6 values separated by space, or press Enter for defaults (50 10 0 4 1 0): ")

            if not input_values.strip():
                work_minutes, short_break_minutes, long_break_minutes, num_cycles, num_blocks, wrap_up_minutes = 50, 10, 0, 4, 1, 0
                setup = False
            
            else:        
                try:
                    work_minutes, short_break_minutes, long_break_minutes, num_cycles, num_blocks, wrap_up_minutes = map(int, input_values.split())
                    if len(input_values.split(" ")) == 6:
                        setup = False
                    else:
                        print("Invalid input!")
                
                except Exception:
                    print("ERROR! Invalid input!")

        # filenames for ding and dingding
        short_break_sound = "short_break.wav"
        long_break_sound = "long_break.wav"

        for block in range(num_blocks):
            for cycle in range(num_cycles):
                
                # Work Session
                clear_screen()
                print(f"Block {block + 1} of {num_blocks}")
                print(f"Work session {cycle + 1} of {num_cycles}")
                countdown(work_minutes * 60)
                
                # Short break
                if cycle < num_cycles - 1:    
                    play_sound(short_break_sound)
                    clear_screen()
                    print(f"Block {block + 1} of {num_blocks}")
                    print("Short break")
                    countdown(short_break_minutes * 60)
                    play_sound(short_break_sound)

            # Long Break
            if block < num_blocks - 1:
                play_sound(long_break_sound)
                clear_screen()
                print(f"Block {block + 1} of {num_blocks}")
                print("Long break")
                countdown(long_break_minutes * 60)
                play_sound(short_break_sound)
        
        # Wrap-up Timer
        if wrap_up_minutes > 0:
            play_sound(long_break_sound)
            clear_screen()
            print("Timer Complete")
            print("Wrap-up")
            countdown(wrap_up_minutes * 60)
            play_sound(long_break_sound)

        # End of session
        clear_screen()
        print("Timer completed. Good job!\n")

        newSession = True
        while newSession:
            reply = input("Would you like to start another session? (y/n): ").lower()
            if reply in ["y", "yes"]:
                newSession = False
            elif reply in ["n", "no"]:
                newSession = False
                session = False

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTimer stopped manually. See you next time!")
        os._exit(0)