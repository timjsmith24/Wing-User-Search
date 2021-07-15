from flask import Flask, render_template, redirect, flash
from flask_bootstrap import Bootstrap
from forms import UserSearchForm
from user_search import clientSearch

app = Flask(__name__)
app.config['SECRET_KEY'] = 'thisIsaTest'
bootstrap = Bootstrap(app)



@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])

def index():
    global refresh_page
    refresh_page = True
    form = UserSearchForm()
    if form.validate_on_submit():
        return redirect('/user/{}/{}'.format(form.site.data, form.user.data))
    return render_template('index.html', form=form)

@app.route('/user/<site>/<user>', methods=['GET', 'POST'])
def user(site, user):
    form = UserSearchForm()
    if form.validate_on_submit():
        return redirect('/user/{}/{}'.format(form.site.data, form.user.data))
    try:
        ap_data = clientSearch(site,user)
    except TypeError as e:
        flash(e)
        return render_template('index.html', form=form)
    except ValueError as e:
        flash(e)
        return render_template('index.html', form=form)
    if not ap_data:
        ### print message on screen
        flash('Client {} not found at {}'.format(user, site))
        return render_template('index.html', form=form)
    else:
        return render_template("user_info.html",
        site = site,
        user = user,
        user_ip = ap_data['ipaddr'],
        user_mac = ap_data['mac'],
        ap_name = ap_data['apname'],
        ap_mac = ap_data['apmac']
        )

if __name__ == "__main__":
    app.run()	