# DATETIME API

## Descripción

DATETIME es una API versátil que ofrece múltiples funcionalidades relacionadas con la manipulación y conversión de fechas y horas. Proporciona herramientas para convertir fechas a diferentes formatos, calcular diferencias entre fechas, obtener información detallada sobre zonas horarias, y mucho más.

### Funcionalidades Principales
- **Suma o resta intervalos de tiempo** a una fecha específica.
- **Conversión de fechas y horas** a diferentes zonas horarias.
- **Obtención de la fecha y hora actuales** en diversos formatos.
- **Cálculo del día de la semana** para una fecha específica.
- **Diferencia entre fechas y horas**.
- **Cálculo del número de semana ISO** para una fecha específica.

---

## Instalación

### Requisitos previos
1. Tener Python 3.7 o superior instalado.
2. Crear y activar un entorno virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate # En Linux/Mac
   venv\Scripts\activate # En Windows
   ```
3. Instalar las dependencias del proyecto:
   ```bash
   pip install -r requirements.txt
   ```

---

## Ejecución

Para ejecutar la API utiliza el siguiente comando:

```bash
uvicorn main:app --reload
```

El servidor estará disponible en: [http://127.0.0.1:8000](http://127.0.0.1:8000)

Para acceder a la documentación interactiva Swagger UI, visita:

- [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Endpoints Disponibles

### Inicio
- **`GET /`**
  - Proporciona una visión general de la API y redirige a la documentación interactiva.

### Funcionalidades

1. **`/addsubtract`**
   - **Descripción:** Suma o resta un intervalo de tiempo a una fecha específica.
   - **Método:** `GET` / `POST`

2. **`/convert`**
   - **Descripción:** Convierte una fecha y hora a diferentes zonas horarias.
   - **Método:** `GET` / `POST`

3. **`/current`**
   - **Descripción:** Devuelve la fecha y hora actuales en varios formatos.
   - **Método:** `GET`

4. **`/dayofweek`**
   - **Descripción:** Devuelve el día de la semana para una fecha específica.
   - **Método:** `GET` / `POST`

5. **`/difference`**
   - **Descripción:** Calcula la diferencia entre dos fechas y horas.
   - **Método:** `GET` / `POST`

6. **`/weeknumber`**
   - **Descripción:** Devuelve el número de semana ISO para una fecha específica.
   - **Método:** `GET` / `POST`