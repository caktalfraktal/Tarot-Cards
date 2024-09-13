import tkinter as tk
from PIL import Image, ImageTk
import os
import random
from tarot_deck import tarot_deck
def draw_cards(num_cards):
    deck = tarot_deck.copy()
    random.SystemRandom().shuffle(deck)
    return deck[:num_cards]
def draw_celtic_cross(canvas_frame, text_box):
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    cards = draw_cards(10)
    images = []
    scaling_factor = 0.56
    for i, card in enumerate(cards):
        image_path = os.path.join(os.path.dirname(__file__), card['image'])
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize(
            (int(pil_image.width * scaling_factor), int(pil_image.height * scaling_factor)),
            Image.LANCZOS
        )
        if i == 1:
            pil_image = pil_image.rotate(90, expand=True)
        card_image = ImageTk.PhotoImage(pil_image)
        images.append(card_image)
    card_width = images[0].width()
    card_height = images[0].height()
    canvas_width = 700
    canvas_height = 800
    canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height)
    canvas.pack(padx=10, pady=10)
    center_x = canvas_width // 3
    center_y = canvas_height // 2 - card_height // 2
    spacing = 20
    horizontal_spacing = spacing * 3
    vertical_spacing_7_10 = -24
    positions = [
        (center_x, center_y),
        (
            center_x + (card_width - images[1].width()) // 2,
            center_y + (card_height - images[1].height()) // 2,
        ),
        (center_x, center_y + card_height + spacing),
        (center_x - card_width - horizontal_spacing, center_y),
        (center_x, center_y - card_height - spacing),
        (center_x + card_width + horizontal_spacing, center_y),
    ]
    x_offset = center_x + (card_width + horizontal_spacing) * 2
    y_offset = center_y + ((card_height + vertical_spacing_7_10) * 1.5)
    for i in range(6, 10):
        positions.append((x_offset, y_offset - (card_height + vertical_spacing_7_10) * (i - 6)))
    for i, (x, y) in enumerate(positions):
        canvas.create_image(x, y, image=images[i], anchor='nw')
    canvas.images = images
    positional_names = [
        "Present Situation (1)",
        "Challenges/Influences (2)",
        "Distant Past (3)",
        "Recent Past (4)",
        "Best Outcome (5)",
        "Immediate Future (6)",
        "Advice (7)",
        "Environment (8)",
        "Hopes or Fears (9)",
        "Potential Outcome (10)"
    ]
    card_meanings = "\n".join(
        [f"{positional_names[i]}:\n{cards[i]['name']} - {cards[i]['meaning']}\n" for i in range(10)]
    )
    text_box.config(state="normal")
    text_box.delete("1.0", tk.END)
    text_box.insert("1.0", card_meanings)
    text_box.config(state="disabled")
def draw_one_card(canvas_frame, text_box):
    for widget in canvas_frame.winfo_children():
        widget.destroy()
    cards = draw_cards(1)
    images = []
    scaling_factor = 1.055
    card = cards[0]
    image_path = os.path.join(os.path.dirname(__file__), card['image'])
    pil_image = Image.open(image_path)
    pil_image = pil_image.resize(
        (int(pil_image.width * scaling_factor), int(pil_image.height * scaling_factor)),
        Image.LANCZOS
    )
    card_image = ImageTk.PhotoImage(pil_image)
    images.append(card_image)
    canvas_width = 700
    canvas_height = 800
    canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height)
    canvas.pack(padx=10, pady=10)
    center_x = canvas_width // 3
    center_y = canvas_height // 2 - images[0].height() // 2
    positions = [
        (center_x, center_y),
    ]
    for i, (x, y) in enumerate(positions):
        canvas.create_image(x, y, image=images[i], anchor='nw')
    canvas.images = images
    positional_names = [
        "Card: "
    ]
    card_meanings = "\n".join(
        [f"{positional_names[i]}{cards[i]['name']}\n{cards[i]['meaning']}\n" for i in range(1)]
    )
    text_box.config(state="normal")
    text_box.delete("1.0", tk.END)
    text_box.insert("1.0", card_meanings)
    text_box.config(state="disabled")
def draw_three_cards(canvas_frame, text_box):
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    cards = draw_cards(3)
    images = []
    scaling_factor = 0.95
    for card in cards:
        image_path = os.path.join(os.path.dirname(__file__), card['image'])
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize(
            (int(pil_image.width * scaling_factor), int(pil_image.height * scaling_factor)),
            Image.LANCZOS
        )
        card_image = ImageTk.PhotoImage(pil_image)
        images.append(card_image)
    canvas_width = 700
    canvas_height = 800
    canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height)
    canvas.pack(padx=10, pady=10)
    center_x = canvas_width // 3
    center_y = canvas_height // 2 - images[0].height() // 2
    card_width = images[0].width()
    horizontal_spacing = 25
    positions = [
        (center_x - card_width - horizontal_spacing, center_y),
        (center_x, center_y),
        (center_x + card_width + horizontal_spacing, center_y)
    ]
    for i, (x, y) in enumerate(positions):
        canvas.create_image(x, y, image=images[i], anchor='nw')
    canvas.images = images
    positional_names = [
        "Card 1: ",
        "Card 2: ",
        "Card 3: "
    ]
    card_meanings = "\n".join(
        [f"{positional_names[i]}{cards[i]['name']}\n{cards[i]['meaning']}\n" for i in range(3)]
    )
    text_box.config(state="normal")
    text_box.delete("1.0", tk.END)
    text_box.insert("1.0", card_meanings)
    text_box.config(state="disabled")
def setup_main_gui(root, spread_type=None):
    window_width = 1275
    window_height = 825
    root.geometry(f"{window_width}x{window_height}")
    root.resizable(False, False)
    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)
    canvas_frame = tk.Frame(content_frame)
    canvas_frame.grid(row=0, column=0, rowspan=2, sticky="n")
    right_frame = tk.Frame(content_frame)
    right_frame.grid(row=0, column=1, sticky="n")
    vertical_padding = 100
    text_box = tk.Text(right_frame, wrap="word", height=30, width=55, font=("Courier New", 10))
    text_box.grid(row=0, column=0, padx=40, pady=(vertical_padding, 10), sticky="n")
    text_box.config(state="disabled")
    buttons_frame = tk.Frame(right_frame)
    buttons_frame.grid(row=1, column=0, padx=5, pady=(5, 10), sticky="n")
    draw_one_card_button = tk.Button(
        buttons_frame,
        text="Draw One Card",
        width=20,
        command=lambda: draw_one_card(canvas_frame, text_box)
    )
    draw_one_card_button.pack(pady=5)
    draw_three_cards_button = tk.Button(
        buttons_frame,
        text="Draw Three Cards",
        width=20,
        command=lambda: draw_three_cards(canvas_frame, text_box)
    )
    draw_three_cards_button.pack(pady=5)
    draw_celtic_button = tk.Button(
        buttons_frame,
        text="Draw Celtic Cross",
        width=20,
        command=lambda: draw_celtic_cross(canvas_frame, text_box)
    )
    draw_celtic_button.pack(pady=5)
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=0)
    if spread_type is None:
        add_placeholder(canvas_frame)
    else:
        if spread_type == "celtic":
            draw_celtic_cross(canvas_frame, text_box)
        elif spread_type == "one":
            draw_one_card(canvas_frame, text_box)
        elif spread_type == "three":
            draw_three_cards(canvas_frame, text_box)
def add_placeholder(canvas_frame):
    try:
        image_path = os.path.join(os.path.dirname(__file__), "Back.gif")
        pil_image = Image.open(image_path)
        scaling_factor = 1.055
        pil_image = pil_image.resize(
            (
                int(pil_image.width * scaling_factor),
                int(pil_image.height * scaling_factor)
            ),
            Image.LANCZOS
        )
        placeholder_image = ImageTk.PhotoImage(pil_image)
        canvas_width = 700
        canvas_height = 800
        canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height)
        canvas.pack(padx=10, pady=10)
        center_x = canvas_width // 3
        center_y = (canvas_height // 2) - (pil_image.height // 2)
        canvas.create_image(center_x, center_y, image=placeholder_image, anchor='nw')
        canvas.placeholder_image = placeholder_image
    except Exception as e:
        print(f"Error loading placeholder image: {e}")
def main():
    root = tk.Tk()
    root.title("Tarot Cards")
    setup_main_gui(root, spread_type=None)
    root.mainloop()
if __name__ == "__main__":
    main()