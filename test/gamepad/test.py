import sys
import pygame
from pygame.locals import *
import paho.mqtt.client as mqtt

#MQTT setup
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "gamepad/button"

client = mqtt.Client()
try:
    client.connect(MQTT_BROKER, MQTT_PORT,60)
    client.loop_start()
except Exception as e:
    print(f"MQTT connection failed: {e}")
# Initialize Pygame
pygame.init()

# Set up gamepad
pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]

if not joysticks:
    print("No gamepad detected!")
    sys.exit()

joystick = joysticks[0]
joystick.init()

print(f"Detected gamepad: {joystick.get_name()}")
print("Press buttons or move axes. Press ESC to quit.")

# Button mapping
BUTTON_NAMES = {
    0: "BACKWARD",
    1: "FORWARD",
    2: "LEFT",
    3: "RIGHT"
}

# Main loop
try:
    while True:
        for event in pygame.event.get():
            # Handle gamepad events
            #Press
            if event.type == JOYBUTTONDOWN:
                print(f"Button {event.button} pressed - {BUTTON_NAMES.get(event.button, 'Unknown')}")
                message = f"Button {event.button} pressed"
                client.publish(MQTT_TOPIC, message)
            #release    
            elif event.type == JOYBUTTONUP:
                print(f"Button {event.button} released - {BUTTON_NAMES.get(event.button, 'Unknown')}")

            #Code to read the controller    
            #elif event.type == JOYAXISMOTION:
                #if abs(event.value) > 0.1:
                 #   print(f"Axis {event.axis} moved: {event.value:.2f}")


            # Handle keyboard exit
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                    
            # Handle window close
            elif event.type == QUIT:
                pygame.quit()
                sys.exit()
            

        # Small delay to prevent high CPU usage
        pygame.time.wait(50)

except KeyboardInterrupt:
    pygame.quit()
    client.loop_stop()
    client.disconnect()
    print("\nExiting cleanly...")
