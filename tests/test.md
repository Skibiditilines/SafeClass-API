# Registro de Pruebas — SafeClass API

Este archivo documenta las pruebas manuales y de integración realizadas sobre los endpoints de la API.

---

## Tabla de pruebas

| ID Prueba | Función / Endpoint | Descripción | Datos de entrada | Resultado esperado | Resultado obtenido | Estado | Fecha | Responsable |
| :-------: | :----------------- | :---------- | :--------------- | :----------------- | :----------------- | :----: | :---: | :---------: |
| P-01 | `fun_01` — POST /auth/signup | Registro exitoso de un académico | nombre, institución, correo, contraseña, municipio válidos | 201 - Usuario creado | | | | |
| P-02 | `fun_02` — POST /auth/signup | Registro con correo duplicado | correo ya registrado | 400 - Error de duplicado | | | | |
| P-03 | `fun_03` — POST /auth/login | Login exitoso | correo y contraseña correctos | 200 - Token JWT | | | | |
| P-04 | `fun_04` — POST /auth/login | Login con credenciales incorrectas | contraseña incorrecta | 401 - No autorizado | | | | |
| P-05 | `fun_05` — POST /municipios | Listar todos los municipios | (ninguno) | 200 - Lista de municipios | | | | |
| P-06 | `fun_06` — GET /municipios/{id} | Obtener municipio por ID válido | id existente | 200 - Datos del municipio | | | | |
| P-07 | `fun_07` — GET /weather | Clima actual del municipio del usuario | Token JWT válido | 200 - Datos climáticos | | | | |
| P-08 | `fun_08` — GET /weather/{fecha} | Pronóstico para fecha válida (≤5 días) | fecha en YYYY-MM-DD | 200 - Pronóstico de la fecha | | | | |
| P-09 | `fun_09` — POST /suspensions | Registrar una suspensión | fecha del día actual | 201 - Suspensión registrada | | | | |
| P-10 | `fun_10` — GET /suspensions | Listar suspensiones del usuario | Token JWT válido | 200 - Lista de suspensiones | | | | |
| P-11 | `fun_10` — GET /suspensions/{fecha} | Suspensión por fecha específica | fecha en YYYY-MM-DD | 200 - Suspensión o null | | | | |

---

## Notas

- **Estado:** Pasó / Falló / Pendiente
- Las pruebas automatizadas se encuentran en `tests/test_*.py` y se ejecutan con `pytest`.
