Feature: CRUD

Scenario Outline: Delete register
    Given a <entidad> and a <id> to delete
    When the register is deleted of DB
    Then the return <message> is correct

    Examples: data
    | entidad     | id    | message                                  |
    | usuarios    | 3     | El registro se eliminó con éxito         |
    | usuarios    | 3     | El registro que desea eliminar no existe |
    | roles       | 3     | El registro se eliminó con éxito         |
    | roles       | 3     | El registro que desea eliminar no existe |