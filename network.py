import socket
import pickle


class Network:
    def __init__(self, player, HOST, user_type="CLIENT", PORT=5555):
        self.player = player
        self.type = user_type
        self.HOST = HOST
        self.PORT = PORT
        self.new_connection()



    def new_connection(self):
        if self.type == "SERVER":
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.bind((self.HOST, self.PORT))
            s.listen()
            while True:
                print("Ожидание подключения")
                self.client_s, addr = s.accept()
                print(f"Соединение установлено с {addr}")
                break
        elif self.type == "CLIENT":
            self.client_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_s.connect((self.HOST, self.PORT))
            print("Соединение установлено")
        else:
            raise Exception("Invalid user type")

    def shot_mechanics(self):
        if not self.player.shot:
            return True

        x1, y1 = self.player.pos
        x2, y2 = self.player.x2, self.player.y2
        dx, dy = x2 - x1, y2 - y1

        angle = self.player.angle
        cos_a = self.player.table_cos[angle]
        sin_a = self.player.table_sin[angle]


        player_depth = dx * cos_a + dy * sin_a # проекция
        if player_depth <= 0:
            return True  # Цель сзади => попадания нет

        distance_from_center = abs(dx * sin_a - dy * cos_a) # растояние от центра противника до линии выстрела

        player_radius = 0.3
        if distance_from_center < player_radius:
            return False
        return True

    def update(self):
        self.client_s.sendall(pickle.dumps((self.player.pos, self.shot_mechanics(), self.player.life)))
        data = pickle.loads(self.client_s.recv(512))
        if data:
            self.player.set_coords_to_2(data[0])
            if self.player.life: self.player.life = data[1]
            self.player.life2 = data[2]
