from pydantic import BaseModel,Field
from typing import Literal


# create a root response object
class RootResponse(BaseModel):
    """creates the payload for the root endpoint."""
    message: str = Field(..., description="root message",
                         examples=["we are live!"])
    

# create a model response object
class ModelResponse(BaseModel):
    """
    Response object for the student dropout prediction model.
    """
    predicted_Target: Literal["Dropout", "Enrolled", "Graduate"] = Field(
        ...,
        description="Predicted Target: Dropout, Enrolled, or Graduate",
        example="Graduate"
    )

    # Marital status application-mode application-order course daytime/evening attendance previous-qualification
    # nacionality mother's qualification  father's qualification mother's occupation father's occupation
    # displaced educational special needs debtor tuition fees up to date gender scholarship holder
    # age at enrollment international Curricular units 1st sem (credited) Curricular units 1st sem (enrolled)
    # Curricular units 1st sem (evaluations) Curricular units 1st sem (approved) Curricular units 1st sem (grade)
    # Curricular units 1st sem (without evaluations) Curricular units 2nd sem (credited) Curricular units 2nd sem (enrolled)
    # Curricular units 2nd sem (evaluations) Curricular units 2nd sem (approved) Curricular units 2nd sem (grade)
    # Curricular units 2nd sem (without evaluations) Unemployment rate Inflation rate GDP


# create the model request object
class ModelRequest(BaseModel):
    """
    creates the request object for the model prediction
    """
    Marital_status: int = Field(...,
                                description="Marital status of the student: 0 = Single, 1 = Married, 2 = Divorced, 3 = Widowed",
                                ge=0,le=3,example=1)
    Application_mode: int = Field(...,
                                  description="Application mode of the student: 1 = Online, 2 = In-person, 3 = Referral, 4 = Other",
                                  ge=1,le=4,example=1)
    Application_order: int = Field(...,
                                   description="Application order of the student: Indicates the ranked preference (e.g., 1 = first choice, 2 = second choice, etc.)",
                                   ge=1,example=1)
    Course: int = Field(
    ...,
    description=(
        "Course code for the program the student is enrolled in. "
        "Mappings: 1 = Agronomy, 2 = Design, 3 = Education, 4 = Nursing, "
        "5 = Management, 6 = Social Service, 7 = Tourism, 8 = Veterinary, "
        "9 = Computer Science, 10 = Law, 11 = Economics, 12 = Biology, "
        "13 = Chemistry, 14 = Physics, 15 = Mathematics, 16 = Psychology, "
        "17 = Medicine, 18 = Engineering, 19 = Architecture, 20 = Sociology."
    ),
    ge=1,
    le=20,
    example=9
)
    Daytime_evening_attendance: int = Field(...,
                                            description="Attendance type of the student: 0 = Daytime, 1 = Evening",
                                            ge=0,le=1,example=0)
    Previous_qualification: int = Field(
    ...,
    description="Previous qualification of the student: 1 = High school, 2 = Bachelor's degree, 3 = Master's degree, 4 = Other",
    ge=1,
    le=4,
    example=1
) 
    Nacionality: int = Field(...,
                             description="Nationality of the student: 1 = Domestic, 2 = International, 3 = Other",
                             ge=1,le=3,example=1)
    Mothers_qualification: int = Field(...,
                                       description="Mother's highest qualification: 1 = None, 2 = Primary education, 3 = Secondary education, 4 = Bachelor's degree, 5 = Master's degree, 6 = Doctorate, 7 = Other",
                                       ge=1,le=7,example=3)
    Fathers_qualification: int = Field(...,
                                       description="Father's highest qualification: 1 = None, 2 = Primary education, 3 = Secondary education, 4 = Bachelor's degree, 5 = Master's degree, 6 = Doctorate, 7 = Other",
                                       ge=1,le=7,example=3)
    Mothers_occupation: int = Field(...,
                                    description="Mother's occupation: 1 = Unemployed, 2 = Self-employed, 3 = Employed in private sector, 4 = Employed in public sector, 5 = Retired, 6 = Other",
                                    ge=1,le=6,example=3)
    Father_occupation: int = Field(...,
                                   description="fathers's occupation: 1 = Unemployed, 2 = Self-employed, 3 = Employed in private sector, 4 = Employed in public sector, 5 = Retired, 6 = Other",
                                   ge=1,le=6,example=3)
    Displaced: int = Field(...,
                           description="Indicates if the student has been displaced: 0 = No, 1 = Yes",
                           ge=0,le=1,example=0)
    Education_special_needs: int = Field(...,
                                         description="Indicates if the student has special educational needs: 0 = No, 1 = Yes",
                                         ge=0,le=1,example=0)
    Debtor: int = Field(...,
                        description="Indicates if the student has any outstanding debts: 0 = No, 1 = Yes",
                        ge=0,le=1,example=0)
    Tuition_fees_up_to_date: int = Field(...,
                                         description="Indicates if the student's tuition fees are paid up to date: 0 = No, 1 = Yes",
                                         ge=0,le=1,example=1)
    Gender: int = Field(...,
                        description="Gender of the student: 0 = Female, 1 = Male, 2 = Other",
                        ge=0,le=2,example=1)
    Scholarship_holder: int = Field(...,
                                    description="Indicates if the student is a scholarship holder: 0 = No, 1 = Yes",
                                    ge=0,le=1,example=0)
    Age_at_enrollment: int = Field(...,
                                   description="Age of the student at the time of enrollment (in years)",
                                   ge=15,le=100,example=18)
    International: int = Field(...,
                               description="Indicates if the student is an international student: 0 = No, 1 = Yes",
                               ge=0,le=1,example=0)
    Curricular_units_1st_sem_credited: int = Field(...,
                                                   description="Number of curricular units credited in the 1st semester",
                                                   ge=0,le=50,example=0)
    Curricular_units_1st_sem_enrolled: int = Field(...,
                                                   description="Number of curricular units enrolled in the 1st semester",
                                                   ge=0,le=50,example=5)
    Curricular_units_1st_sem_evaluations: int = Field(...,
                                                      description="Number of curricular units evaluated in the 1st semester",
                                                      ge=0,le=50,example=5)
    Curricular_units_1st_sem_approved: int = Field(...,
                                                   description="Number of curricular units approved in the 1st semester",
                                                   ge=0,le=50,example=5)
    Curricular_units_1st_sem_grade: float = Field(...,
                                                  description="Average grade for curricular units in the 1st semester (0 to 20 scale)",
                                                  ge=0.0,le=20.0,example=14.5)
    Curricular_units_1st_sem_without_evaluations: int = Field(...,
                                                              description="Number of curricular units in the 1st semester without evaluations",
                                                              ge=0,le=50,example=0)
    Curricular_units_2nd_sem_credited: int = Field(...,
                                                   description="Number of curricular units credited in the 2nd semester",
                                                   ge=0,le=50,example=0)
    Curricular_units_2nd_sem_enrolled: int = Field(...,
                                                   description="Number of curricular units enrolled in the 2nd semester",
                                                   ge=0,le=50,example=5)
    Curricular_units_2nd_sem_evaluations: int = Field(...,
                                                      description="Number of curricular units evaluated in the 2nd semester",
                                                      ge=0,le=50,example=5)
    Curricular_units_2nd_sem_approved: int = Field(...,
                                                   description="Number of curricular units approved in the 2nd semester",
                                                   ge=0,le=50,example=4)
    Curricular_units_2nd_sem_grade: float = Field(...,
                                                  description="Average grade of curricular units in the 2nd semester (0.0 to 20.0 scale)",
                                                  ge=0.0,le=20.0,example=13.5)
    Curricular_units_2nd_sem_without_Evaluations: int = Field(...,
                                                              description="Number of curricular units in the 2nd semester without any evaluations",
                                                              ge=0,le=50,example=0)
    Unemployment_rate: float = Field(...,
                                     description="Unemployment rate at the time of enrollment (percentage)",
                                     ge=0.0,le=100.0,example=7.5)
    Inflation_rate: float = Field(...,
                                  description="Inflation rate at the time of enrollment (percentage)",
                                  ge=-50.0,le=100.0,example=2.3)
    GDP: float = Field(...,
                       description="Gross Domestic Product (GDP) growth rate at the time of enrollment (in percentage)",
                       ge=-100.0,le=100.0,example=2.5)
    