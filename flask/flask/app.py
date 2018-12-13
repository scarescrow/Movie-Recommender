from flask import Flask, render_template, request
import model
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

# @app.route('/conventional')

@app.route('/image')
def image():
    return render_template('image.html')

@app.route('/image-result', methods=['GET', 'POST'])
def image_result():
    try:
        original_title = request.form['original-title']
        nbrs = model.show_recommendations(original_title, image_df)
        query = nbrs[0]
        recs = nbrs[1:]    
        return render_template('image-result.html', query=query, recs=recs)
    except:
        return render_template('error.html')

@app.route('/movies', methods=['GET'])
def list_movies():
    try:
        movies_list = model.get_image_ids(image_df)
        return render_template('all-movies.html', movies=movies_list, path=model.construct_nbr_file_path)
    except Exception as e:
        print(e)
        return render_template('error.html')


if __name__ == '__main__':
    image_df = model.load_pickled_df()
    app.run(debug=True)
