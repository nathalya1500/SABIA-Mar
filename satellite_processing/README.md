# Satellite Processing

El paquete Satellite Processing es una herramienta para el procesamiento de imágenes satelitales de nivel 2 (L2) a nivel 3 (L3). Proporciona funciones para el bineado espacial y temporal de datos satelitales, siguiendo las recomendaciones del informe "Vol. 32: Level-3 SeaWiFS Data Products: Spatial and Temporal Binning Algorithms" de la NASA.

## Instalación

Para instalar el paquete, puedes ejecutar el siguiente comando:

```bash
pip install satellite_processing
```

Asegúrate de tener las dependencias necesarias mencionadas en el archivo requirements.txt.

## Uso
Aquí tienes un ejemplo básico de cómo usar el paquete para realizar el bineado espacial y temporal de imágenes satelitales:
```python
from satellite_processing.binning.spatial_binning import initbin, lat2row, constrain_lon, rowlon2bin
from satellite_processing.binning.temporal_binning import get_spatial_bin_vectorized, temporal_binning

# Código de ejemplo para procesar las imágenes satelitales

# ...
```
Puedes encontrar más ejemplos de uso en el directorio examples del repositorio

## Contribución
Si deseas contribuir a este proyecto, por favor sigue las siguientes pautas:

Realiza un fork del repositorio.
Crea una rama nueva para tu contribución: git checkout -b mi-nueva-funcionalidad.
Realiza tus cambios y pruebas.
Asegúrate de que tu código siga las guías de estilo y está correctamente documentado.
Realiza un pull request con tus cambios.

## Soporte
Si tienes alguna pregunta, problema o sugerencia, no dudes en abrir un issue en el repositorio o contactarnos por correo electrónico.

## Licencia
Este proyecto está bajo la Licencia MIT. Consulta el archivo LICENSE para más detalles.