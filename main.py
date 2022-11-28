#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr, PaymentCardNumber

# FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path
from fastapi import status

app = FastAPI()


# Models

class Hair_Color(Enum):
    white = 'white'
    brown = 'brown'
    black = 'black'
    blonde = 'blonde'
    red = 'red'


class Location(BaseModel):
    city : str = Field(
        ...,
        max_length = 120, 
        example = 'Bogotá'
    )
    state : str = Field(
        ...,
        max_length = 120,  
        example = 'Cundinamarca'
    )
    country: str = Field(
        ...,
        max_length = 120,  
        example = 'Colombia'
    )


class PersonBase(BaseModel):
    first_name : str = Field(
        ..., 
        min_length = 1,
        max_length = 50,
        example = 'Oscar'
        )

    last_name : str = Field(
        ..., 
        min_length = 1,
        max_length = 50,
        example = 'Piedrahita'
        )

    age : int = Field(
        ...,
        gt = 0,
        le = 115,
        example = '56'
    )
    hair_color : Optional[Hair_Color] = Field(default = None, example = 'black')
    is_married : Optional[bool] = Field( default= None, example = False)
    email : EmailStr
    payment : PaymentCardNumber = Field(
        ...,
        example = '1234567788534679'
    )
    blood_type: Optional[str] = Field(
        ...,
        min_length = 2,
        max_length = 3,
        example = 'o+'
    )


class Person(PersonBase):
    password : str = Field(
        ...,
        min_length=8
    )
    

class PersonOut(PersonBase):
    pass



@app.get(
    path = '/',
    status_code=status.HTTP_200_OK
    )
def home():
    return {'Hello': 'World'}




# Request and Response body 

@app.post(
    path='/person/new',
    response_model = PersonOut,
    status_code=status.HTTP_201_CREATED
    )
def create_person(person:Person = Body(...)):
    return person



# Validations: Query Parameters 

@app.get('/person/detail')

def show_person(

    name : Optional[str] = Query(
    None,
    min_length=1, 
    max_length=50,
    title = 'Person Name',
    description = 'This is the person name. It is between 1 and 50 characters',
    example = 'Rocío'
    ),


    age : int = Query(
        ...,
        title = 'Person Name',
        description = 'This is the person age. It is required',
        example=89
        )
):

    return {name:age} 



# Validations: Path Parameters

@app.get(
    path='/person/detail/{person_id}',
    status_code=status.HTTP_200_OK
    )
def show_person(

    person_id: int = Path(

        ...,
        gt=0,
        title = 'Person Name',
        description = 'This is the person tweet' ,
        example=123
        )

):
    return{person_id: 'It exists!'}



# Validations : Request Body 

@app.put('/person/{person_id}')
def update_person(
    person_id : int = Path(
        ...,
        title = 'Person ID',
        description = 'This is the person ID',
        gt = 0,
        example=123 
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results


