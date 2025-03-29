from flask import Blueprint, render_template, request, redirect, url_for, jsonify
from agrosmart.backend.extensions import db
from ..models.models import Variety

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Главная страница с поиском сортов"""
    query = request.args.get('query', '')
    
    try:
        latest_varieties = Variety.query.order_by(Variety.id.desc()).limit(5).all()
        results = Variety.query.filter(Variety.name_main.ilike(f'%{query}%')).all() if query else []
        
        return render_template(
            'index.html',
            latest_varieties=latest_varieties,
            results=results,
            query=query
        )
    except Exception as e:
        print(f"Ошибка при загрузке страницы: {str(e)}")
        return render_template('500.html'), 500

@main_bp.route('/add_info', methods=['POST'])
def add_info():
    """Добавление нового сорта"""
    try:
        new_variety = Variety(
            name_main=request.form['name'],
            type_main=request.form['type'],
            code=request.form['code'],
            description=request.form['description'],
            origin=request.form['origin'],
            registration_year=request.form['year']
        )
        
        db.session.add(new_variety)
        db.session.commit()
        return redirect(url_for('main.index'))
    except Exception as e:
        db.session.rollback()
        print(f"Ошибка при добавлении сорта: {str(e)}")
        from flask import abort
        abort(500)  # Будет использовать стандартный обработчик ошибок Flask

# Остальные маршруты остаются аналогичными с заменой main на main_bp
@main_bp.route('/tables')
def tables():
    all_varieties = db.session.query(
        Variety.id,
        Variety.name_main.label('name'),
        Variety.type_main.label('type'),
        Variety.code,
        Variety.registration_year
    ).order_by(Variety.id).all()
    return render_template('tables.html', varieties=all_varieties)

@main_bp.route('/about')
def about():
    """Страница 'О нас'"""
    return render_template('about.html')

@main_bp.route('/test-db')
def test_db():
    from ..models.models import Variety
    count = Variety.query.count()
    return f'В базе {count} записей'
