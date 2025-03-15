from flask import Flask, render_template, request, redirect, url_for
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads' 
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
items = []

def allowed_file(filename):
    """Check if the file has a valid extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    """Render the homepage with all items."""
    return render_template('home.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    """Add a new item to the marketplace."""
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        price = request.form['price']
        contact = request.form['contact']
        image = request.files['image']

        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)  
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)  
            image.save(image_path)  
            image_url = f'{UPLOAD_FOLDER}/{filename}' 
        else:
            image_url = None

        new_item = {
            'name': name,
            'description': description,
            'price': price,
            'contact': contact,
            'image': image_url
        }

        items.append(new_item)

      
        return redirect(url_for('home'))

    return render_template('add_item.html')

if __name__ == '__main__':
  
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)