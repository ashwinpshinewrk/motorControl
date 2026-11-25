# Motor Sim
A simple motor behaviour done on ROS 2 with Lag filter.

## Architecture

```
teleop_twsit_keyboard -> /cmd_vel -> /motor_sim/motor_target_rpm -> /motor_sim/telemetry_string & /motor_sim/telemetry_data
```

## Working
### Velocity to RPM.
Input is captured from teleop_twist_keyboard as controller. This data is then convereted to velocity of a differential-drive system.

Equations used are:
$$v_l = v - \frac{w1}{2}$$
$$v_r = v + \frac{w1}{2}$$

for converting veloctiy to RPM:

$$RPM  = v * \frac{60}{2\pi}$$

### Motor Response
The lag formula is used to simulate how fast should the motor change. The instantanoues values of RPM can't be used as the sudden change brings high current in the motor and damange it.

Lag formula:

$$value_{new} = value_{old} + \alpha (target - value_{old}) $$

Where $\alpha$ is used as a smoothing factor.

## Building

```bash
colcon build 
source install/setup.bash
ros2 launch motor_sim motor_sim.launch.py
```

In another terminal,
```bash
source install/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

In one more terminal,
```bash
source install/setup.bash
ros2 topic echo /motor_sim/telemetry_string
```

## Expected behaviour
When you press the keys i, l, j ,m ,n, u,., , you are controlling the robot and the screen should give you a reading of what current RPM of the motor should be.

## Assumption
- It is diff-drive system. Wheels modeled as thrusters.
- No external factors such as drag.
