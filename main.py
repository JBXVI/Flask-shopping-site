from flask import Flask, render_template as render, request as req, url_for, redirect
from pymongo import MongoClient
import time
import os


class Orders:
    def __init__(self):
        self.client = MongoClient("mongodb://localhost:27017/")

        # databse - db_admin - col_admin (for uploading products and update order status)
        self.admin = self.client['root']
        self.col_uploads = self.admin['uploads']

    def flaskapp(self):

        col_uploads = self.col_uploads

        app = Flask(__name__)
        app.config['UPLOAD_PATH'] = 'static/images'

        @app.route('/', methods=["GET", "POST"])
        def home():
            products = col_uploads.find()
            return render("home.html", products=products)

        @app.route('/upload', methods=["GET", "POST"])
        def upload():
            if req.method == "POST":
                title = req.form.get('title')
                price = req.form.get('price')
                desciption = req.form.get("description")
                id = req.form.get('id')
                tags = req.form.get("tags")
                m = req.form.get('m')
                l = req.form.get('l')
                xl = req.form.get('xl')
                xxl = req.form.get('xxl')
                xxxl = req.form.get('xxxl')

                file = req.files['image']

                file.save(os.path.join(app.config['UPLOAD_PATH'], id + ".jpg"))
                image_path = f"/{app.config['UPLOAD_PATH']}/{id}.jpg"
                find = col_uploads.find_one({"id": id})
                if find != None:
                    return render("upload.html", message="Same ID already exists")
                else:
                    t = time.localtime()
                    current_time = time.strftime("%I:%M:%S:%p", t)
                    current_date = time.strftime("%y:%m:%d")
                    col_uploads.insert_one({"title": title, "price": price,"image":image_path, "desciption":desciption, "id": id, "tags": tags
                                               , "m": m, "l": l, "xl": xl, "xxl": xxl, "xxxl": xxxl
                                               , "time": current_time, "date": current_date})
                    return render("upload.html", message="successfully uploaded")

            return render('upload.html', message="")

        if __name__ == "__main__":
            app.run(debug=True)


app = Orders()
app.flaskapp()
