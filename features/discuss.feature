Feature: Discuss with AI Assitant about a given PDF document
    In order to extract valuable information from a PDF document
    As a User
    I want to ask questions and to get answers in natural language about the content of the PDF document


Scenario: Get references on the content used by AI Assistant to produce an answer to a question
    Given a PDF document
    When I ask a question on the content to the AI Assistant
    Then I get an answer with the references on the content (page, lines)

