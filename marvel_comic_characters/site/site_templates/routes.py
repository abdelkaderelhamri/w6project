

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from marvel_comic_characters.forms import ComicForm
from marvel_comic_characters.models import Comic, db
from marvel_comic_characters.helpers import random_comic_generator

site = Blueprint('site', __name__, template_folder='site_templates')



@site.route('/')
def home():
    print("ooga booga in the terminal")
    return render_template('index.html')


@site.route('/profile', methods = ['GET', 'POST'])
@login_required
def profile():
    my_comic = ComicForm()

    try:
        if request.method == "POST" and my_comic.validate_on_submit():
            name = my_comic.name.data
            description = my_comic.description.data
            comics_appeared_in =  comics_appeared_in .data
            
            super_power=super_power.data
            date_created=datetime.utcnow.data
            
           
            if my_comic.comic.data:
                random_comic = my_comic.comic.data
            else:
                random_comic = random_comic_generator()          
            user_token = current_user.token

            comic = Comic(name, description, comics_appeared_in, super_power, date_created, user_token)

            db.session.add(comic)
            db.session.commit()

            return redirect(url_for('site.profile'))
    except:
        raise Exception("Comic not created, please check your form and try again!")
    
    current_user_token = current_user.token

    comics = Comic.query.filter_by(user_token=current_user_token)

    
    return render_template('profile.html', form=my_comic, comics = comics )