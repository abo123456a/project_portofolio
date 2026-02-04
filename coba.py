from flask import Flask, render_template_string, request, redirect, url_for

app = Flask(__name__)

# =========================
# Data dummy (biasanya di database)
# =========================
produk_list = [
    {"id": 1, "nama": "Kopi Arabika", "harga": 50000, "stok": 10},
    {"id": 2, "nama": "Kopi Robusta", "harga": 40000, "stok": 8},
    {"id": 3, "nama": "Teh Hijau", "harga": 35000, "stok": 12}
]

# =========================
# Template HTML sederhana
# =========================
layout = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f3f3f3; }
        header { background: #222; color: white; padding: 15px; text-align: center; }
        nav a { color: white; margin: 0 15px; text-decoration: none; }
        .container { padding: 20px; }
        .produk { background: white; border-radius: 5px; padding: 15px; margin: 10px 0; box-shadow: 0 0 5px #aaa; }
        footer { text-align: center; padding: 15px; background: #222; color: white; margin-top: 40px; }
        input, button { padding: 8px; margin-top: 10px; }
    </style>
</head>
<body>
    <header>
        <h1>☕ Toko Kopi & Teh</h1>
        <nav>
            <a href="/">Beranda</a>
            <a href="/produk">Produk</a>
            <a href="/kontak">Kontak</a>
        </nav>
    </header>

    <div class="container">
        {{ content }}
    </div>

    <footer>
        <p>© 2025 Toko Kopi & Teh | Dibuat dengan Python + Flask</p>
    </footer>
</body>
</html>
"""

# =========================
# Halaman Beranda
# =========================
@app.route('/')
def beranda():
    content = """
        <h2>Selamat datang di Toko Kopi & Teh!</h2>
        <p>Kami menjual kopi dan teh pilihan terbaik dari seluruh nusantara.</p>
        <p><a href='/produk'>Lihat Produk Kami</a></p>
    """
    return render_template_string(layout, title="Beranda", content=content)

# =========================
# Halaman Daftar Produk
# =========================
@app.route('/produk')
def produk():
    content = "<h2>Daftar Produk</h2>"
    for p in produk_list:
        content += f"""
        <div class='produk'>
            <h3>{p['nama']}</h3>
            <p>Harga: Rp {p['harga']:,}</p>
            <p>Stok: {p['stok']}</p>
            <form action='/beli/{p['id']}' method='post'>
                <button type='submit'>Beli Sekarang</button>
            </form>
        </div>
        """
    return render_template_string(layout, title="Produk", content=content)

# =========================
# Halaman Beli Produk (POST)
# =========================
@app.route('/beli/<int:produk_id>', methods=['POST'])
def beli(produk_id):
    for p in produk_list:
        if p['id'] == produk_id and p['stok'] > 0:
            p['stok'] -= 1
            pesan = f"Terima kasih! Kamu membeli {p['nama']}."
            break
    else:
        pesan = "Produk tidak ditemukan atau stok habis."

    content = f"""
        <h2>Transaksi Berhasil</h2>
        <p>{pesan}</p>
        <a href='/produk'>Kembali ke produk</a>
    """
    return render_template_string(layout, title="Pembelian", content=content)

# =========================
# Halaman Kontak
# =========================
@app.route('/kontak', methods=['GET', 'POST'])
def kontak():
    if request.method == 'POST':
        nama = request.form.get('nama')
        pesan = request.form.get('pesan')
        content = f"""
            <h2>Terima kasih, {nama}!</h2>
            <p>Pesan kamu telah kami terima:</p>
            <blockquote>{pesan}</blockquote>
            <a href='/'>Kembali ke beranda</a>
        """
        return render_template_string(layout, title="Pesan Diterima", content=content)

    # form input
    form = """
        <h2>Hubungi Kami</h2>
        <form method="POST">
            <label>Nama:</label><br>
            <input name="nama" required><br>
            <label>Pesan:</label><br>
            <textarea name="pesan" rows="4" cols="40" required></textarea><br>
            <button type="submit">Kirim Pesan</button>
        </form>
    """
    return render_template_string(layout, title="Kontak", content=form)

# =========================
# Jalankan aplikasi
# =========================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
