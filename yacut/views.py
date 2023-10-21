from flask import render_template, redirect, request, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap
from .utils import get_unique_short_id


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if request.method == 'POST':
        if not form.validate_on_submit():
            return render_template('index.html', form=form)
        if form.custom_id.data is None or form.custom_id.data == '':
            short_link = get_unique_short_id()
        else:
            short_link = form.custom_id.data
        url_map = URLMap(original=form.original_link.data, short=short_link)
        db.session.add(url_map)
        db.session.commit()
        return render_template(
            'index.html',
            form=form,
            url=url_for(
                'redirect_from_short_link',
                short_id=short_link,
                _external=True
            )
        )
    return render_template('index.html', form=form)


@app.route('/<string:short_id>', methods=['GET', ])
def redirect_from_short_link(short_id):
    return redirect(
        URLMap.query.filter_by(short=short_id).first_or_404().original
    )
