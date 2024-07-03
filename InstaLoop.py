import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import screeninfo


class InstaLoop:
    def __init__(self, root):
        self.root = root
        self.root.title("InstaLoop")
        self.root.geometry("600x400")
        self.root.configure(bg="#2C3E50")

        self.video_files = []

        style = ttk.Style()
        style.configure("TButton", font=("Helvetica", 12), padding=10, background="#ECF0F1")
        style.configure("TLabel", font=("Helvetica", 14), background="#2C3E50", foreground="#ECF0F1")
        style.configure("Treeview", font=("Helvetica", 12), background="#ECF0F1", fieldbackground="#ECF0F1",
                        foreground="#2C3E50")
        style.configure("Treeview.Heading", font=("Helvetica", 14, "bold"), background="#34495E", foreground="#ECF0F1")
        style.map('TButton', background=[('active', '#34495E')])
        style.map('Treeview.Heading', background=[('active', '#34495E')])  # Prevents changing color on hover

        self.label = ttk.Label(root, text="Select and Play Videos")
        self.label.pack(pady=20)

        self.select_button = ttk.Button(root, text="Select Videos", command=self.select_videos)
        self.select_button.pack(pady=10)

        self.play_button = ttk.Button(root, text="Play Videos", command=self.play_videos)
        self.play_button.pack(pady=10)

        self.esc_label = ttk.Label(root, text="Press 'Esc' key to exit the player", foreground="#ECF0F1", font=("Helvetica", 12))
        self.esc_label.pack(pady=5)

        self.tree = ttk.Treeview(root, columns=("File Path",), show='headings')
        self.tree.heading("File Path", text="Selected Videos")
        self.tree.pack(pady=20, fill=tk.BOTH, expand=True)

    def select_videos(self):
        self.video_files = filedialog.askopenfilenames(filetypes=[("Video files", "*.mp4 *.avi *.mkv")])
        self.update_video_list()

    def update_video_list(self):
        self.tree.delete(*self.tree.get_children())
        for video in self.video_files:
            self.tree.insert("", tk.END, values=(video,))

    def play_videos(self):
        if not self.video_files:
            messagebox.showerror("Error", "No videos selected. Please select video files to play.")
            return

        screen = screeninfo.get_monitors()[0]
        screen_width, screen_height = screen.width, screen.height

        while True:
            for video_file in self.video_files:
                cap = cv2.VideoCapture(video_file)
                cv2.namedWindow("InstaLoopPlayer", cv2.WND_PROP_FULLSCREEN)
                cv2.setWindowProperty("InstaLoopPlayer", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        break

                    # Resize the frame to fit the screen
                    frame = cv2.resize(frame, (screen_width, screen_height))
                    cv2.imshow("InstaLoopPlayer", frame)
                    if cv2.waitKey(25) & 0xFF == 27:  # Check for 'Esc' key
                        cap.release()
                        cv2.destroyAllWindows()
                        return

                cap.release()

        cv2.destroyAllWindows()


if __name__ == "__main__":
    root = tk.Tk()
    app = InstaLoop(root)
    root.mainloop()
