import pygame, sys, math, argparse, struct, base64, socket, threading, queue
from dataclasses import dataclass
from enum import IntEnum
from typing import Union

# Really, really bad controller visualizer to assist in using the robots.

# Robot control protocol thoughts:
# 4 bytes for floats for analog controls
# Digital buttons packed into bitfields
# Base64 encoded

# 4-byte "control message number"
#   - The ESP32 should respond with this number to indicate that it has acknowledged the message.
# 2 bytes: button bitfield
#   - Smallest bit to largest bit:
#     - Right Bumper
#     - Left Bumper
#     - Start
#     - Back
#     - A
#     - B
#     - X
#     - Y
#     - Right Stick
#     - Left Stick
#     - Guide button
#     - Reserved
#     - Reserved
#     - Reserved
#     - Reserved
#     - Reserved
# 1 byte: D-pad direction
#   - Smallest to largest bit:
#     - East
#     - Northeast
#     - North
#     - Northwest
#     - West
#     - Southwest
#     - South
#     - Southeast
# 4 bytes: Right trigger (float)
# 4 bytes: Left trigger (float)
# 4 bytes: Right stick X (float)
# 4 bytes: Right stick Y (float)
# 4 bytes: Left stick X (float)
# 4 bytes: Left stick Y (float)

_message_number = 0

ROBOT_IP_ADDRESS = "192.168.4.1"
ROBOT_PORT = 1853

class Direction(IntEnum):
    NONE      = 0
    EAST      = 1
    NORTHEAST = 1 << 1
    NORTH     = 1 << 2
    NORTHWEST = 1 << 3
    WEST      = 1 << 4
    SOUTHWEST = 1 << 5
    SOUTH     = 1 << 6
    SOUTHEAST = 1 << 7


@dataclass
class GamepadState:
    """Class for storing the current state of the selected gamepad."""
    connected:          bool      = False
    left_stick_x:       float     = 0.0             # Axis 0
    left_stick_y:       float     = 0.0             # Axis 1
    right_stick_x:      float     = 0.0             # Axis 3
    right_stick_y:      float     = 0.0             # Axis 4
    left_trigger:       float     = 0.0             # Axis 2
    right_trigger:      float     = 0.0             # Axis 5
    d_pad:              Direction = Direction.NONE  #
    right_bumper:       bool      = False           # Button 5
    left_bumper:        bool      = False           # Button 4
    start_button:       bool      = False           # Button 7
    back_button:        bool      = False           # Button 6
    x_button:           bool      = False           # Button 2
    a_button:           bool      = False           # Button 0
    b_button:           bool      = False           # Button 1
    y_button:           bool      = False           # Button 3
    right_stick_button: bool      = False           # Button 9
    left_stick_button:  bool      = False           # Button 8
    guide_button:       bool      = False           # Button 10

def read_gamepad(joystick: Union[pygame.joystick.Joystick, None]) -> GamepadState:
    g = GamepadState()
    if joystick is not None:
        g.connected = True
        g.left_stick_x = joystick.get_axis(0)
        g.left_stick_y = joystick.get_axis(1)
        g.right_stick_x = joystick.get_axis(3)
        g.right_stick_y = joystick.get_axis(4)
        g.left_trigger = joystick.get_axis(2)
        g.right_trigger = joystick.get_axis(5)

        g.right_bumper = joystick.get_button(5)
        g.left_bumper = joystick.get_button(4)
        g.start_button = joystick.get_button(7)
        g.back_button = joystick.get_button(6)
        g.a_button = joystick.get_button(0)
        g.b_button = joystick.get_button(1)
        g.x_button = joystick.get_button(2)
        g.y_button = joystick.get_button(3)
        g.right_stick_button = joystick.get_button(9)
        g.left_stick_button = joystick.get_button(8)
        g.guide_button = joystick.get_button(10)

        # Still need to handle d_pad.
        return g

    keys = pygame.key.get_pressed()
    g.connected = False
    g.left_stick_x = 1.0 if keys[pygame.K_d] else -1.0 if keys[pygame.K_a] else 0.0
    g.left_stick_y = 1.0 if keys[pygame.K_s] else -1.0 if keys[pygame.K_w] else 0.0
    g.right_stick_x = 1.0 if keys[pygame.K_l] else -1.0 if keys[pygame.K_j] else 0.0
    g.right_stick_y = 1.0 if keys[pygame.K_k] else -1.0 if keys[pygame.K_i] else 0.0
    g.left_trigger = 0.5 if keys[pygame.K_2] else 0.0
    g.right_trigger = 0.75 if keys[pygame.K_9] else 0.0

    g.right_bumper = keys[pygame.K_0]
    g.left_bumper = keys[pygame.K_1]
    g.start_button = keys[pygame.K_8]
    g.back_button = keys[pygame.K_3]
    g.a_button = keys[pygame.K_DOWN]
    g.b_button = keys[pygame.K_RIGHT]
    g.x_button = keys[pygame.K_LEFT]
    g.y_button = keys[pygame.K_UP]
    g.right_stick_button = keys[pygame.K_7]
    g.left_stick_button = keys[pygame.K_4]
    g.guide_button = keys[pygame.K_SPACE]

    d_pad_number = Direction.NONE
    if keys[pygame.K_KP6]:
        d_pad_number = Direction.EAST
    if keys[pygame.K_KP9]:
        d_pad_number = Direction.NORTHEAST
    if keys[pygame.K_KP8]:
        d_pad_number = Direction.NORTH
    if keys[pygame.K_KP7]:
        d_pad_number = Direction.NORTHWEST
    if keys[pygame.K_KP4]:
        d_pad_number = Direction.WEST
    if keys[pygame.K_KP1]:
        d_pad_number = Direction.SOUTHWEST
    if keys[pygame.K_KP2]:
        d_pad_number = Direction.SOUTH
    if keys[pygame.K_KP3]:
        d_pad_number = Direction.SOUTHEAST

    g.d_pad = d_pad_number
    return g



def pack_and_send_message(sock: socket.socket, gamepad: GamepadState): #When we get controllers, this should not be based on keys, this is just for testing.
    global _message_number
    control_message_number_bytes = _message_number.to_bytes(4, byteorder='little')

    button_number = 0
    button_number |= int(gamepad.right_bumper)       << 0 # Right bumper
    button_number |= int(gamepad.left_bumper)        << 1 # Left bumper
    button_number |= int(gamepad.start_button)       << 2 # Start
    button_number |= int(gamepad.back_button)        << 3 # Back
    button_number |= int(gamepad.a_button)           << 4 # A
    button_number |= int(gamepad.b_button)           << 5 # B
    button_number |= int(gamepad.x_button)           << 6 # X
    button_number |= int(gamepad.y_button)           << 7 # Y
    button_number |= int(gamepad.right_stick_button) << 8 # Right stick
    button_number |= int(gamepad.left_stick_button)  << 9 # Left stick
    button_number |= int(gamepad.guide_button)       << 10

    button_bytes = button_number.to_bytes(2, byteorder='little')

    d_pad_bytes = gamepad.d_pad.to_bytes(1, byteorder='little')

    rt_bytes = struct.pack('<f', gamepad.right_trigger)
    lt_bytes = struct.pack('<f', gamepad.left_trigger)
    lsx_bytes = struct.pack('<f', gamepad.left_stick_x)
    lsy_bytes = struct.pack('<f', gamepad.left_stick_y)
    rsx_bytes = struct.pack('<f', gamepad.right_stick_x)
    rsy_bytes = struct.pack('<f', gamepad.right_stick_y)

    message_bytes = b"".join([control_message_number_bytes, button_bytes, d_pad_bytes, rt_bytes, lt_bytes, rsx_bytes, rsy_bytes, lsx_bytes, lsy_bytes])

    #print(f"{int.from_bytes(message_bytes, byteorder='little'):0248b}")
    sock.sendto(base64.b64encode(message_bytes) + b'\n', (ROBOT_IP_ADDRESS, ROBOT_PORT))

    _message_number += 1
    _message_number %= 2**(4*8)

def control_thread(control_input_queue: queue.Queue, control_hz: int, keep_alive: threading.Event):

    clock = pygame.time.Clock()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while keep_alive.is_set():
        gamepad = GamepadState()
        while not control_input_queue.empty():
            gamepad = control_input_queue.get_nowait()
        
        pack_and_send_message(sock, gamepad)

        clock.tick(control_hz)

    sock.close()

def display_thread(control_input_queue: queue.Queue, display_hz: int):

    clock = pygame.time.Clock()

    gamepad = GamepadState()

    label_font = pygame.font.SysFont('lucidaconsole', 12)
    button_font = pygame.font.SysFont('lucidaconsole', 32)

    width, height = 1000, 1000
    screen = pygame.display.set_mode(size=(width, height), flags=pygame.SCALED | pygame.RESIZABLE)
    pygame.display.set_caption("Cornell College Engineering Club Robot Controller")

    DARK_GRAPHITE = (25, 23, 24)
    GRAPHITE = (61, 59, 60)
    BLUE = (64, 64, 255)
    PLATINUM = (235, 235, 235)
    RED = (255, 64, 64)

    yb_label = button_font.render('Y', True, PLATINUM)
    bb_label = button_font.render('B', True, PLATINUM)
    ab_label = button_font.render('A', True, PLATINUM)
    xb_label = button_font.render('X', True, PLATINUM)

    ybl_rect = yb_label.get_rect()
    bbl_rect = bb_label.get_rect()
    abl_rect = ab_label.get_rect()
    xbl_rect = xb_label.get_rect()

    lb_label = button_font.render('LB', True, PLATINUM)
    rb_label = button_font.render('RB', True, PLATINUM)
    lt_label = button_font.render('LT', True, PLATINUM)
    rt_label = button_font.render('RT', True, PLATINUM)

    lbl_rect = lb_label.get_rect()
    rbl_rect = rb_label.get_rect()
    ltl_rect = lt_label.get_rect()
    rtl_rect = rt_label.get_rect()

    back_label = button_font.render("BACK", True, PLATINUM)
    start_label = button_font.render("START", True, PLATINUM)
    bl_rect = back_label.get_rect()
    sl_rect = start_label.get_rect()


    while True:
        gamepad = read_gamepad(None)
        try:
            control_input_queue.put_nowait(gamepad)
        except queue.Full:
            pass

        screen.fill(DARK_GRAPHITE)

        left_stick_box = pygame.draw.rect(screen, GRAPHITE, (175, 100, 300, 300))
        right_stick_box = pygame.draw.rect(screen, GRAPHITE, (width//2 + 25, 100, 300, 300))

        pygame.draw.aaline(screen, PLATINUM, (175 + 300/2, 100), (175 + 300/2, 100 + 300))
        pygame.draw.aaline(screen, PLATINUM, (175, 100 + 300/2), (175 + 300, 100 + 300/2))

        pygame.draw.aaline(screen, PLATINUM, (width//2 + 25 + 300/2, 100), (width//2 + 25 + 300/2, 100 + 300))
        pygame.draw.aaline(screen, PLATINUM, (width//2 + 25, 100 + 300/2), (width//2 + 25 + 300, 100 + 300/2))

        la_label = label_font.render("Left Analog Stick", True, PLATINUM)
        la_label_rect = la_label.get_rect()
        la_label_rect.center = (left_stick_box[0] + left_stick_box[2]//2, 90)
        screen.blit(la_label, la_label_rect)

        ra_label = label_font.render("Right Analog Stick", True, PLATINUM)
        ra_label_rect = ra_label.get_rect()
        ra_label_rect.center = (right_stick_box[0] + right_stick_box[2]//2, 90)
        screen.blit(ra_label, ra_label_rect)

        # Triggers
        pygame.draw.rect(screen, PLATINUM if gamepad.left_trigger != 0.0 else DARK_GRAPHITE, (48, 198, 104, 204))
        pygame.draw.rect(screen, PLATINUM if gamepad.right_trigger != 0.0 else DARK_GRAPHITE, (width-50-102, 198, 104, 204))

        lt_down = 200 + int((1 - gamepad.left_trigger) * 200)
        lt_height = 200 + 200 - lt_down
        rt_down = 200 + int((1 - gamepad.right_trigger) * 200)
        rt_height = 200 + 200 - rt_down

        left_trigger_box = pygame.draw.rect(screen, GRAPHITE, (50, 200, 100, 200))
        right_trigger_box = pygame.draw.rect(screen, GRAPHITE, (width-50-100, 200, 100, 200))

        pygame.draw.rect(screen, BLUE, (50, lt_down, 100, lt_height))
        pygame.draw.rect(screen, RED, (width-50-100, rt_down, 100, rt_height))

        # Bumpers
        pygame.draw.rect(screen, PLATINUM if gamepad.left_bumper else DARK_GRAPHITE, (48, 98, 104, 79))
        pygame.draw.rect(screen, PLATINUM if gamepad.right_bumper else DARK_GRAPHITE, (width-50-102, 98, 104, 79))
        left_bumper_box = pygame.draw.rect(screen, BLUE if gamepad.left_bumper else GRAPHITE, (50, 100, 100, 75))
        right_bumper_box = pygame.draw.rect(screen, RED if gamepad.right_bumper else GRAPHITE, (width-50-100, 100, 100, 75))

        # Start and Back

        pygame.draw.rect(screen, PLATINUM if gamepad.back_button else DARK_GRAPHITE, (48, 200 + 200 + 23, 104, 79))
        pygame.draw.rect(screen, PLATINUM if gamepad.start_button else DARK_GRAPHITE, (width-50-102, 200 + 200 + 23, 104, 79))
        back_box = pygame.draw.rect(screen, BLUE if gamepad.back_button else GRAPHITE, (50, 200 + 200 + 25, 100, 75))
        start_box = pygame.draw.rect(screen, RED if gamepad.start_button else GRAPHITE, (width-50-100, 200 + 200 + 25, 100, 75))

        # Buttons
        buttons_centroid = (
            right_stick_box[0] + right_stick_box[2]//2,
            right_stick_box[1] + right_stick_box[3] + 50 + 100
        )

        pygame.draw.circle(screen, PLATINUM if gamepad.y_button else DARK_GRAPHITE, (buttons_centroid[0], buttons_centroid[1]-75), 42)
        pygame.draw.circle(screen, PLATINUM if gamepad.a_button else DARK_GRAPHITE, (buttons_centroid[0], buttons_centroid[1]+75), 42)
        pygame.draw.circle(screen, PLATINUM if gamepad.x_button else DARK_GRAPHITE, (buttons_centroid[0]-75, buttons_centroid[1]), 42)
        pygame.draw.circle(screen, PLATINUM if gamepad.b_button else DARK_GRAPHITE, (buttons_centroid[0]+75, buttons_centroid[1]), 42)

        yb_box = pygame.draw.circle(screen, RED if gamepad.y_button else GRAPHITE, (buttons_centroid[0], buttons_centroid[1]-75), 40)
        ab_box = pygame.draw.circle(screen, RED if gamepad.a_button else GRAPHITE, (buttons_centroid[0], buttons_centroid[1]+75), 40)
        xb_box = pygame.draw.circle(screen, RED if gamepad.x_button else GRAPHITE, (buttons_centroid[0]-75, buttons_centroid[1]), 40)
        bb_box = pygame.draw.circle(screen, RED if gamepad.b_button else GRAPHITE, (buttons_centroid[0]+75, buttons_centroid[1]), 40)

        # D-pad
        dpad_centroid = (
            left_stick_box[0] + left_stick_box[2]//2,
            left_stick_box[1] + left_stick_box[3] + 50 + 100
        )

        angle = None
        match gamepad.d_pad:
            case Direction.EAST:
                angle = 0
            case Direction.NORTHEAST:
                angle = 45
            case Direction.NORTH:
                angle = 90
            case Direction.NORTHWEST:
                angle = 135
            case Direction.WEST:
                angle = 180
            case Direction.SOUTHWEST:
                angle = 225
            case Direction.SOUTH:
                angle = 270
            case Direction.SOUTHEAST:
                angle = 315
            case _:
                pass
    
        pygame.draw.circle(screen, PLATINUM if angle is not None else DARK_GRAPHITE, dpad_centroid, 127)
        pygame.draw.circle(screen, GRAPHITE, dpad_centroid, 125)
        pygame.draw.aaline(screen, PLATINUM, (dpad_centroid[0], dpad_centroid[1] - 110), (dpad_centroid[0], dpad_centroid[1] + 110))
        pygame.draw.aaline(screen, PLATINUM, (dpad_centroid[0] - 110, dpad_centroid[1]), (dpad_centroid[0] + 110, dpad_centroid[1]))
        if angle is not None:
            dpad_endpoint = (
                dpad_centroid[0] + math.cos(math.radians(angle)) * 90,
                dpad_centroid[1] - math.sin(math.radians(angle)) * 90
            )
            pygame.draw.circle(screen, PLATINUM, dpad_centroid, 14)
            pygame.draw.line(screen, PLATINUM, dpad_centroid, dpad_endpoint, 23)
            pygame.draw.circle(screen, PLATINUM, dpad_endpoint, 22)
            pygame.draw.circle(screen, BLUE, dpad_centroid, 12)
            pygame.draw.line(screen, BLUE, dpad_centroid, dpad_endpoint, 19)
            pygame.draw.circle(screen, BLUE, dpad_endpoint, 20)


        # Analog stick indicators
        left_stick_pos = (
            left_stick_box[0] + gamepad.left_stick_x * left_stick_box[2]//2 + left_stick_box[2]//2,
            left_stick_box[1] + gamepad.left_stick_y * left_stick_box[3]//2 + left_stick_box[3]//2
        )
        right_stick_pos = (
            right_stick_box[0] + gamepad.right_stick_x * right_stick_box[2]//2 + right_stick_box[2]//2,
            right_stick_box[1] + gamepad.right_stick_y * right_stick_box[3]//2 + right_stick_box[3]//2
        )

        pygame.draw.circle(screen, PLATINUM, left_stick_pos, 17 if gamepad.left_stick_button else 12)
        pygame.draw.circle(screen, BLUE if gamepad.left_stick_button else GRAPHITE, left_stick_pos, 15 if gamepad.left_stick_button else 10)
        pygame.draw.circle(screen, PLATINUM, right_stick_pos, 17 if gamepad.right_stick_button else 12)
        pygame.draw.circle(screen, RED if gamepad.right_stick_button else GRAPHITE, right_stick_pos, 15 if gamepad.right_stick_button else 10)

        ybl_rect.center = yb_box.center
        bbl_rect.center = bb_box.center
        abl_rect.center = ab_box.center
        xbl_rect.center = xb_box.center

        screen.blit(yb_label, ybl_rect)
        screen.blit(bb_label, bbl_rect)
        screen.blit(ab_label, abl_rect)
        screen.blit(xb_label, xbl_rect)

        lbl_rect.center = left_bumper_box.center
        rbl_rect.center = right_bumper_box.center
        ltl_rect.center = left_trigger_box.center
        rtl_rect.center = right_trigger_box.center

        screen.blit(lb_label, lbl_rect)
        screen.blit(rb_label, rbl_rect)
        screen.blit(lt_label, ltl_rect)
        screen.blit(rt_label, rtl_rect)

        bl_rect.center = back_box.center
        sl_rect.center = start_box.center

        screen.blit(back_label, bl_rect)
        screen.blit(start_label, sl_rect)

        status = "Connecting to your robot..." if pygame.key.get_focused() else "Click this window to control your robot!"

        status_label = button_font.render(status, True, PLATINUM)
        status_rect = status_label.get_rect()
        status_rect.center = (width//2, 35)
        screen.blit(status_label, status_rect)

        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return
        pygame.display.flip()

        clock.tick(display_hz)

def main():
    parser = argparse.ArgumentParser(
        prog='Robot Controller',
        description='Allows you to control an ESP32 robot over Wi-Fi.'
    )

    parser.add_argument('-f', '--fps-limit', action='store', default=60, type=int, help="The maximum framerate to display in FPS. You can lower this if your monitor has a lower refresh rate.")
    parser.add_argument('-c', '--control-hz', action='store', default=60, type=int, help="Frequency at which packets are sent to the robot in Hz.")

    args = parser.parse_args()
    print(f"Framerate will be capped to {args.fps_limit} FPS.")
    print(f"Robot control message rate is {args.control_hz} Hz.")

    pygame.init()

    q = queue.Queue()
    keep_alive = threading.Event()
    keep_alive.set()
    ct = threading.Thread(target=control_thread, args=(q, args.control_hz, keep_alive), daemon=True)
    ct.start()
    display_thread(q, args.fps_limit)
    keep_alive.clear()
    ct.join()
    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
