from behave import *
import requests
from flask import get_flashed_messages


@given('a {entidad} and a {id} to delete')
def step_impl(context, entidad, id):
    context.api_url = f'http://localhost:5000/delete/{entidad}/{id}'
    print('url :'+context.api_url)

@when('the registry is deleted of DB')
def step_impl(context):
    session = requests.Session()
    response = session.get(url=context.api_url, headers="")
    context.mensaje = response.text

@then('the return {message} is correct')
def step_impl(context, message):
    #assert (context.mensaje == message)
    assert (message in context.mensaje)