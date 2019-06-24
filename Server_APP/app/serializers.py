from app.models import Usuario, Pelicula, Resena
from rest_framework.serializers import ModelSerializer

class UsuarioSerializer(ModelSerializer):
    class Meta:
        model = Usuario
        fields = "__all__"

class PeliculaSerializer(ModelSerializer):
    class Meta:
        model = Pelicula
        fields = "__all__"

class ResenaSerializer(ModelSerializer):
    class Meta:
        model = Resena
