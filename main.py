from flask import Flask, render_template, request
import numpy as np
from collections import Counter
import webcolors
import cv2

app = Flask(__name__)

def top_10_colours(image_path):
    image = cv2.imread(image_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    pixels = np.reshape(image, (-1, 3))
    color_counts = Counter(tuple(pixel) for pixel in pixels)
    total_pixels = len(pixels)
    top_colors = color_counts.most_common(10)
    top_colors_with_percentage = [(webcolors.rgb_to_hex(color), count, round(count / total_pixels * 100, 2), color) for color, count in top_colors]
    return top_colors_with_percentage

@app.route('/', methods=['GET', 'POST'])
def upload_image():
    if request.method == 'POST':
        if 'file' not in request.files:
            return render_template('index.html', error='No file part')

        file = request.files['file']

        if file.filename == '':
            return render_template('index.html', error='No selected file')

        if file:
            file_path = 'static/assets/' + file.filename
            file.save(file_path)
            top_colors = top_10_colours(file_path)
            return render_template('index.html', top_colors=top_colors, image_path=file_path)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)







