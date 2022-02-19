from pydantic import BaseModel as PydanticBaseModel
from pydantic import Field
from typing import Literal
import joblib
import pandas as pd
from fastapi import HTTPException


# Entrada del modelo.

# Adapten esta clase según cómo sean sus entradas.
# Miren su X, ¿cómo eran los datos con los que aprendió el modelo?
# Recuerden que las variables categoricas acá las dejaremos en un solo parametro.
# Miren cómo trabajamos con el salary_level para un ejemplo de variable categorica.

# Una variable binaria puede ser:
# binaria: int = Field(ge=0, le=1)
# O, binaria: bool

class ModelInput(PydanticBaseModel):
    """
    Clase que define las entradas del modelo
    """

    satisfaction_level: float = Field(description="Nivel de Satisfacción", ge=0, le=1)
    average_montly_hours: int = Field(
        description="Horas promedio trabajas al mes", ge=8, le=310
    )
    salary_level: Literal["high", "low", "medium"]

    # OPCIONAL: Poner el ejemplo para que en la documentación ya puedan de una lanzar la predicción.
    class Config:
        schema_extra = {
            "example": {
                "satisfaction_level": 0.69,
                "average_montly_hours": 242,
                "salary_level": "high",
            }
        }


class ModelOutput(PydanticBaseModel):
    """
    Clase que define las salidas del modelo
    """

    employee_left_proba: float = Field(
        description="Probabilidad de Renuncia del empleado", ge=0, le=1
    )

    class Config:
        schema_extra = {"example": {"employee_left_proba": 0.42}}


class APIModelBackEnd:
    """
    Esta clase maneja el back end de nuestro modelo de Machine Learning para la API en FastAPI
    """

    def __init__(self, satisfaction_level: float, average_montly_hours: int, salary_level: str):
        """
        Este método se usa al instanciar las clases
        Aquí, hacemos que pida los mismos parámetros que tenemos en ModelInput.
        Para más información del __init__ method, pueden leer en línea en sitios cómo
        https://www.udacity.com/blog/2021/11/__init__-in-python-an-overview.html
        Este método lo cambian según sus inputs
        """
        self.satisfaction_level = satisfaction_level
        self.average_montly_hours = average_montly_hours
        self.salary_level = salary_level

    def _load_model(self, model_filename: str = "modelo.pkl"):
        """
        Clase para cargar el modelo. Es una forma exótica de correr joblib.load pero teniendo funcionalidad con la API.
        Este método seguramente no lo van a cambiar, y si lo cambian, cambian el valor por defecto del string
        """
        # Asignamos a un atributo el nombre del archivo
        self.model_filename = model_filename
        try:
            # Se intenta cargar el modelo
            self.model = joblib.load(self.model_filename)
        except Exception:
            # Si hay un error, se levanda una Exception de HTTP diciendo que no se encontró el modelo
            raise HTTPException(
                status_code=404,
                detail=f"Modelo con el nombre {self.model_filename} no fue encontrado",
            )
        # Si todo corre ok, imprimimos que cargamos el modelo
        print(f"El modelo '{self.model_filename}' fue cargado exitosamente")

    def _prepare_data(self):
        """
        Clase de preparar lo datos.
        Este método convierte las entradas en los datos que tenían en X_train y X_test.
        Miren el orden de las columnas de los datos antes de su modelo.
        Tienen que recrear ese orden, en un dataframe de una fila.
        """
        # Aquí, ponemos los valores para los niveles de satisfacción.
        # Pueden manejar así las variables categoricas.
        # Revisen los X!!! De eso depende que valores hay aquí.
        # Para ver más o menos que valores pueden ser, en un data frame se le aplico pd.get_dummies, corran algo como:
        # X_test[[col for col in X_test.columns if "nombre de columna" in col]].drop_duplicates()

        salary_levels = {"high": [0, 0], "low": [1, 0], "medium": [0, 1]}

        # Hacemos el DataFrame.
        # Ponemos en columns lo que nos da de correr list(X_test.columns)
        # En data, ponemos los datos en el orden en que están en las columnas

        df = pd.DataFrame(
            columns=[
                "satisfaction_level",
                "average_montly_hours",
                "salary_level_low",
                "salary_level_medium",
            ],
            data=[
                [
                    self.satisfaction_level,
                    self.average_montly_hours,
                    *salary_levels[self.salary_level],
                ]
            ],
        )

        # Ese * en *salary_levels[self.salary_level] hace unpacking a la lista.
        # Sería como escribir salary_levels[self.salary_level][0], salary_levels[self.salary_level][1]
        return df

    def predict(self, y_name: str = "employee_left_proba"):
        """
        Clase para predecir.
        Carga el modelo, prepara los datos y predice.
        Acá, solo deberían cambiar en el input el valor por defecto de y_name (eso en rojo que dice employee_left_proba)
        para que sea coherente con su ModelOutput
        además de quizá, la línea
        prediction = pd.DataFrame(self.model.predict_proba(X)[:,1]).rename(columns={0:y_name})
        por
        prediction = pd.DataFrame(self.model.predict(X)).rename(columns={0:y_name})
        """
        self._load_model()
        x = self._prepare_data()
        prediction = pd.DataFrame(self.model.predict_proba(x)[:, 1]).rename(
            columns={0: y_name}
        )
        return prediction.to_dict(orient="records")