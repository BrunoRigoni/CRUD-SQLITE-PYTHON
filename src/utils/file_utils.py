import os
import uuid
from werkzeug.utils import secure_filename

# Configurações para upload de arquivos
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}


def allowed_file(filename):
    """Verifica se o arquivo tem uma extensão permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def save_image(file):
    """Salva uma imagem no diretório de uploads"""
    if file and allowed_file(file.filename):
        # Gerar nome único para o arquivo
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

        # Criar pasta de uploads se não existir
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        file.save(filepath)
        return unique_filename
    return None


def delete_image(filename):
    """Deleta uma imagem do diretório de uploads"""
    if filename:
        try:
            image_path = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.exists(image_path):
                os.remove(image_path)
                return True
        except Exception as e:
            print(f"Erro ao deletar imagem: {e}")
    return False
