from flask import Flask, render_template, request, session, redirect, url_for
import random
import os
import json

app = Flask(__name__)
app.secret_key = '8f42a73054b173648f58838be5e6502c'

def load_photo_counts():
    try:
        with open('photo_counts.json', 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

# Function to save photo counts
def save_photo_counts(counts):
    with open('photo_counts.json', 'w') as file:
        json.dump(counts, file)

# Load initial photo counts
photo_counts = load_photo_counts()

# Function to reset photo counts to initial values
def reset_photo_counts():
    global photo_counts
    photo_counts = {}
    save_photo_counts(photo_counts)

# Function to get folder names dynamically
def get_folders():
    try:
        folder_path = 'static/photo/'
        folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        return folders
    except FileNotFoundError:
        return []

# Function to get paths of photos for all sets
def get_all_photo_paths():
    all_photo_paths = {}
    try:
        folder_path = 'static/photo/'
        folders = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
        allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}

        for folder in folders:
            folder_path = f'static/photo/{folder}/'
            photo_paths = [
                f'photo/{folder}/{filename}' for filename in os.listdir(folder_path)
                if filename.split('.')[-1].lower() in allowed_extensions
            ]
            all_photo_paths[folder] = photo_paths

    except FileNotFoundError:
        pass

    return all_photo_paths

@app.route('/')
def index():
    all_photo_paths = get_all_photo_paths()
    return render_template('index.html', all_photo_paths=all_photo_paths, artist_name=session.get('artist_name', 'Anonymous Artist'))

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        if 'artistName' in request.form:
            session['artist_name'] = request.form['artistName']
        if 'photoFolder' in request.form:
            session['photo_folder'] = request.form['photoFolder']
        return redirect(url_for('index'))
    return render_template('settings.html', photo_folders=get_folders())

@app.route('/vote', methods=['POST'])
def vote():
    selected_photo_path = request.form['photo']
    selected_photo = os.path.basename(selected_photo_path)

    folder_name = session.get('photo_folder', 'default')

    if folder_name not in photo_counts:
        photo_counts[folder_name] = {}

    if selected_photo not in photo_counts[folder_name]:
        photo_counts[folder_name][selected_photo] = 0

    photo_counts[folder_name][selected_photo] += 1
    save_photo_counts(photo_counts)

    all_photo_paths = get_all_photo_paths()

    # Shuffle the photo paths for the selected set
    selected_set_paths = all_photo_paths.get(folder_name, [])
    random.shuffle(selected_set_paths)

    print(f"Voted for {selected_photo}. Total votes: {photo_counts[folder_name][selected_photo]}")  # Voor debugging

    # Haal de lijst van alle mapnamen op
    all_folders = get_folders()

    # Bepaal de index van de huidige map
    current_folder_index = all_folders.index(folder_name)

    # Kies de volgende map (rond af naar het begin als het de laatste map is)
    next_folder_index = (current_folder_index + 1)
    if next_folder_index == len(all_photo_paths):
        next_folder_index = 0
    
    next_folder = all_folders[next_folder_index]

    # Update de sessie met de geselecteerde map
    session['photo_folder'] = next_folder

    # Haal de paden van de foto's op voor de nieuwe map
    next_set_paths = all_photo_paths.get(next_folder, [])
    # random.shuffle(next_set_paths)

    return render_template('index.html', all_photo_paths={next_folder: next_set_paths}, artist_name=session.get('artist_name', 'Anonymous Artist'))

@app.route('/results')
def results():
    all_photo_paths = get_all_photo_paths()
    
    all_photo_data = {}
    for folder, photo_paths in all_photo_paths.items():
        photo_data = {}
        for photo_path in photo_paths:
            photo = os.path.basename(photo_path)
            votes = photo_counts.get(folder, {}).get(photo, 0)
            photo_data[photo_path] = {"votes": votes, "filename": photo}  # Update de structuur van photo_data
        all_photo_data[folder] = photo_data

    print("Loaded photo counts:", photo_counts)

    return render_template('results.html', all_photo_data=all_photo_data)



@app.route('/reset_counts', methods=['POST'])
def reset_counts():
    reset_photo_counts()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)