# Seguridad

## Reportar Vulnerabilidades

**IMPORTANTE**: Si descubres una vulnerabilidad de seguridad, **NO** la reportes en GitHub Issues.

Por favor, envía un email a tu-email@ejemplo.com con:
- Descripción de la vulnerabilidad
- Pasos para reproducir
- Impacto potencial
- (Opcional) Sugerencia de fix

## Información de Seguridad del Proyecto

### Cifrado

- **Algoritmo**: AES-256-CBC (estándar militar)
- **Derivación de claves**: PBKDF2-HMAC-SHA256 con 100,000 iteraciones
- **Almacenamiento**: 100% local, nunca en la nube
- **Transmisión**: Los datos nunca se envían a internet

### Prácticas de Seguridad

1. **Entorno aislado**: La app funciona completamente offline
2. **No tracking**: Sin analíticos, sin telemetría
3. **Código auditado**: Los módulos de cifrado pueden ser revisados
4. **Dependencias mínimas**: Solo lo necesario

### Limitaciones

- Este es un proyecto educativo
- Para producción, usa gestores de contraseñas profesionales (Bitwarden, 1Password)
- No proporciona sincronización entre dispositivos
- No tiene recuperación ante pérdida de master password

### Buenas Prácticas

1. **Guarda tu Master Password**: Sin ella, pierdes acceso
2. **No compartas contraseñas**: Usa esta herramienta solo personalmente
3. **Mantén Python actualizado**: Especialmente las dependencias de cryptography
4. **Respaldo local**: Copia los archivos de datos encriptados

---

**Última actualización**: 2024
