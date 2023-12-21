from flask import Flask, render_template, request, jsonify, session, redirect, url_for, abort
import numpy as np
from joblib import load
import pandas as pd

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Ganti dengan kunci rahasia yang kuat

@app.route("/")
def home():
    return render_template("index.html")

# Data anggota
class Founder:
    def __init__(self, name, photo, nim, prodi,university, jobdes):
        self.name = name
        self.photo = photo
        self.nim = nim
        self.prodi = prodi
        self.university = university
        self.jobdes = jobdes

founders_data = [
    Founder("Iryu Astika Haidar", "img/iryu.png", "20210410700072", "Teknik Informatika", "Universitas Muhammadiyah Jakarta", "Data Exploration | Machine Learning Engineer"),
    Founder("Delila Septiani Dwi Putri", "img/delila.png", "1306620028","Fisika", "Universitas Negeri Jakarta", "UI/UX | Back-End Development"),
    Founder("Luthfiyanti Indah Saputri", "img/luthfiyanti.png", "12210408", "Informatika","Universitas Nusa Mandiri", "UI/UX | Front-End Development"),
    Founder("Siti Uswatun Hasanah", "img/uswah.png", "3121071", "Pend. Agama Islam","Universitas Islam Jakarta", "Data Collecting | Content Created"),
]
@app.route('/about')
def about():
    return render_template('about.html', founders=founders_data)

# Data pertanyaan Faq
faq_data = [
    {"question": "Apa itu BMI?", "answer": "Body Mass Index atau Indeks Massa Tubuh adalah cara menghitung berat badan ideal yang didasarkan pada usia, berat badan dan tinggi badan seseorang."},
    {"question": "Apa itu Kalkulator BMI?", "answer": "Kalkulator BMI adalah alat atau metrik standar yang digunakan untuk menghitung dan mengidentifikasi apakah berat badan kamu termasuk dalam kategori ideal atau tidak."},
    {"question": "Ada berapa kategori dalam BMI?", "answer": "Kategori BMI dibagi menjadi beberapa yaitu, Berat Badan Kurang (Underweight), Normal, Kelebihan berat badan (Overweight), Obesitas, dan Obesitas II. Kategori dalam BMI memberikan gambaran umum tentang status berat badan seseorang."},
    {"question": "Berapa BMI ideal atau normal?", "answer": "Angka BMI normal berada pada kisaran 18,5-25. Jika angka BMI melebihi 25, kamu memiliki berat badan berlebih (overweight). Sementara itu, jika angka BMI berada di bawah 18 berarti berat badan kurang (underweight)."},
    {"question": "Mengapa penting mengetahui BMI?", "answer": "Mengetahui BMI dapat membantu dalam memahami apakah berat badan mereka berada dalam kategori yang tergolong ideal atau tidak. Dan BMI dapat membantu dalam melambangkan kesehatan kita, misalkan semakin tinggi BMI dari angka normal, berarti termasuk golongan obesitas sehingga dapat meningkatkan risiko penyakit jantung, dan penyakit berbahaya lainnya"},
    {"question": "Hal apa saja yang perlu diperhatikan pada Kalkulator BMI?", "answer": "Terdapat dua hal yang perlu diperhatikan saat menghitung BMI yaitu rumus BMI dan kategori berat badan."},
    {"question": "Apakah BMI sepenuhnya akurat dalam mengukur kebugaran tubuh?", "answer": "Meskipun BMI memberikan indikasi kasar tentang berat badan seseorang, itu tidak membedakan antara lemak tubuh dan massa otot. Oleh karena itu, dapat ada variasi dalam interpretasi, terutama untuk atlet yang memiliki tingkat massa otot tinggi."},
    {"question": "Apa itu VITA?", "answer": "VITA (Vitality Assistant for Achieving Your Ideal Shape) adalah sebuah situs web yang menggunakan kecerdasan buatan (AI ) untuk menghitung dan memberikan informasi terkait BMI (Body Mass Index) seseorang berdasarkan usia, berat badan serta tinggi badan."},
    {"question": "Bagaimana AI BMI di VITA berfungsi?", "answer": "VITA menggunakan algoritma kecerdasan buatan (AI) untuk mengolah dan memprediksi data usia, berat badan dan tinggi badan yang dimasukkan oleh pengguna. Algoritma VITA kemudian menghitung nilai BMI, kemudian memberikan hasil terkait kategori berat badan, seperti underweight, normal, overweight, atau obese, dan memberikan saran kesehatan sesuai dengan hasil prediksi."},
    {"question": "Apakah VITA memberikan saran kesehatan?", "answer": "Ya, VITA memberikan informasi dan saran kesehatan sesuai dengan hasil dari kategori berat badan pengguna. Tetapi apabila diperlukan pengguna disarankan untuk berkonsultasi dengan profesional kesehatan untuk evaluasi lebih lanjut."},
    {"question": "Apakah VITA menyediakan rekomendasi makanan diet atau alat kebugaran?", "answer": "Ya, VITA memberikan rekomendasi makanan diet dan peralatan olahraga dari perusahaan yang bekerja sama dengan kami. Sehingga dapat membantu dalam mencapai berat ideal Anda."},
]
@app.route('/faq')
def faq():
    return render_template('faq.html', faq_data=faq_data)

@app.route('/product')
def product():
    return render_template('product.html')

# Data produk makanan
food_products = [
    {"name": "Cranapple Muffin", "description": "Diet to Go", "kalori":"280", "harga":"35.000", "image": "img/food1.png"},
    {"name": "Classic Egg & Potato", "description": "FRESHNLEAN","kalori":"400", "harga":"40.000", "image": "img/food2.png"},
    {"name": "Avocado Toast with Egg", "description": "Diet to Go", "kalori":"260", "harga":"45.000", "image": "img/food3.png"},
    {"name": "French Toast", "description": "Diet to Go", "kalori":"300", "harga":"30.000", "image": "img/food4.png"},
    {"name": "Comfort Beef Stew", "description": "FRESHNLEAN", "kalori":"450","harga":"70.000", "image": "img/food5.png"},
    {"name": "Tuscan Bean Salad", "description": "Diet to Go", "kalori":"360","harga":"50.000", "image": "img/food6.png"},
    {"name": "Crustless Chicken Potato", "description": "FRESHNLEAN", "kalori":"540","harga":"60.000", "image": "img/food7.png"},
    {"name": "Baked Turkey with Rice", "description": "Diet to Go", "kalori":"380","harga":"55.000", "image": "img/food8.png"},
    {"name": "Lemon Butter Seared Basa with Garlicky Brussels Hash", "description": "FRESHNLEAN", "kalori":"450","harga":"75.000", "image": "img/food9.png"},
    {"name": "Lemon Garlic Chicken with Snap Peas", "description": "FRESHNLEAN", "kalori":"450","harga":"55.000", "image": "img/food10.png"},
    {"name": "Grilled Chicken with Mashed Potatoes, Corn And Gravy", "description": "FRESHNLEAN", "kalori":"370","harga":"65.000", "image": "img/food11.png"},
    {"name": "Hearty Granola (4OZ) - Original", "description": "FRESHNLEAN", "kalori":"370","harga":"50.000", "image": "img/food12.png"},
]
@app.route('/food')
def food():
    return render_template('food.html', products=food_products)

# Data produk olahraga
sport_products = [
    {"name": "[FREE Bag] Yoga Mat NBR 10mm Pastel", "category": "Home Workout, Yoga & Pilates", "description": "HAPPYFIT", "harga":"139.000", "image": "img/sport1.png"},
    {"name": "[FREE Strap] Yoga Mat TPE Eco Friendly 6mm Polos","category": "Home Workout,  Yoga & Pilates", "description": "HAPPYFIT", "harga":"159.000", "image": "img/sport2.png"},
    {"name": "Neoprene Kettlebell 2, 6, 10, 14 KG","category": "Home Workout, Gym & Fitness", "description": "HAPPYFIT", "harga":"398,000", "image": "img/sport3.png"},
    {"name": "[2 PCS] Neoprene Non Slip Dumbbell 1 KG", "category": "Home Workout, Gym & Fitness", "description": "HAPPYFIT", "harga":"129,000", "image": "img/sport4.png"},
    {"name": "[2 PCS] Neoprene Non Slip Dumbbell 1,5 KG", "category": "Home Workout, Gym & Fitness", "description": "HAPPYFIT", "harga":"169.000", "image": "img/sport5.png"},
    {"name": "[2 PCS] Neoprene Non Slip Dumbbell 4 KG", "category": "Home Workout, Gym & Fitness", "description": "HAPPYFIT", "harga":"399.000", "image": "img/sport6.png"},
    {"name": "New PVC Jump Rope", "category": "Home Workout, Jump Rope", "description": "HAPPYFIT", "harga":"48.000", "image": "img/sport7.png"},
    {"name": "Anti Burst Gym Ball 55 CM", "category": "Home Workout, Yoga & Pilates", "description": "HAPPYFIT", "harga":"129.000", "image": "img/sport8.png"},
    {"name": "Raket Tenis Dewasa Lite TR160", "category": "Tenis", "description": "DECATHLON", "harga":"450.000", "image": "img/sport9.png"},
    {"name": "Raket Badminton Dewasa Br 930 P", "category": "Badminton", "description": "DECATHLON", "harga":"250.000", "image": "img/sport10.png"},
    {"name": "BT100 Size 7 Basketball - Oranye","category": "Basket", "description": "DECATHLON", "harga":"230.000", "image": "img/sport11.png"},
    {"name": "Bola Voli Outdoor Pemula", "category": "Voli", "description": "DECATHLON", "harga":"270.000", "image": "img/sport12.png"},
] 
@app.route('/sport')
def sport():
    return render_template('sport.html', products=sport_products)

@app.route('/cart')
def cart():
    cart_products = session.get('cart', [])
    return render_template('cart.html', cart_products=cart_products)

@app.route('/add_to_cart/<string:category>/<int:product_id>')
def add_to_cart(category, product_id):
    if category == 'food':
        products = food_products
    elif category == 'sport':
        products = sport_products
    else:
        # Kategori tidak valid
        abort(404)

    # Pastikan product_id valid
    if 1 <= product_id <= len(products):
        product = products[product_id - 1]
        cart_products = session.get('cart', [])
        cart_products.append(product)
        session['cart'] = cart_products
        return redirect(url_for('cart'))
    else:
        # product_id tidak valid
        abort(404)

@app.route('/remove_from_cart/<int:product_index>')
def remove_from_cart(product_index):
    cart_products = session.get('cart', [])
    
    if 1 <= product_index <= len(cart_products):
        del cart_products[product_index - 1]
        session['cart'] = cart_products
    
    return redirect(url_for('cart'))

@app.route('/get_started')
def get_started():
    # Implement logic for the 'GET STARTED' page
    return render_template("get_started.html")

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/api/calculate_bmi', methods=['POST'])
def calculate_bmi():
    if request.method=='POST':
        input_gender = request.form.get('gender')
        input_age = int(request.form.get('age'))
        input_weight = float(request.form.get('weight'))
        input_height = float(request.form.get('height'))

        # Hitung BMI
        bmi = input_weight / ((input_height / 100) ** 2) 

        #Load data
        data = pd.read_csv('vita_test.csv', sep=';')

        #membuat dataframe pandas
        df = pd.DataFrame(
            data={ 
            "age":[input_age],
            "height":[input_height],
            "weight":[input_weight],
            "bmi":[bmi]
            }
        )
        
        #menampilkan prediksi model
        hasil_prediksi = model.predict(df[0:1])[0]
        print(f"Hasil Prediksi: {hasil_prediksi}")
        
        if hasil_prediksi == 'Underweight':
            advice1 = 'Disarankan 2,500 - 3,000 kalori atau lebih, tergantung pada kebutuhan individu.'
            advice2 = '4-5 makanan utama dengan porsi tambahan, Camilan tinggi kalori di antara waktu makan utama.'
            advice3 = 'Latihan kekuatan untuk membangun massa otot, Aerobik yang ringan untuk meningkatkan nafsu makan.'
            advice4 = 'Minum air secara teratur sepanjang hari.'
        elif hasil_prediksi == 'Normal Weight':
            advice1 = 'Disarankan 2,000 - 2,500 kalori dan dapat disesuaikan dengan kebutuhan individu'
            advice2 = '3 besar makanan utama dengan porsi seimbang, 2 - 3 camilan sehat antara waktu makan utama, Hindari makan berlebihan.'
            advice3 = 'Minimal 150 menit aktivitas aerobik sedang atau 75 menit aktivitas aerobik intensitas tinggi setiap minggu, Latihan kekuatan 2 kali seminggu.'
            advice4 = 'Setidaknya 8 gelas air per hari, dapat disesuaikan dengan kebutuhan individu'
        elif hasil_prediksi == 'Overweight':
            advice1 = 'Reduksi sekitar 500 - 1,000 kalori dari kebutuhan harian.'
            advice2 = 'Porsi yang lebih kecil dengan fokus pada makanan rendah kalori, 4 - 5 makanan utama dengan porsi yang terkontrol.'
            advice3 = 'Minimal 150-300 menit aktivitas aerobik sedang atau 75 - 90 menit aktivitas aerobik intensitas tinggi per minggu, Latihan kekuatan 2 kali seminggu.'
            advice4 = 'Setidaknya 8 - 10 gelas air per hari, dapat disesuaikan dengan kebutuhan individu'
        elif hasil_prediksi == 'Obese Class 1':
            advice1 = 'Reduksi sekitar 800 - 1,200 kalori dari kebutuhan harian.'
            advice2 = 'Porsi yang lebih kecil dengan fokus pada makanan rendah kalori, makanan utama dengan porsi yang terkontrol.'
            advice3 = 'Lakukan aktivitas fisik seperti senam, bersepeda, berenang, dan jalan kaki minimal 30 menit setiap hari atau 150 menit setiap minggu. Latihan kekuatan 4 kali seminggu.'
            advice4 = 'Setidaknya 8-10 gelas air per hari, dapat disesuaikan dengan kebutuhan individu'
        elif hasil_prediksi == 'Obese Class 2':
            advice1 = 'Reduksi sekitar 1000 - 1,200 kalori dari kebutuhan harian.'
            advice2 = 'Porsi yang lebih kecil dengan fokus pada makanan rendah kalori, makanan utama dengan porsi yang terkontrol.'
            advice3 = 'Lakukan aktivitas fisik seperti senam, bersepeda, berenang, dan jalan kaki minimal 45 menit setiap hari atau 225 menit setiap minggu. Latihan kekuatan 4 kali seminggu.'
            advice4 = 'Setidaknya 8-10 gelas air per hari, dapat disesuaikan dengan kebutuhan individu'
        else:
            advice1 = 'Reduksi sekitar 1,200 - 1,500 kalori dari kebutuhan harian.'
            advice2 = 'Porsi yang lebih kecil dengan fokus pada makanan rendah kalori, makanan utama dengan porsi yang terkontrol, batasi asupan gula, garam, dan lemak yang berlebihan.'
            advice3 = 'Lakukan aktivitas fisik seperti senam, bersepeda, berenang, jalan kaki minimal 60 menit setiap hari atau 300 menit setiap minggu. Latihan kekuatan 4 kali seminggu.'
            advice4 = 'Setidaknya 8 - 10 gelas air per hari.'

        #return hasil prediksi dengan format jsoN
        #return jsonify({
        #   "prediksi": str(hasil_prediksi)
        #})
    
        return render_template('history.html', prediction=hasil_prediksi, advice1=advice1, advice2=advice2, advice3=advice3, advice4=advice4)

if __name__ == "__main__":
    model= load('vitax.model')

    app.run(host='0.0.0.0',port = 4000,debug=True)