#!/usr/bin/env python3
import pygame
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
screen_width = 1366
screen_height = 768

# Set up the display in full-screen mode
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption("Speedometer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Font for numbers and labels
#font = pygame.font.SysFont(None, 30)
#font_path = "DejaVuSans.ttf"  # Replace with the actual path to your font file
#font = pygame.font.Font(font_path, 20)
font_path = "/home/orangepi/Symbola.ttf"  # Replace with the path to your Noto Emoji font file
font = pygame.font.Font(font_path, 30)
if font is None:
    print("Failed to load font!")
large_font = pygame.font.SysFont(font_path, 60)
odometer_font = pygame.font.SysFont(font_path, 40)
speed_font = pygame.font.SysFont(font_path, 80)  # Font for the speed readout

# Angle offset to adjust the starting point of the speedometer
angle_offset = 0  # Adjust to position 0 MPH as needed

def draw_high_beam_indicator(high_beam_on):
    if high_beam_on:
        # Draw the high beam indicator (blue circle with "H" in the middle)
        indicator_radius = 30
        pygame.draw.circle(screen, BLUE, (screen_width // 2, 50), indicator_radius)
        high_beam_text = large_font.render("H", True, WHITE)
        screen.blit(high_beam_text, (screen_width // 2 - high_beam_text.get_width() // 2, 50 - high_beam_text.get_height() // 2))

def draw_turn_signals(left_signal_on, right_signal_on):
    indicator_radius = 30  # Size of the indicator circles

    # Left turn signal indicator
    left_signal_color = GREEN if left_signal_on else WHITE
    pygame.draw.circle(screen, left_signal_color, (screen_width // 4, 50), indicator_radius)

    # Right turn signal indicator
    right_signal_color = GREEN if right_signal_on else WHITE
    pygame.draw.circle(screen, right_signal_color, (3 * screen_width // 4, 50), indicator_radius)


def draw_voltage_gauge(center, radius, voltage_level):
    # Check if voltage is too low or too high and set background color accordingly
    if voltage_level < 10 or voltage_level > 15:  # Change these thresholds as needed
        background_color = RED
    else:
        background_color = BLACK
    
    # Draw background circle
    pygame.draw.circle(screen, background_color, center, radius, 0)
    
    # Draw outer circle
    pygame.draw.circle(screen, WHITE, center, radius, 5)
    
    # Draw the "9", "14", and "19" labels
    voltage_labels = [9, 14, 19]
    label_angles = [135, 90, 45]  # Adjusted angles to make 14 at the top, 9 left, 19 right
    for i, voltage in enumerate(voltage_labels):
        voltage_label = font.render(str(voltage), True, WHITE)
        label_x = center[0] + (radius - 30) * math.cos(math.radians(label_angles[i]))
        label_y = center[1] - (radius - 30) * math.sin(math.radians(label_angles[i]))
        screen.blit(voltage_label, (label_x - voltage_label.get_width() // 2, label_y - voltage_label.get_height() // 2))
    
    # Draw battery icon in the middle
    voltage_icon = font.render("🔋", True, BLUE)
    screen.blit(voltage_icon, (center[0] - voltage_icon.get_width() // 2, center[1] - voltage_icon.get_height() // 2))
    
    # Draw ticks
    tick_length = 15
    tick_angles = [135, 120, 105, 90, 75, 60, 45]  # More angles for precise tick placement
    for angle in tick_angles:
        tick_x = center[0] + (radius - tick_length) * math.cos(math.radians(angle))
        tick_y = center[1] - (radius - tick_length) * math.sin(math.radians(angle))
        outer_x = center[0] + radius * math.cos(math.radians(angle))
        outer_y = center[1] - radius * math.sin(math.radians(angle))
        pygame.draw.line(screen, WHITE, (tick_x, tick_y), (outer_x, outer_y), 2)
    
    # Draw the needle (Dynamic based on voltage level)
    needle_length = radius - 30
    # Adjust the needle to move from 9 (135 degrees) to 19 (45 degrees)
    # Normalize voltage_level to [0, 1] where 0 is 9 and 1 is 19
    normalized_voltage = (voltage_level - 9) / (19 - 9)
    needle_angle = 135 - (normalized_voltage * 90)  # Move needle from 135 to 45 degrees
    needle_x = center[0] + needle_length * math.cos(math.radians(needle_angle))
    needle_y = center[1] - needle_length * math.sin(math.radians(needle_angle))
    pygame.draw.line(screen, WHITE, center, (needle_x, needle_y), 5)
    
    # Draw the current voltage level inside the gauge
    voltage_text = large_font.render(f"{voltage_level:.1f} V", True, YELLOW)
    # Position the text inside the circle below the needle
    screen.blit(voltage_text, (center[0] - voltage_text.get_width() // 2, center[1] + radius // 4))
def draw_oil_pressure_gauge(center, radius, oil_pressure):
    # Check if oil pressure is too low or too high and set background color accordingly
    if oil_pressure < 10 or oil_pressure > 70:  # Change these thresholds as needed
        background_color = RED
    else:
        background_color = BLACK
    
    # Draw background circle
    pygame.draw.circle(screen, background_color, center, radius, 0)
    
    # Draw outer circle
    pygame.draw.circle(screen, WHITE, center, radius, 5)
    
    # Draw the "0", "40", and "80" labels
    pressure_labels = [0, 40, 80]
    label_angles = [135, 90, 45]  # Adjusted angles to make 40 at the top, 0 left, 80 right
    for i, pressure in enumerate(pressure_labels):
        pressure_label = font.render(str(pressure), True, WHITE)
        label_x = center[0] + (radius - 30) * math.cos(math.radians(label_angles[i]))
        label_y = center[1] - (radius - 30) * math.sin(math.radians(label_angles[i]))
        screen.blit(pressure_label, (label_x - pressure_label.get_width() // 2, label_y - pressure_label.get_height() // 2))
    
    # Draw oil pressure icon in the middle
    oil_icon = font.render("🛢️", True, BLUE)
    screen.blit(oil_icon, (center[0] - oil_icon.get_width() // 2, center[1] - oil_icon.get_height() // 2))
    
    # Draw ticks
    tick_length = 15
    tick_angles = [135, 120, 105, 90, 75, 60, 45]  # More angles for precise tick placement
    for angle in tick_angles:
        tick_x = center[0] + (radius - tick_length) * math.cos(math.radians(angle))
        tick_y = center[1] - (radius - tick_length) * math.sin(math.radians(angle))
        outer_x = center[0] + radius * math.cos(math.radians(angle))
        outer_y = center[1] - radius * math.sin(math.radians(angle))
        pygame.draw.line(screen, WHITE, (tick_x, tick_y), (outer_x, outer_y), 2)
    
    # Draw the needle (Dynamic based on oil pressure level)
    needle_length = radius - 30
    # Adjust the needle to move from 0 (135 degrees) to 80 (45 degrees)
    # Normalize oil_pressure to [0, 1] where 0 is 0 and 1 is 80
    normalized_pressure = (oil_pressure - 0) / (80 - 0)
    needle_angle = 135 - (normalized_pressure * 90)  # Move needle from 135 to 45 degrees
    needle_x = center[0] + needle_length * math.cos(math.radians(needle_angle))
    needle_y = center[1] - needle_length * math.sin(math.radians(needle_angle))
    pygame.draw.line(screen, WHITE, center, (needle_x, needle_y), 5)
    
    # Draw the current oil pressure value inside the gauge
    pressure_text = large_font.render(f"{oil_pressure} PSI", True, YELLOW)
    # Position the text inside the circle below the needle
    screen.blit(pressure_text, (center[0] - pressure_text.get_width() // 2, center[1] + radius // 4))


def draw_temp_gauge(center, radius, temp_level):
    # Check if temperature is high and set background color accordingly
    if temp_level > 230:  # Change this threshold as needed
        background_color = RED
    else:
        background_color = BLACK
    
    # Draw background circle
    pygame.draw.circle(screen, background_color, center, radius, 0)
    
    # Draw outer circle
    pygame.draw.circle(screen, WHITE, center, radius, 5)
    
    # Draw the "100", "210", and "260" labels
    temp_labels = [100, 210, 260]
    label_angles = [135, 90, 45]  # Adjusted angles to make 210 at the top, 100 left, 260 right
    for i, temp in enumerate(temp_labels):
        temp_label = font.render(str(temp), True, WHITE)
        label_x = center[0] + (radius - 30) * math.cos(math.radians(label_angles[i]))
        label_y = center[1] - (radius - 30) * math.sin(math.radians(label_angles[i]))
        screen.blit(temp_label, (label_x - temp_label.get_width() // 2, label_y - temp_label.get_height() // 2))
    
    # Draw temperature icon in the middle
    temp_icon = font.render("🌡️", True, BLUE)
    screen.blit(temp_icon, (center[0] - temp_icon.get_width() // 2, center[1] - temp_icon.get_height() // 2))
    
    # Draw ticks
    tick_length = 15
    tick_angles = [135, 120, 105, 90, 75, 60, 45]  # More angles for precise tick placement
    for angle in tick_angles:
        tick_x = center[0] + (radius - tick_length) * math.cos(math.radians(angle))
        tick_y = center[1] - (radius - tick_length) * math.sin(math.radians(angle))
        outer_x = center[0] + radius * math.cos(math.radians(angle))
        outer_y = center[1] - radius * math.sin(math.radians(angle))
        pygame.draw.line(screen, WHITE, (tick_x, tick_y), (outer_x, outer_y), 2)
    
    # Draw the needle (Dynamic based on temperature level)
    needle_length = radius - 30
    # Adjust the needle to move from 100 (135 degrees) to 260 (45 degrees)
    # Normalize temp_level to [0, 1] where 0 is 100°F and 1 is 260°F
    normalized_temp = (temp_level - 100) / (260 - 100)
    needle_angle = 135 - (normalized_temp * 90)  # Move needle from 135 to 45 degrees
    needle_x = center[0] + needle_length * math.cos(math.radians(needle_angle))
    needle_y = center[1] - needle_length * math.sin(math.radians(needle_angle))
    pygame.draw.line(screen, WHITE, center, (needle_x, needle_y), 5)
    
    # Draw the current temperature value inside the gauge
    temp_text = large_font.render(f"{temp_level}°F", True, YELLOW)
    # Position the text slightly higher inside the circle below the needle
    screen.blit(temp_text, (center[0] - temp_text.get_width() // 2, center[1] + radius // 4))

def draw_fuel_gauge(center, radius, fuel_level):
    # Set background color based on fuel level
    if fuel_level < 0.15:  # Change this threshold as needed for low fuel
        background_color = RED
    else:
        background_color = BLACK

    # Draw background circle
    pygame.draw.circle(screen, background_color, center, radius, 0)
    
    # Draw outer circle
    pygame.draw.circle(screen, WHITE, center, radius, 5)
    
    # Draw the "E" and "F" labels
    e_label = font.render("E", True, WHITE)
    f_label = font.render("F", True, WHITE)
    screen.blit(e_label, (center[0] - radius + 10, center[1] - e_label.get_height() // 2))
    screen.blit(f_label, (center[0] + radius - f_label.get_width() - 10, center[1] - f_label.get_height() // 2))
    
    # Draw fuel pump icon in the middle
    fuel_icon = font.render("⛽", True, GREEN)
    screen.blit(fuel_icon, (center[0] - fuel_icon.get_width() // 2, center[1] - fuel_icon.get_height() // 2))
    
    # Draw ticks
    tick_length = 15
    for i in range(5):
        angle = (i - 2) * 30 + 92  # Adjust the angle to position the ticks evenly
        tick_x = center[0] + (radius - tick_length) * math.cos(math.radians(angle))
        tick_y = center[1] - (radius - tick_length) * math.sin(math.radians(angle))
        outer_x = center[0] + radius * math.cos(math.radians(angle))
        outer_y = center[1] - radius * math.sin(math.radians(angle))
        pygame.draw.line(screen, WHITE, (tick_x, tick_y), (outer_x, outer_y), 2)
    
    # Draw the needle (Dynamic based on fuel level)
    needle_length = radius - 30
    # Full is 0 degrees, Empty is 180 degrees
    needle_angle = (1 - fuel_level) * 180  # 1.0 = Full, 0.0 = Empty
    needle_x = center[0] + needle_length * math.cos(math.radians(needle_angle))
    needle_y = center[1] - needle_length * math.sin(math.radians(needle_angle))
    pygame.draw.line(screen, WHITE, center, (needle_x, needle_y), 5)
    
    # Draw the current fuel level inside the gauge
    fuel_text = large_font.render(f"{int(fuel_level * 100)}%", True, YELLOW)
    # Position the text inside the circle below the fuel pump icon
    screen.blit(fuel_text, (center[0] - fuel_text.get_width() // 2, center[1] + radius // 4))


# Function to draw the speedometer
def draw_speedometer(center, radius, speed, max_speed):
    # Draw outer circle
    pygame.draw.circle(screen, WHITE, center, radius, 5)
    
    # Angle range to expand the numbers and ticks (e.g., 240 degrees instead of 180)
    angle_range = 240  # Adjust this to control how much of the circle the gauge covers
    
    # Draw speedometer numbers and ticks (Static)
    for i in range(0, max_speed + 1, 10):
        # Adjust the angle calculation to use the new angle range
        angle = (1 - i / max_speed) * angle_range - (angle_range // 2) + angle_offset
        inner_tick_length = 15
        outer_tick_length = 25
        tick_color = WHITE

        # Coordinates for inner and outer ticks
        inner_x = center[0] + (radius - inner_tick_length) * math.cos(math.radians(angle + 90))
        inner_y = center[1] - (radius - inner_tick_length) * math.sin(math.radians(angle + 90))
        outer_x = center[0] + radius * math.cos(math.radians(angle + 90))
        outer_y = center[1] - radius * math.sin(math.radians(angle + 90))
        
        # Draw the main tick
        pygame.draw.line(screen, tick_color, (inner_x, inner_y), (outer_x, outer_y), 2)
        
        # Draw speedometer numbers
        number_x = center[0] + (radius - 40) * math.cos(math.radians(angle + 90))
        number_y = center[1] - (radius - 40) * math.sin(math.radians(angle + 90))
        number_text = font.render(str(i), True, WHITE)
        screen.blit(number_text, (number_x - number_text.get_width() // 2, number_y - number_text.get_height() // 2))
    
    # Draw 5 MPH ticks between the numbers (Static)
    for i in range(5, max_speed + 1, 10):
        angle = (1 - i / max_speed) * angle_range - (angle_range // 2) + angle_offset
        inner_tick_length = 20
        outer_tick_length = 15

        # Coordinates for 5 MPH ticks
        inner_x = center[0] + (radius - outer_tick_length) * math.cos(math.radians(angle + 90))
        inner_y = center[1] - (radius - outer_tick_length) * math.sin(math.radians(angle + 90))
        outer_x = center[0] + (radius - 5) * math.cos(math.radians(angle + 90))
        outer_y = center[1] - (radius - 5) * math.sin(math.radians(angle + 90))
        
        # Draw the 5 MPH tick
        pygame.draw.line(screen, WHITE, (inner_x, inner_y), (outer_x, outer_y), 2)
    
    # Draw the needle (Dynamic based on actual speed)
    needle_length = radius - 40
    # Adjust the needle angle to use the expanded angle range
    dynamic_max_speed = max_speed * 2.5  # Allow needle to go beyond 85 MPH
    needle_angle = (1 - (speed % dynamic_max_speed) / max_speed) * angle_range - (angle_range // 2) + angle_offset
    needle_x = center[0] + needle_length * math.cos(math.radians(needle_angle + 90))
    needle_y = center[1] - needle_length * math.sin(math.radians(needle_angle + 90))
    pygame.draw.line(screen, WHITE, center, (needle_x, needle_y), 5)
    
    # Draw speed readout just above the needle center
    speed_readout = speed_font.render(str(int(speed)), True, YELLOW)
    # Positioning the speed readout just above the center of the speedometer
    screen.blit(speed_readout, (center[0] - speed_readout.get_width() // 2, center[1] - speed_readout.get_height() - 20))
    
    # Draw odometer
    odometer_value = "355892"
    trip_value = "0746"
    odometer_text = odometer_font.render(odometer_value, True, ORANGE)
    trip_text = font.render(trip_value, True, ORANGE)
    screen.blit(odometer_text, (center[0] - odometer_text.get_width() // 2, center[1] + 70))
    screen.blit(trip_text, (center[0] - trip_text.get_width() // 2, center[1] + 110))

# Function to draw the tachometer
def draw_tachometer(center, radius, rpm, max_rpm):
    # Draw outer circle
    pygame.draw.circle(screen, WHITE, center, radius, 5)
    
    # Angle range to expand the numbers and ticks (e.g., 240 degrees instead of 180)
    angle_range = 240  # Adjust this to control how much of the circle the gauge covers
    
    # Draw tachometer numbers and ticks (Static)
    for i in range(0, max_rpm + 1, 1000):
        # Adjust the angle calculation to use the new angle range
        angle = (1 - i / max_rpm) * angle_range - (angle_range // 2) + angle_offset
        inner_tick_length = 15
        outer_tick_length = 25
        tick_color = WHITE

        # Coordinates for inner and outer ticks
        inner_x = center[0] + (radius - inner_tick_length) * math.cos(math.radians(angle + 90))
        inner_y = center[1] - (radius - inner_tick_length) * math.sin(math.radians(angle + 90))
        outer_x = center[0] + radius * math.cos(math.radians(angle + 90))
        outer_y = center[1] - radius * math.sin(math.radians(angle + 90))
        
        # Draw the main tick
        pygame.draw.line(screen, tick_color, (inner_x, inner_y), (outer_x, outer_y), 2)
        
        # Draw tachometer numbers
        number_x = center[0] + (radius - 40) * math.cos(math.radians(angle + 90))
        number_y = center[1] - (radius - 40) * math.sin(math.radians(angle + 90))
        number_text = font.render(str(i // 1000), True, WHITE)  # Divide by 1000 to display RPM as x1000
        screen.blit(number_text, (number_x - number_text.get_width() // 2, number_y - number_text.get_height() // 2))
    
    # Draw 500 RPM ticks between the numbers (Static)
    for i in range(500, max_rpm + 1, 1000):
        # Adjust the angle calculation to use the new angle range
        angle = (1 - i / max_rpm) * angle_range - (angle_range // 2) + angle_offset
        inner_tick_length = 20
        outer_tick_length = 15

        # Coordinates for 500 RPM ticks
        inner_x = center[0] + (radius - outer_tick_length) * math.cos(math.radians(angle + 90))
        inner_y = center[1] - (radius - outer_tick_length) * math.sin(math.radians(angle + 90))
        outer_x = center[0] + (radius - 5) * math.cos(math.radians(angle + 90))
        outer_y = center[1] - (radius - 5) * math.sin(math.radians(angle + 90))
        
        # Draw the 500 RPM tick
        pygame.draw.line(screen, WHITE, (inner_x, inner_y), (outer_x, outer_y), 2)
    
    # Draw the needle (Dynamic based on actual RPM)
    needle_length = radius - 40
    # Correct the needle angle calculation using the expanded angle range
    needle_angle = (1 - (rpm / max_rpm)) * angle_range - (angle_range // 2) + angle_offset
    needle_x = center[0] + needle_length * math.cos(math.radians(needle_angle + 90))
    needle_y = center[1] - needle_length * math.sin(math.radians(needle_angle + 90))
    pygame.draw.line(screen, WHITE, center, (needle_x, needle_y), 5)
    
    # Draw RPM readout just above the needle center
    rpm_readout = speed_font.render(str(int(rpm)), True, YELLOW)
    # Positioning the RPM readout just above the center of the tachometer
    screen.blit(rpm_readout, (center[0] - rpm_readout.get_width() // 2, center[1] - rpm_readout.get_height() - 20))
    
    # Draw tachometer label inside the circle
    label_text = font.render("RPM x1000", True, ORANGE)
    screen.blit(label_text, (center[0] - label_text.get_width() // 2, center[1] + 70))



# Main loop
running = True
speed = 0
rpm = 0
fuel_level = 1.0
max_speed = 85  # This is the maximum static speed for drawing the ticks and numbers
oil_pressure = 0
max_rpm = 8000
temp_level = 100
voltage_level = 9
left_signal_on = False
right_signal_on = False
signal_blink_counter = 0  # Counter for blinking turn signals
signal_duration = 60
high_beam_on = False
high_beam_counter = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            # Exit on ESC key press
            running = False
    
    # Clear screen
    screen.fill(BLACK)

    # Draw turn signal indicators
    signal_blink_counter += 1
    if signal_blink_counter >= signal_duration * 2:  # Reset counter after one full cycle
        signal_blink_counter = 0
    # Alternate between left and right signals
    left_signal_on = signal_blink_counter < signal_duration
    right_signal_on = not left_signal_on

    high_beam_counter += 1
    if high_beam_counter >= 60:  # Adjust blinking speed here
        high_beam_counter = 0
    high_beam_on = high_beam_counter < 30  # Flash on for 30 frames, off for 30 frames
    
    # Draw high beam indicator
    draw_high_beam_indicator(high_beam_on)

    # Blinking effect (on for 10 frames, off for 5 frames)
    blink_on = (signal_blink_counter % 15) < 10
    
    # Draw the turn signals with blinking effect
    draw_turn_signals(left_signal_on and blink_on, right_signal_on and blink_on)

    draw_fuel_gauge((screen_width // 8, screen_height // 6), 100, fuel_level)

    # Draw speedometer
    draw_speedometer((screen_width // 3, screen_height // 2), 200, speed, max_speed)

    draw_tachometer((2 * screen_width // 3, screen_height // 2), 200, rpm, max_rpm)

    draw_temp_gauge((screen_width // 8, 4 * screen_height // 5), 100, temp_level)

    draw_oil_pressure_gauge((7 * screen_width // 8, screen_height // 6), 100, oil_pressure)

    draw_voltage_gauge((7 * screen_width // 8, 4 * screen_height // 5), 100, voltage_level)

    # Update speed for demo (replace with actual speed data)
    speed = (speed + 1) % (int(max_speed * 2.5) + 1)  # Increment speed, loop back to 0 after exceeding max_speed

    rpm = (rpm + 100) % (max_rpm + 1)
    fuel_level -= 0.001  # Decrease fuel level gradually
    if fuel_level < 0:
        fuel_level = 1.0  # Stop at empty

    temp_level += 1
    if temp_level > 260:
        temp_level = 100

    oil_pressure += 0.5
    if oil_pressure > 80 or oil_pressure < 0:
        oil_pressure = 0

    voltage_level += 0.1
    if voltage_level > 19 or voltage_level < 0:
        voltage_level = 9

    # Update display
    pygame.display.flip()
    
    # Control frame rate
    clock.tick(30)

pygame.quit()
