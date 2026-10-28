Feature: Petstore API

  Background:
    Given the API base URL

  Scenario: 1. Create pet
    When I POST "/pet" with pet body
    Then status is 200
    And body has "id"

  Scenario: 2. Get pet by ID
    Given a pet exists
    When I GET "/pet/{pet_id}"
    Then status is 200
    And body has "name"

  Scenario: 3. Get pet by invalid ID
    When I GET "/pet/999999999"
    Then status is 404

  Scenario: 4. Update pet
    Given a pet exists
    When I PUT "/pet" with pet body and id
    Then status is 200

  Scenario: 5. Get inventory
    When I GET "/store/inventory"
    Then status is 200

  Scenario: 6. Place order
    When I POST "/store/order" with order body
    Then status is 200
    And body has "id"

  Scenario: 7. Get order by ID
    Given an order exists
    When I GET "/store/order/{order_id}"
    Then status is 200

  Scenario: 8. Create user
    When I POST "/user" with user body
    Then status is 200

  Scenario: 9. Get user by username
    Given a user exists
    When I GET "/user/{username}"
    Then status is 200
    And body has "username"

  Scenario: 10. Login user
    Given a user exists
    When I GET "/user/login" with user credentials
    Then status is 200