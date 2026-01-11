from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
import numpy as np
from PIL import Image
import os
from werkzeug.utils import secure_filename
import tensorflow as tf
try:
    from tensorflow.keras.models import load_model
except ImportError:
    from keras.models import load_model

import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Inisialisasi Flask app
app = Flask(__name__)

# Konfigurasi
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # Max 16MB
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Konfigurasi Gemini API
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    print(f"DEBUG: API Key Loaded: {GEMINI_API_KEY[:10]}...") # Print depan key untuk verifikasi
else:
    print("WARNING: GEMINI_API_KEY not found in environment variables.")

# Daftar kelas (urutan sesuai output model)
CLASS_NAMES = [
    'bangun_bangun',
    'jambu_biji',
    'lidah_buaya',
    'mint',
    'pandan',
    'pegagan',
    'sirih',
    'sirsak'
]

# Load model saat aplikasi dimulai
print("Loading model...")
try:
    model = load_model('mobilenetv2_daun_v2.h5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

def allowed_file(filename):
    """Cek apakah file yang diupload valid"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def preprocess_image(image_path):
    """
    Preprocessing gambar:
    - Resize, Convert RGB, Normalize, Expand Dims
    """
    # Load dan resize gambar
    img = Image.open(image_path)
    img = img.resize((224, 224))
    
    # Konversi ke RGB jika perlu (untuk gambar grayscale atau RGBA)
    if img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Konversi ke numpy array
    img_array = np.array(img)
    
    # Normalisasi pixel ke range 0-1
    img_array = img_array.astype('float32') / 255.0
    
    # Expand dimension untuk batch (model expect shape: (batch_size, 224, 224, 3))
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

def get_herbal_info(plant_name):
    """
    Menggunakan Gemini API untuk mendapatkan informasi khasiat tanaman.
    """
    if not GEMINI_API_KEY:
        print("DEBUG: API Key is missing inside get_herbal_info")
        return "API Key Gemini belum dikonfigurasi. Tidak dapat memuat informasi khasiat."
    
    # Daftar model cadangan (Fallback models)
    # Kita coba dari yang paling baru/experimental (biasanya kuota besar) ke yang stabil
    # Daftar model cadangan (Fallback models)
    # Prioritas sesuai request user: Gemini 2.0 Flash
    candidate_models = [
        'gemini-2.0-flash',       # Prioritas UTAMA (Confirmed by User CURL)
        'gemini-2.0-flash-exp',
        'gemini-1.5-flash',
        'gemini-flash-latest'
    ]

    last_error = None

    for model_name in candidate_models:
        try:
            print(f"DEBUG: Trying Gemini Model: {model_name}...")
            model_gemini = genai.GenerativeModel(model_name)
            
            prompt = f"""
            Berikan informasi singkat dan menarik tentang tanaman herbal "{plant_name}" dalam Bahasa Indonesia.
            Format output yang diinginkan (gunakan markdown untuk styling):
            
            ### 🌱 Khasiat Utama
            [Jelaskan 2-3 khasiat utama secara singkat]
            
            ### 🍵 Cara Penggunaan Tradisional
            [Jelaskan 1 cara penggunaan yang paling umum dan mudah]
            
            ### ⚠️ Peringatan Singkat
            [Satu kalimat peringatan atau efek samping jika ada]
            
            Jawab dengan tone informatif, ramah, dan ringkas. Jangan terlalu panjang.
            """
            
            response = model_gemini.generate_content(prompt)
            print(f"DEBUG: Success with model {model_name}!")
            return response.text
            
        except Exception as e:
            print(f"DEBUG: Failed with {model_name}: {e}")
            last_error = e
            # Lanjut ke model berikutnya di list
            continue
            
    # Jika semua gagal
    import traceback
    traceback.print_exc()
    return f"Maaf, gagal memuat informasi khasiat. Semua model sibuk/limit. Error terakhir: {str(last_error)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    """Halaman utama & Logic Prediksi"""
    prediction_result = None
    
    if request.method == 'POST':
        # Cek file
        if 'file' not in request.files:
            return redirect(request.url)
            
        file = request.files['file']
        
        if file.filename == '':
            return redirect(request.url)
            
        if file and allowed_file(file.filename):
            try:
                # 1. Simpan File
                filename = secure_filename(file.filename)
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                
                # 2. Prediksi CNN (Gunakan helper function yang ada)
                if model is None:
                    raise Exception("Model CNN belum siap.")

                processed_image = preprocess_image(filepath)
                predictions = model.predict(processed_image)
                
                confidence = np.max(predictions) * 100
                predicted_class = CLASS_NAMES[np.argmax(predictions)]
                
                # Format nama
                readable_name = predicted_class.replace('_', ' ').title()
                
                # 3. Info Gemini
                description = get_herbal_info(readable_name)
                
                # 4. Data untuk Template
                prediction_result = {
                    'name': readable_name,
                    'confidence': f"{confidence:.1f}",
                    'description': description,
                    'image_path': filename  # Jika ingin menampilkan file yg diupload (perlu setup static url)
                }
                
                # Hapus file temp (optional, atau biarkan untuk debug/display)
                # os.remove(filepath) 
                
            except Exception as e:
                print(f"Error processing: {e}")
                prediction_result = {'error': str(e)}

    return render_template('index.html', prediction=prediction_result)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    from flask import send_from_directory
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/predict', methods=['POST'])
def predict_api():
    return redirect(url_for('index'))
    
    # Cek apakah file valid
    if file and allowed_file(file.filename):
        # Simpan file dengan nama yang aman
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            if model is None:
                raise Exception("Model CNN tidak dimuat dengan benar.")

            # 1. Prediksi menggunakan CNN
            processed_image = preprocess_image(filepath)
            predictions = model.predict(processed_image)
            predicted_class_idx = np.argmax(predictions[0])
            predicted_class = CLASS_NAMES[predicted_class_idx]
            confidence = float(predictions[0][predicted_class_idx] * 100)
            
            # Format nama daun agar lebih rapi untuk ditampilkan dan dikirim ke LLM
            readable_name = predicted_class.replace('_', ' ').title()
            
            # 2. Generate Info Khasiat menggunakan Gemini
            description = get_herbal_info(readable_name)
            
            # Hapus file setelah prediksi (opsional, untuk menghemat space)
            os.remove(filepath)
            
            # Return hasil prediksi
            return jsonify({
                'success': True,
                'predicted_class': predicted_class,
                'readable_name': readable_name,
                'confidence': round(confidence, 2),
                'description': description
            })
            
        except Exception as e:
            # Hapus file jika terjadi error
            if os.path.exists(filepath):
                os.remove(filepath)
            return jsonify({'error': f'Process error: {str(e)}'}), 500
    
    else:
        return jsonify({'error': 'Invalid file type'}), 400

if __name__ == '__main__':
    # Pastikan folder uploads ada
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Jalankan aplikasi di localhost
    print("\n" + "="*50)
    print("🌿 Aplikasi Klasifikasi Daun Herbal")
    print("="*50)
    print("Server running at: http://localhost:5000")
    print("Press CTRL+C to quit")
    print("="*50 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
