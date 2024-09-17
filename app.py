from flask import Flask, render_template, request, flash, redirect, url_for
import instaloader

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    kullaniciAdi = request.form['username']
    sifre = request.form['password']
    
    instagram = instaloader.Instaloader()

    try:
        instagram.login(kullaniciAdi, sifre)
        
        profil = instaloader.Profile.from_username(instagram.context, kullaniciAdi)
        
        takipciler = profil.get_followers()
        takipEdilenler = profil.get_followees()
        
        takipciList = [i.username for i in takipciler]
        takipEdilenList = [i.username for i in takipEdilenler]
        
        takip_etmeyenler = [i for i in takipEdilenList if i not in takipciList]
        
        return f"Takip etmeyenler: {', '.join(takip_etmeyenler)}"
    
    except instaloader.exceptions.BadCredentialsException:
        flash('Kullanıcı adı veya şifre yanlış, lütfen tekrar deneyin.', 'error')
        return redirect(url_for('index'))
    
    except instaloader.exceptions.ConnectionException:
        flash('Instagram ile bağlantı kurulamadı. Lütfen daha sonra tekrar deneyin.', 'error')
        return redirect(url_for('index'))
    
    except Exception as e:
        flash(f'Bilinmeyen bir hata oluştu: {str(e)}', 'error')
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
