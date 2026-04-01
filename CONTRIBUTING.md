# Contribuir al Proyecto

¡Gracias por tu interés en contribuir! Este documento contiene pautas para contribuir.

## Proceso de Contribución

1. **Fork el repositorio**
   ```bash
   git clone https://github.com/tu-usuario/Analizador-Fortaleza-Contraseñas.git
   cd Analizador-Fortaleza-Contraseñas
   ```

2. **Crear una rama para tu feature**
   ```bash
   git checkout -b feature/mi-feature
   ```

3. **Hacer cambios y tests**
   ```bash
   # Instalar dependencias de desarrollo
   pip install -r requirements-dev.txt
   
   # Ejecutar tests
   pytest tests/ -v
   
   # Verificar código con linter
   flake8 utils/ app/
   ```

4. **Commit con mensajes descriptivos**
   ```bash
   git commit -m "Add feature: descripción clara de los cambios"
   ```

5. **Push a tu rama**
   ```bash
   git push origin feature/mi-feature
   ```

6. **Crear un Pull Request**
   - Describe los cambios de forma clara
   - Referencia issues relacionados (si existen)
   - Asegúrate de que todos los tests pasen

## Estándares de Código

- **PEP 8**: Sigue la guía de estilos Python
- **Docstrings**: Toda función debe tener docstring
- **Type hints**: Usa anotaciones de tipo cuando sea posible
- **Tests**: Todo código nuevo debe incluir tests
- **Coverage**: Intenta mantener >80% de cobertura

## Reportar Bugs

- Usa GitHub Issues
- Describe el bug claramente
- Incluye pasos para reproducir
- Menciona tu sistema operativo y versión de Python

## Solicitar Features

- Abre un GitHub Issue con el label `enhancement`
- Describe la feature y por qué es útil
- Proporciona ejemplos de uso si es posible

## Código de Conducta

- Sé respetuoso
- Acepta críticas constructivas
- Ayuda a otros usuarios
- Respeta la privacidad y seguridad

---

¡Gracias por contribuir! 🚀
