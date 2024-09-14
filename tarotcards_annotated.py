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
    # Clear previous content in canvas_frame
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    cards = draw_cards(10)
    images = []
    scaling_factor = 0.56  # Reduce size to ensure all cards fit

    # Load images, resize them, and handle rotation for the crossing card
    for i, card in enumerate(cards):
        image_path = os.path.join(os.path.dirname(__file__), card['image'])
        pil_image = Image.open(image_path)

        # Resize images
        pil_image = pil_image.resize(
            (int(pil_image.width * scaling_factor), int(pil_image.height * scaling_factor)),
            Image.LANCZOS
        )

        if i == 1:
            pil_image = pil_image.rotate(90, expand=True)
        card_image = ImageTk.PhotoImage(pil_image)
        images.append(card_image)

    # Update card dimensions after resizing
    card_width = images[0].width()
    card_height = images[0].height()

    # Create a canvas to position the cards with fixed size
    canvas_width = 700
    canvas_height = 800
    canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height)
    canvas.pack(padx=10, pady=10)

    # Center coordinates for the cross
    center_x = canvas_width // 3
    center_y = canvas_height // 2 - card_height // 2

    # Spacing adjustments
    spacing = 20
    horizontal_spacing = spacing * 3
    vertical_spacing_7_10 = -24

    # Positions for the Celtic Cross layout
    positions = [
        (center_x, center_y),  # Card 1
        (
            center_x + (card_width - images[1].width()) // 2,
            center_y + (card_height - images[1].height()) // 2,
        ),  # Card 2
        (center_x, center_y + card_height + spacing),  # Card 3
        (center_x - card_width - horizontal_spacing, center_y),  # Card 4
        (center_x, center_y - card_height - spacing),  # Card 5
        (center_x + card_width + horizontal_spacing, center_y),  # Card 6
    ]

    # Positions for cards 7 to 10 (vertical line to the right)
    x_offset = center_x + (card_width + horizontal_spacing) * 2
    y_offset = center_y + ((card_height + vertical_spacing_7_10) * 1.5)

    for i in range(6, 10):
        positions.append((x_offset, y_offset - (card_height + vertical_spacing_7_10) * (i - 6)))

    # Draw the cards on the canvas
    for i, (x, y) in enumerate(positions):
        canvas.create_image(x, y, image=images[i], anchor='nw')

    # Keep a reference to prevent garbage collection
    canvas.images = images

    # Define the traditional Celtic Cross position names with card numbers
    positional_names = [
        "Present Situation (1)",
        "Challenges or Influences (2)",
        "Distant Past (3)",
        "Recent Past (4)",
        "Best Outcome (5)",
        "Immediate Future (6)",
        "Advice (7)",
        "Environment (8)",
        "Hopes or Fears (9)",
        "Potential Outcome (10)"
    ]

    # Display card meanings on the right side with positional names
    card_meanings = "\n".join(
        [f"{positional_names[i]}:\n{cards[i]['name']} - {cards[i]['meaning']}\n" for i in range(10)]
    )

    # Update the text box with the card meanings
    text_box.config(state="normal")  # Enable editing
    text_box.delete("1.0", tk.END)  # Clear previous content
    text_box.insert("1.0", card_meanings)
    text_box.config(state="disabled")  # Make the text read-only

def draw_one_card(canvas_frame, text_box):
    # Clear previous content in canvas_frame
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    cards = draw_cards(1)
    images = []
    scaling_factor = 1.055  # Draw One Card scaling factor

    # Load and resize the single card image
    card = cards[0]
    image_path = os.path.join(os.path.dirname(__file__), card['image'])
    pil_image = Image.open(image_path)
    pil_image = pil_image.resize(
        (int(pil_image.width * scaling_factor), int(pil_image.height * scaling_factor)),
        Image.LANCZOS
    )
    card_image = ImageTk.PhotoImage(pil_image)
    images.append(card_image)

    # Create a canvas to position the card with fixed size
    canvas_width = 700
    canvas_height = 800
    canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height)
    canvas.pack(padx=10, pady=10)

    # Center coordinates for Card 1 position in Celtic Cross
    center_x = canvas_width // 3
    center_y = canvas_height // 2 - images[0].height() // 2

    # Position for the single card (same as Card 1 in Celtic Cross)
    positions = [
        (center_x, center_y),  # Card 1
    ]

    # Draw the single card on the canvas
    for i, (x, y) in enumerate(positions):
        canvas.create_image(x, y, image=images[i], anchor='nw')

    # Keep a reference to prevent garbage collection
    canvas.images = images

    # Define the positional name for the single card
    positional_names = [
        "Card: "
    ]

    # Display card meanings in the text box
    card_meanings = "\n".join(
        [f"{positional_names[i]}{cards[i]['name']}\n{cards[i]['meaning']}\n" for i in range(1)]
    )

    text_box.config(state="normal")  # Enable editing
    text_box.delete("1.0", tk.END)  # Clear previous content
    text_box.insert("1.0", card_meanings)
    text_box.config(state="disabled")  # Make the text read-only

def draw_three_cards(canvas_frame, text_box):
    # Clear previous content in canvas_frame
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    cards = draw_cards(3)
    images = []
    scaling_factor = 0.95  # Draw 3 cards scaling factor

    # Load and resize the three card images
    for card in cards:
        image_path = os.path.join(os.path.dirname(__file__), card['image'])
        pil_image = Image.open(image_path)
        pil_image = pil_image.resize(
            (int(pil_image.width * scaling_factor), int(pil_image.height * scaling_factor)),
            Image.LANCZOS
        )
        card_image = ImageTk.PhotoImage(pil_image)
        images.append(card_image)

    # Create a canvas to position the cards with fixed size
    canvas_width = 700
    canvas_height = 800
    canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height)
    canvas.pack(padx=10, pady=10)

    # Calculate positions based on Celtic Cross layout
    center_x = canvas_width // 3
    center_y = canvas_height // 2 - images[0].height() // 2
    card_width = images[0].width()
    horizontal_spacing = 25  # Spacing between cards horizontally

    # Positions for the three-card spread:
    # New Card 1 in position of Card 4
    # New Card 2 in position of Card 1
    # New Card 3 in position of Card 6
    positions = [
        (center_x - card_width - horizontal_spacing, center_y),  # New Card 1 (Position of Card 4)
        (center_x, center_y),                                   # New Card 2 (Position of Card 1)
        (center_x + card_width + horizontal_spacing, center_y)  # New Card 3 (Position of Card 6)
    ]

    # Draw the three cards on the canvas
    for i, (x, y) in enumerate(positions):
        canvas.create_image(x, y, image=images[i], anchor='nw')

    # Keep a reference to prevent garbage collection
    canvas.images = images

    # Define the positional names for the three-card spread
    positional_names = [
        "Card 1: ",
        "Card 2: ",
        "Card 3: "
    ]

    # Display card meanings in the text box
    card_meanings = "\n".join(
        [f"{positional_names[i]}{cards[i]['name']}\n{cards[i]['meaning']}\n" for i in range(3)]
    )

    text_box.config(state="normal")  # Enable editing
    text_box.delete("1.0", tk.END)  # Clear previous content
    text_box.insert("1.0", card_meanings)
    text_box.config(state="disabled")  # Make the text read-only

def setup_main_gui(root, spread_type=None):
    # Set the main window size
    window_width = 1275  # Adjust as needed
    window_height = 825  # Adjust as needed
    root.geometry(f"{window_width}x{window_height}")

    # Prevent window resizing
    root.resizable(False, False)

    # Create content frames
    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)

    canvas_frame = tk.Frame(content_frame)
    canvas_frame.grid(row=0, column=0, rowspan=2, sticky="n")

    right_frame = tk.Frame(content_frame)
    right_frame.grid(row=0, column=1, sticky="n")

    # Create the text box with fixed padding to maintain layout
    vertical_padding = 100  # Adjust this value to move the text box up or down
    text_box = tk.Text(right_frame, wrap="word", height=30, width=55, font=("Courier New", 10))
    text_box.grid(row=0, column=0, padx=40, pady=(vertical_padding, 10), sticky="n")
    text_box.config(state="disabled")  # Initially empty and disabled

    # Create the buttons frame
    buttons_frame = tk.Frame(right_frame)
    buttons_frame.grid(row=1, column=0, padx=5, pady=(5, 10), sticky="n")

    # Create the "Draw One Card" button
    draw_one_card_button = tk.Button(
        buttons_frame,
        text="Draw One Card",
        width=20,
        command=lambda: draw_one_card(canvas_frame, text_box)
    )
    draw_one_card_button.pack(pady=5)

    # Create the "Draw Three Cards" button
    draw_three_cards_button = tk.Button(
        buttons_frame,
        text="Draw Three Cards",
        width=20,
        command=lambda: draw_three_cards(canvas_frame, text_box)
    )
    draw_three_cards_button.pack(pady=5)

    # Create the "Draw Celtic Cross" button
    draw_celtic_button = tk.Button(
        buttons_frame,
        text="Draw Celtic Cross",
        width=20,
        command=lambda: draw_celtic_cross(canvas_frame, text_box)
    )
    draw_celtic_button.pack(pady=5)

    # Adjust the row and column configurations to maintain layout
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=1)
    content_frame.grid_columnconfigure(1, weight=0)

    # If no spread is selected, add a placeholder
    if spread_type is None:
        add_placeholder(canvas_frame)
    else:
        # Perform the initial spread based on user selection
        if spread_type == "celtic":
            draw_celtic_cross(canvas_frame, text_box)
        elif spread_type == "one":
            draw_one_card(canvas_frame, text_box)
        elif spread_type == "three":
            draw_three_cards(canvas_frame, text_box)
        # If spread_type is None, do not draw any spread initially

def add_placeholder(canvas_frame):
    """Adds the back.gif image as a placeholder at Card 1 position."""
    try:
        # Path to back.gif
        image_path = os.path.join(os.path.dirname(__file__), "back.gif")
        
        # Open the image using PIL
        pil_image = Image.open(image_path)

        # Optionally resize the image to match card size
        scaling_factor = 1.055  #                                                           Adjust this factor as needed
        pil_image = pil_image.resize(
            (
                int(pil_image.width * scaling_factor),
                int(pil_image.height * scaling_factor)
            ),
            Image.LANCZOS
        )

        # Convert the PIL image to a PhotoImage
        placeholder_image = ImageTk.PhotoImage(pil_image)

        # Create a canvas to position the placeholder
        canvas_width = 700
        canvas_height = 800
        canvas = tk.Canvas(canvas_frame, width=canvas_width, height=canvas_height)
        canvas.pack(padx=10, pady=10)

        # Calculate center coordinates for Card 1
        center_x = canvas_width // 3
        center_y = (canvas_height // 2) - (pil_image.height // 2)

        # Add the placeholder image to the canvas at the Card 1 position
        canvas.create_image(center_x, center_y, image=placeholder_image, anchor='nw')

        # Keep a reference to prevent garbage collection
        canvas.placeholder_image = placeholder_image
    except Exception as e:
        print(f"Error loading placeholder image: {e}")

def main():
    root = tk.Tk()
    root.title("Tarot Cards")

    # Setup the main GUI without performing any initial spread
    setup_main_gui(root, spread_type=None)

    root.mainloop()

if __name__ == "__main__":
    main()
