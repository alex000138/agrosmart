from flask import Blueprint, Flask, render_template, request, jsonify
from agrosmart.backend.extensions import db
from agrosmart.backend.app.models.models import (Variety,DiseaseResistance,Disease,Region,VarietyRegion,Author,Applicant,VarietyAuthor,VarietyApplicant,QualityParameters)

# Создание Blueprint
api_bp = Blueprint('api', __name__)

# Получение списка сортов
@api_bp.route('/varieties', methods=['GET'])
def get_varieties():
    try:
        # Логирование для отладки
        print("Attempting to query varieties...")
        varieties = Variety.query.all()
        print(f"Found {len(varieties)} varieties")
        
        if not varieties:
            return jsonify({"status": "success", "message": "No varieties found", "data": []}), 200
            
        result = []
        for variety in varieties:
            print(f"Processing variety: {variety.id} - {variety.name_main}")
            result.append({
                'id': variety.id,
                'name': variety.name_main,
                'type': variety.type_main,
                'code': variety.code,
                'origin': variety.origin
            })
        return jsonify({"status": "success", "data": result}), 200
    except Exception as e:
        print(f"Error in get_varieties: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Добавление нового сорта
@api_bp.route('/varieties', methods=['POST'])
def create_variety():
    try:
        # Получаем данные из запроса
        data = request.get_json()

        # Извлекаем данные
        name_main = data['название']
        type_main = data['Культура']
        code = data['Код сорта']
        description = data['Описание']
        origin = data['Оригинатор(ы)']
        registration_year = data['Год включения в реестр допущенных']
        patent_number = data.get('Номер патента')

        # Создаем новую модель сорта
        variety = Variety(
            name_main=name_main,
            type_main=type_main,
            code=code,
            description=description,
            origin=origin,
            registration_year=registration_year,
            patent_number=patent_number,
        )

        # Добавляем авторов
        authors = data.get('Автор(ы)', '').split(';')
        for author_name in [name.strip() for name in authors]:
            author = Author.query.filter_by(name=author_name).first()
            if author is None:
                author = Author(name=author_name)
                db.session.add(author)
            variety.authors.append(author)

        # Добавляем регионы
        regions = data.get('Регион(ы)', '').split(',')
        for region_name in [name.strip() for name in regions]:
            region = Region.query.filter_by(name_territory=region_name).first()
            if region is None:
                region = Region(name_territory=region_name)
                db.session.add(region)
            variety.regions.append(region)

        # Добавляем заявителей
        applicants = data.get('Заявители', '').split(';')
        for applicant_name in [name.strip() for name in applicants]:
            applicant = Applicant.query.filter_by(name=applicant_name).first()
            if applicant is None:
                applicant = Applicant(name=applicant_name)
                db.session.add(applicant)
            variety.applicants.append(applicant)

        # Добавляем устойчивость к заболеваниям
        diseases = data.get('устойчивость_к_заболеваниям', {})
        for disease_name, resistance_level in diseases.items():
            # Проверяем, существует ли заболевание
            disease = Disease.query.filter_by(name_dis=disease_name).first()
            if disease is None:
                # Если заболевания нет, создаем новое
                disease = Disease(name_dis=disease_name)
                db.session.add(disease)
            # Создаем связь между сортом и заболеванием
            disease_resistance = DiseaseResistance(
                variety=variety,
                disease=disease,
                resistance_level=resistance_level
            )
            db.session.add(disease_resistance)

        # Добавляем качество зерна
        quality_parameters = data.get('качество_зерна', {})
        if quality_parameters:
            # Создаем запись о качестве зерна
            quality = QualityParameters(
                variety=variety,
                protein_content=quality_parameters.get('протеин_содержание'),
                gluten_content=quality_parameters.get('gluten_содержание'),
                test_weight=quality_parameters.get('вес_в_мешке')
            )
            db.session.add(quality)

        # Сохраняем изменения
        db.session.add(variety)
        db.session.commit()

        return jsonify({"status": "success", "message": "Сорт успешно добавлен"}), 201

    except Exception as e:
        # Откат изменений в случае ошибки
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
