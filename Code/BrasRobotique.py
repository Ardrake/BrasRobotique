class MyRobot:
    def __init__(self, my_id):
        self.robot_id = my_id
        self.servo_list = []

    def add_servo(self, my_id, pos):
        my_servo = MyServo(my_id, pos)
        self.servo_list.append(my_servo)

    # routine de calibration des servos
    def calibrate_servos(self):
        pass

    # enregistré une séquence d'action
    def save_sequence(self):
        pass

    # recupere une séquence d'action a éxécuté
    def load_sequence(self):
        pass


class MyServo:
    def __init__(self, my_id, pos):
        self.id = my_id
        self.pos = pos