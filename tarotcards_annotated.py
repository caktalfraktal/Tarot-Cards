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

    # Load images and handle rotation for the crossing card
    for i, card in enumerate(cards):
        image_path = os.path.join(os.path.dirname(__file__), card['image'])
        pil_image = Image.open(image_path)

        if i == 1:
            pil_image = pil_image.rotate(90, expand=True)

        images.append(pil_image)

    # Create a canvas that will resize with the window
    canvas = tk.Canvas(canvas_frame)
    canvas.pack(fill="both", expand=True)

    # Keep a reference to prevent garbage collection
    canvas.images = images

    # Bind the resize event
    canvas.bind("<Configure>", lambda event: redraw_celtic_cross(canvas, images))

    # Initial draw
    redraw_celtic_cross(canvas, images)

    # Update the text box with the card meanings
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

    card_meanings = "\n".join(
        [f"{positional_names[i]}:\n{cards[i]['name']} - {cards[i]['meaning']}\n" for i in range(10)]
    )

    text_box.config(state="normal")  # Enable editing
    text_box.delete("1.0", tk.END)  # Clear previous content
    text_box.insert("1.0", card_meanings)
    text_box.config(state="disabled")  # Make the text read-only

def redraw_celtic_cross(canvas, images):
    canvas.delete("all")

    # Get canvas dimensions
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Ensure canvas dimensions are greater than zero
    if canvas_width <= 0 or canvas_height <= 0:
        return  # Can't draw yet

    # Original card dimensions
    card_original_width = images[0].width
    card_original_height = images[0].height

    # Spacing adjustments at scaling=1
    spacing = 20
    horizontal_spacing = 100  # spacing * 5
    vertical_spacing_7_10 = -24
    extra_horizontal_spacing_4_6 = 30  # New extra spacing for cards 4 and 6
    extra_horizontal_offset_7_10 = 50   # New extra offset for cards 7-10

    # Total width and height needed at scaling=1, including extra spacings
    total_width = (
        4 * card_original_width
        + 3 * horizontal_spacing
        + 3 * extra_horizontal_spacing_4_6  # Updated from 2 to 3
        + extra_horizontal_offset_7_10
    )
    total_height = card_original_height * 4 + (-24 * 3)

    # Calculate scaling factors
    scaling_x = canvas_width / total_width
    scaling_y = canvas_height / total_height
    scaling = min(scaling_x, scaling_y, 1)  # Prevent scaling up beyond 1

    # Now adjust spacing and positions according to scaling
    spacing *= scaling
    horizontal_spacing *= scaling
    vertical_spacing_7_10 *= scaling
    extra_horizontal_spacing_4_6 *= scaling
    extra_horizontal_offset_7_10 *= scaling

    # Resize images
    resized_images = []
    for i, pil_image in enumerate(images):
        img = pil_image.copy()
        new_width = max(int(img.width * scaling), 1)
        new_height = max(int(img.height * scaling), 1)
        img = img.resize((new_width, new_height), Image.LANCZOS)
        resized_image = ImageTk.PhotoImage(img)
        resized_images.append(resized_image)

    card_width = resized_images[0].width()
    card_height = resized_images[0].height()

    # Recalculate total width at current scaling
    total_width = (
        4 * card_width
        + 3 * horizontal_spacing
        + 3 * extra_horizontal_spacing_4_6  # Updated from 2 to 3
        + extra_horizontal_offset_7_10
    )

    # Adjust center_x to center the spread within the canvas
    leftmost_x = (canvas_width - total_width) / 2
    center_x = leftmost_x + card_width + horizontal_spacing + extra_horizontal_spacing_4_6

    # Center_y can be center of canvas
    center_y = canvas_height / 2 - card_height / 2

    # Positions for the Celtic Cross layout
    positions = [
        (center_x, center_y),  # Card 1
        (
            center_x + (card_width - resized_images[1].width()) / 2,
            center_y + (card_height - resized_images[1].height()) / 2,
        ),  # Card 2
        (center_x, center_y + card_height + spacing),  # Card 3
        (
            center_x - card_width - horizontal_spacing - extra_horizontal_spacing_4_6,
            center_y,
        ),  # Card 4
        (center_x, center_y - card_height - spacing),  # Card 5
        (
            center_x + card_width + horizontal_spacing + extra_horizontal_spacing_4_6,
            center_y,
        ),  # Card 6
    ]

    # Positions for cards 7 to 10 (vertical line to the right)
    x_offset = (
        center_x
        + 2 * (card_width + horizontal_spacing)
        + extra_horizontal_offset_7_10
        + 2 * extra_horizontal_spacing_4_6
    )
    y_offset = center_y + 1.5 * (card_height + vertical_spacing_7_10)

    for i in range(6, 10):
        positions.append(
            (x_offset, y_offset - (card_height + vertical_spacing_7_10) * (i - 6))
        )

    # Draw the cards on the canvas
    for i, (x, y) in enumerate(positions):
        canvas.create_image(x, y, image=resized_images[i], anchor='nw')

    # Keep a reference to prevent garbage collection
    canvas.images = resized_images

def draw_one_card(canvas_frame, text_box):
    # Clear previous content in canvas_frame
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    cards = draw_cards(1)
    images = []

    # Load the single card image
    card = cards[0]
    image_path = os.path.join(os.path.dirname(__file__), card['image'])
    pil_image = Image.open(image_path)
    images.append(pil_image)

    # Create a canvas that will resize with the window
    canvas = tk.Canvas(canvas_frame)
    canvas.pack(fill="both", expand=True)

    # Keep a reference to prevent garbage collection
    canvas.images = images

    # Bind the resize event
    canvas.bind("<Configure>", lambda event: redraw_one_card(canvas, images))

    # Initial draw
    redraw_one_card(canvas, images)

    # Update the text box with the card meaning
    positional_names = ["Card: "]
    card_meanings = f"{positional_names[0]}{cards[0]['name']}\n{cards[0]['meaning']}\n"

    text_box.config(state="normal")  # Enable editing
    text_box.delete("1.0", tk.END)  # Clear previous content
    text_box.insert("1.0", card_meanings)
    text_box.config(state="disabled")  # Make the text read-only

def redraw_one_card(canvas, images):
    canvas.delete("all")

    # Get canvas dimensions
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Ensure canvas dimensions are greater than zero
    if canvas_width <= 0 or canvas_height <= 0:
        return  # Can't draw yet

    # Adjust scaling factor based on canvas size
    img = images[0]
    scaling = min(
        canvas_width / img.width,
        canvas_height / img.height
    )

    # Ensure scaling does not exceed 1
    scaling = min(scaling, 1)

    # Ensure scaling is not zero
    if scaling <= 0:
        scaling = 1

    # Resize image
    new_width = max(int(img.width * scaling), 1)
    new_height = max(int(img.height * scaling), 1)

    img_resized = img.resize((new_width, new_height), Image.LANCZOS)
    resized_image = ImageTk.PhotoImage(img_resized)

    # Center coordinates
    center_x = canvas_width // 2 - resized_image.width() // 2
    center_y = canvas_height // 2 - resized_image.height() // 2

    # Draw the card on the canvas
    canvas.create_image(center_x, center_y, image=resized_image, anchor='nw')

    # Keep a reference to prevent garbage collection
    canvas.images = [resized_image]

def draw_three_cards(canvas_frame, text_box):
    # Clear previous content in canvas_frame
    for widget in canvas_frame.winfo_children():
        widget.destroy()

    cards = draw_cards(3)
    images = []

    # Load the three card images
    for card in cards:
        image_path = os.path.join(os.path.dirname(__file__), card['image'])
        pil_image = Image.open(image_path)
        images.append(pil_image)

    # Create a canvas that will resize with the window
    canvas = tk.Canvas(canvas_frame)
    canvas.pack(fill="both", expand=True)

    # Keep a reference to prevent garbage collection
    canvas.images = images

    # Bind the resize event
    canvas.bind("<Configure>", lambda event: redraw_three_cards(canvas, images))

    # Initial draw
    redraw_three_cards(canvas, images)

    # Update the text box with the card meanings
    positional_names = [
        "Card 1: ",
        "Card 2: ",
        "Card 3: "
    ]

    card_meanings = "\n".join(
        [f"{positional_names[i]}{cards[i]['name']}\n{cards[i]['meaning']}\n" for i in range(3)]
    )

    text_box.config(state="normal")  # Enable editing
    text_box.delete("1.0", tk.END)  # Clear previous content
    text_box.insert("1.0", card_meanings)
    text_box.config(state="disabled")  # Make the text read-only

def redraw_three_cards(canvas, images):
    canvas.delete("all")

    # Get canvas dimensions
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Ensure canvas dimensions are greater than zero
    if canvas_width <= 0 or canvas_height <= 0:
        return  # Can't draw yet

    # Adjust scaling factor based on canvas size
    img_width = images[0].width
    img_height = images[0].height

    # Calculate total width needed
    spacing = 25  # Base spacing

    # Define padding
    padding_left = 30  # Increased padding to the left
    padding_right = 30  # Keep padding consistent

    total_width = padding_left + img_width * 3 + spacing * 2 + padding_right

    scaling = min(
        canvas_width / total_width,
        canvas_height / img_height
    )

    # Ensure scaling does not exceed 1
    scaling = min(scaling, 1)

    # Ensure scaling is not zero
    if scaling <= 0:
        scaling = 1

    # Apply scaling to spacing and padding
    horizontal_spacing = spacing * scaling
    padding_left_scaled = padding_left * scaling
    padding_right_scaled = padding_right * scaling

    # Resize images
    resized_images = []
    for img in images:
        new_width = max(int(img.width * scaling), 1)
        new_height = max(int(img.height * scaling), 1)

        img_resized = img.resize((new_width, new_height), Image.LANCZOS)
        resized_image = ImageTk.PhotoImage(img_resized)
        resized_images.append(resized_image)

    # Update card dimensions after resizing
    card_width = resized_images[0].width()
    card_height = resized_images[0].height()

    # Calculate total width needed after resizing
    total_width = padding_left_scaled + card_width * 3 + horizontal_spacing * 2 + padding_right_scaled

    # Calculate starting x position to center the cards
    start_x = (canvas_width - total_width) // 2 + padding_left_scaled
    center_y = canvas_height // 2 - card_height // 2

    positions = [
        (start_x, center_y),  # Card 1
        (start_x + card_width + horizontal_spacing, center_y),  # Card 2
        (start_x + 2 * (card_width + horizontal_spacing), center_y)  # Card 3
    ]

    # Draw the three cards on the canvas
    for i, (x, y) in enumerate(positions):
        canvas.create_image(x, y, image=resized_images[i], anchor='nw')

    # Keep a reference to prevent garbage collection
    canvas.images = resized_images

def setup_main_gui(root, spread_type=None):
    # Set the main window size (adjusted to accommodate three cards at full size)
    # Load a sample card to get its dimensions
    sample_card_path = os.path.join(os.path.dirname(__file__), tarot_deck[0]['image'])
    sample_card_image = Image.open(sample_card_path)
    card_width, card_height = sample_card_image.size

    # Calculate total width needed for three cards at full size with spacing and padding
    spacing = 25
    padding_left = 30
    padding_right = 30
    total_width = padding_left + card_width * 3 + spacing * 2 + padding_right

    # Set the window size accordingly
    window_width = total_width + 400                                        # Adding space for the text field and some extra margin
    window_height = card_height + 250                                       # Adding some extra margin for the window borders

    root.geometry(f"{int(window_width)}x{int(window_height)}")

    # Allow window resizing
    root.resizable(True, True)

    # Create content frames
    content_frame = tk.Frame(root)
    content_frame.pack(fill="both", expand=True)

    # Configure grid weights
    content_frame.grid_rowconfigure(0, weight=1)
    content_frame.grid_columnconfigure(0, weight=3)  # Adjusted weight for canvas_frame
    content_frame.grid_columnconfigure(1, weight=1)  # Increased weight for right_frame

    canvas_frame = tk.Frame(content_frame)
    canvas_frame.grid(row=0, column=0, sticky="nsew")

    right_frame = tk.Frame(content_frame, width=250)  # Increased width by 25%
    right_frame.grid(row=0, column=1, sticky="nsew")

    # Prevent right_frame from expanding beyond its width
    right_frame.grid_propagate(False)

    # Configure right_frame grid weights
    right_frame.grid_rowconfigure(0, weight=1)
    right_frame.grid_columnconfigure(0, weight=1)

    # Create the text box with a scrollbar
    text_frame = tk.Frame(right_frame)
    text_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Configure text_frame grid weights
    text_frame.grid_rowconfigure(0, weight=1)
    text_frame.grid_columnconfigure(0, weight=1)

    text_box = tk.Text(text_frame, wrap="word", font=("Courier New", 10), width=38)    #                Adjust text
    text_box.grid(row=0, column=0, sticky="nsew")

    # Add a scrollbar to the text box
    scrollbar = tk.Scrollbar(text_frame, orient="vertical", command=text_box.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")

    text_box.config(yscrollcommand=scrollbar.set)

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

def add_placeholder(canvas_frame):
    """Adds the back.gif image as a placeholder at the center."""
    try:
        # Clear previous content in canvas_frame
        for widget in canvas_frame.winfo_children():
            widget.destroy()

        # Path to back.gif
        image_path = os.path.join(os.path.dirname(__file__), "back.gif")

        # Open the image using PIL
        pil_image = Image.open(image_path)

        # Create a canvas that will resize with the window
        canvas = tk.Canvas(canvas_frame)
        canvas.pack(fill="both", expand=True)

        # Keep a reference to prevent garbage collection
        canvas.placeholder_image = pil_image

        # Bind the resize event
        canvas.bind("<Configure>", lambda event: redraw_placeholder(canvas, pil_image))

        # Initial draw
        redraw_placeholder(canvas, pil_image)

    except Exception as e:
        print(f"Error loading placeholder image: {e}")

def redraw_placeholder(canvas, pil_image):
    canvas.delete("all")

    # Get canvas dimensions
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()

    # Ensure canvas dimensions are greater than zero
    if canvas_width <= 0 or canvas_height <= 0:
        return  # Can't draw yet

    # Adjust scaling factor based on canvas size
    scaling = min(canvas_width / pil_image.width, canvas_height / pil_image.height)

    # Ensure scaling does not exceed 1
    scaling = min(scaling, 1)

    # Ensure scaling is not zero
    if scaling <= 0:
        scaling = 1  # Or some default scaling factor

    # Resize image
    new_width = max(int(pil_image.width * scaling), 1)
    new_height = max(int(pil_image.height * scaling), 1)

    img = pil_image.resize((new_width, new_height), Image.LANCZOS)
    resized_image = ImageTk.PhotoImage(img)

    # Center coordinates
    center_x = canvas_width // 2 - resized_image.width() // 2
    center_y = canvas_height // 2 - resized_image.height() // 2

    # Draw the placeholder on the canvas
    canvas.create_image(center_x, center_y, image=resized_image, anchor='nw')

    # Keep a reference to prevent garbage collection
    canvas.placeholder_image = resized_image

def main():
    root = tk.Tk()
    root.title("Tarot Cards")

    # Allow window resizing
    root.resizable(True, True)

    # Setup the main GUI without performing any initial spread
    setup_main_gui(root, spread_type=None)

    root.mainloop()

if __name__ == "__main__":
    main()