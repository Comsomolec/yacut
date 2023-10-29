from flask import flash, render_template, redirect, url_for
from wtforms.validators import ValidationError

from . import app
from .forms import URLMapForm
from .models import URLMap
from settings import REDIRECT_FROM_SHORT_LINK


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        url_map = URLMap.create(
            original=form.original_link.data, short=form.custom_id.data
        )
    except ValidationError as error:
        flash(error)
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        url=url_for(
            REDIRECT_FROM_SHORT_LINK,
            short_id=url_map.short,
            _external=True
        )
    )


@app.route('/<string:short_id>', methods=['GET', ])
def redirect_from_short_link(short_id):
    return redirect(URLMap.get_or_404(short_id).original)
