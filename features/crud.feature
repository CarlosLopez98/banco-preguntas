Feature: CRUD

Scenario Outline: Add registry
    Given a <entidad> to add a registry
    When the registry is added to DB
    Then the return <message> is correct

    Examples: data
    | entidad     | message                                  |
    | usuarios    | El registro se eliminó con éxito         |
    | usuarios    | El registro que desea eliminar no existe |
    | roles       | El registro se eliminó con éxito         |
    | roles       | El registro que desea eliminar no existe |

Scenario Outline: Delete registry
    Given a <entidad> and a <id> to delete
    When the registry is deleted of DB
    Then the return <message> is correct

    Examples: data
    | entidad     | id    | message                                  |
    | usuarios    | 3     | El registro se eliminó con éxito         |
    | usuarios    | 3     | El registro que desea eliminar no existe |
    | respuestas  | 3     | El registro se eliminó con éxito         |
    | respuestas  | 3     | El registro que desea eliminar no existe |