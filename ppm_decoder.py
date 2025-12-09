import board
import pulseio
import time

PPM_PIN = board.GP0
NUM_CHANNELS = 8
SYNC_US = 4200

# Create PulseIn object that measures HIGH pulse lengths
ppm = pulseio.PulseIn(PPM_PIN, maxlen=100, idle_state=False)

# Clear buffer initially
ppm.clear()

def get_ppm_frame():
    """
    Reads pulses until a sync (>4ms) then reads NUM_CHANNELS pulses.
    Returns a list of channel widths in microseconds.
    """
    channels = [499] * NUM_CHANNELS

    # Wait for sync
    while True:
        if ppm:
            pulse = ppm.popleft()
            if pulse > SYNC_US:
                break

    # Now read each channel
    for i in range(NUM_CHANNELS):
        while not ppm:
            pass  # wait for next pulse
        pulse = ppm.popleft()

        # Acceptable pulse range
        if 499 < pulse < 2200:
            channels[i] = pulse
    return channels

if __name__ == "__main__":
    while False:
        ch = get_ppm_frame()
        print("CH:", ch)
    while  True:
        while ppm:
            print(ppm.popleft())
