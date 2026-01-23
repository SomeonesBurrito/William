from PyQt5 import QtWidgets, QtGui, QtCore
import random, sys, math, time


class CircularWaveVisualizer(QtWidgets.QWidget):
    def __init__(self, scale_factor=1.0, parent=None):
        super().__init__(parent)
        self.scale_factor = scale_factor

        # Scaled properties
        self.wave_thickness = int(5 * self.scale_factor)
        self.wave_speed = 0.02
        self.wave_amplitude = 20 * self.scale_factor
        self.wave_count = 12
        self.wave_length = 0.3
        self.wave_base_radius = 190 * self.scale_factor
        self.inner_radius = int(self.wave_base_radius * 0.96)
        self.inner_border_width = int(4 * self.scale_factor)

        # Colours
        self.wave_colors = [
            QtGui.QColor(0, 150, 220, 220),
            QtGui.QColor(160, 0, 220, 220),
            QtGui.QColor(0, 180, 160, 220),
            QtGui.QColor(200, 100, 0, 220),
            QtGui.QColor(160, 160, 0, 220),
            QtGui.QColor(0, 120, 200, 220),
            QtGui.QColor(180, 0, 140, 220),
            QtGui.QColor(60, 140, 100, 220),
        ]
        self.current_colors = self.wave_colors.copy()
        self.target_colors = self.wave_colors.copy()
        self.color_transition_speed = 0.015

        # Animation properties
        self.angle = 0
        self.time = 0
        self.layer_change_counter = 0
        self.layer_change_interval = 90
        self.z_layers = list(range(self.wave_count))
        self.waves_visible = True

        # Generate wave data
        self.waves = []
        for i in range(self.wave_count):
            self.waves.append({
                "phase_offset": random.uniform(0, 6.28),
                "amplitude_mod": random.uniform(0.7, 1.3),
                "speed_mod": random.uniform(0.7, 1.3),
                "thickness_mod": random.uniform(0.7, 1.3),
                "color_idx": i % len(self.wave_colors),
                "wave_radius_offset": random.uniform(-5, 5) * self.scale_factor
            })

        # Timer
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.animate)
        self.timer.start(30)

    def animate(self):
        self.angle += self.wave_speed
        self.time += 0.04
        self.layer_change_counter += 1

        self.update_color_transitions()
        self.update_layer_transitions()
        self.update()

    def toggle_waves(self):
        self.waves_visible = not self.waves_visible
        self.update()

    def update_color_transitions(self):
        for i in range(len(self.current_colors)):
            current = self.current_colors[i]
            target = self.target_colors[i]
            new_r = current.red() + (target.red() - current.red()) * self.color_transition_speed
            new_g = current.green() + (target.green() - current.green()) * self.color_transition_speed
            new_b = current.blue() + (target.blue() - current.blue()) * self.color_transition_speed
            new_a = current.alpha() + (target.alpha() - current.alpha()) * self.color_transition_speed
            self.current_colors[i] = QtGui.QColor(int(new_r), int(new_g), int(new_b), int(new_a))

    def update_layer_transitions(self):
        if self.layer_change_counter >= self.layer_change_interval:
            self.layer_change_counter = 0
            if random.random() < 0.8:
                i = random.randint(0, self.wave_count - 2)
                self.z_layers[i], self.z_layers[i + 1] = self.z_layers[i + 1], self.z_layers[i]

    def paintEvent(self, event):
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        w, h = self.width(), self.height()
        cx, cy = w / 2, h / 2

        if self.waves_visible:
            self.draw_waves(painter, cx, cy)
        self.draw_inner_circle(painter, cx, cy)

    def draw_inner_circle(self, painter, cx, cy):
        pen = QtGui.QPen(QtGui.QColor(0, 180, 255, 200), self.inner_border_width)
        painter.setPen(pen)
        painter.setBrush(QtGui.QColor(20, 25, 35))
        painter.drawEllipse(QtCore.QPointF(cx, cy), self.inner_radius, self.inner_radius)

    def draw_waves(self, painter, cx, cy):
        points_per_wave = 120
        for z_index in self.z_layers:
            wave_data = self.waves[z_index]
            wave_color = self.current_colors[wave_data["color_idx"]]
            wave_points = []
            base_phase = self.angle * wave_data["speed_mod"]

            for i in range(points_per_wave):
                angle_around = 2 * math.pi * (i / points_per_wave)
                total_angle = angle_around + (z_index * 2 * math.pi / self.wave_count)
                wave_value = math.sin(base_phase + angle_around * self.wave_length + wave_data["phase_offset"]) * wave_data["amplitude_mod"]
                wave_radius = self.wave_base_radius + wave_data["wave_radius_offset"] + wave_value * self.wave_amplitude
                x = cx + wave_radius * math.cos(total_angle)
                y = cy + wave_radius * math.sin(total_angle)
                wave_points.append(QtCore.QPointF(x, y))

            pen = QtGui.QPen(wave_color, self.wave_thickness * wave_data["thickness_mod"])
            pen.setCapStyle(QtCore.Qt.RoundCap)
            painter.setPen(pen)
            path = QtGui.QPainterPath()
            if wave_points:
                path.moveTo(wave_points[0])
                for pt in wave_points[1:]:
                    path.lineTo(pt)
                path.closeSubpath()
            painter.drawPath(path)


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        screen = QtWidgets.QApplication.primaryScreen()
        screen_geometry = screen.availableGeometry()
        self.scale_x = screen_geometry.width() / 3840
        self.scale_y = screen_geometry.height() / 2160
        self.scale_factor = min(self.scale_x, self.scale_y) * 1.4

        # Window setup
        self.setFixedSize(int(2100 * self.scale_factor), int(1175 * self.scale_factor))
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        # Background
        central = QtWidgets.QWidget()
        central.setStyleSheet(f"""
            background-color: rgba(30, 35, 45, 255);
            border-radius: {int(20 * self.scale_factor)}px;
            border: {int(3 * self.scale_factor)}px solid rgba(80, 90, 110, 180);
        """)
        self.setCentralWidget(central)

        layout = QtWidgets.QVBoxLayout(central)
        layout.setAlignment(QtCore.Qt.AlignCenter)
        layout.setContentsMargins(int(50 * self.scale_factor), int(50 * self.scale_factor),
                                  int(50 * self.scale_factor), int(50 * self.scale_factor))

        # Wave visualiser
        self.visualizer = CircularWaveVisualizer(self.scale_factor)
        size = int(900 * self.scale_factor)
        self.visualizer.setFixedSize(size, size)
        layout.addWidget(self.visualizer)

        # Time display
        self.time_frame = QtWidgets.QFrame(central)
        self.time_frame.setGeometry(
            int(52 * self.scale_factor),
            int(50 * self.scale_factor),
            int(210 * self.scale_factor),
            int(50 * self.scale_factor)
        )
        self.time_frame.setStyleSheet(f"""
            background-color: black;
            border-radius: {int(24 * self.scale_factor)}px;
        """)

        self.time_label = QtWidgets.QLabel(self.time_frame)
        self.time_label.setFont(QtGui.QFont("Verdana", int(16 * self.scale_factor), QtGui.QFont.Bold))
        self.time_label.setAlignment(QtCore.Qt.AlignCenter)
        self.time_label.setGeometry(
            int(6 * self.scale_factor),
            int(6 * self.scale_factor),
            int(205 * self.scale_factor),
            int(38 * self.scale_factor)
        )
        self.time_label.setStyleSheet("color: white; background: transparent; border: none;")

        # Neon rotating border effect using QConicalGradient
        self.border_angle = 0
        self.neon_timer = QtCore.QTimer(self)
        self.neon_timer.timeout.connect(self.update_neon_border)
        self.neon_timer.start(50)

        # Timer for live clock
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()

        # Centre window
        self.center_on_screen()
        self.show()

    def update_neon_border(self):
        self.border_angle = (self.border_angle + 4) % 360

        gradient = QtGui.QConicalGradient(self.time_frame.rect().center(), self.border_angle)
        gradient.setColorAt(0.0, QtGui.QColor(0, 200, 255))
        gradient.setColorAt(0.5, QtGui.QColor(180, 0, 255))
        gradient.setColorAt(1.0, QtGui.QColor(0, 200, 255))
        brush = QtGui.QBrush(gradient)

        # Create a pixmap for border effect
        size = self.time_frame.size()
        pixmap = QtGui.QPixmap(size)
        pixmap.fill(QtCore.Qt.transparent)

        painter = QtGui.QPainter(pixmap)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        pen = QtGui.QPen(brush, int(8 * self.scale_factor))
        painter.setPen(pen)
        painter.drawRoundedRect(
            pixmap.rect().adjusted(2, 2, -2, -2),
            int(24 * self.scale_factor),
            int(24 * self.scale_factor)
        )
        painter.end()

        # Apply as border image
        self.time_frame.setStyleSheet(f"""
            background-color: black;
            border-radius: {int(24 * self.scale_factor)}px;
        """)
        palette = self.time_frame.palette()
        palette.setBrush(QtGui.QPalette.Window, QtGui.QBrush(pixmap))
        self.time_frame.setAutoFillBackground(True)
        self.time_frame.setPalette(palette)

    def update_time(self):
        current_time = time.strftime("%I:%M %p")
        self.time_label.setText(current_time)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Space:
            self.visualizer.toggle_waves()

    def center_on_screen(self):
        screen = QtWidgets.QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
