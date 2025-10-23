# Project TODOs & Improvement Ideas

List of tasks, enhancements, and ideas for future development.

Each item includes a rationale to help with evaluation and prioritization.

---

## TO-DOs

### Add key specs under `docs/specs`

**Rationale:**  
Documenting specifications such as functional requirements, system architecture, and entity-relationship diagrams in `docs/specs` will provide clear guidance for development, improve onboarding, and ensure alignment on system goals and design decisions.

### Sanitize post contents before saving or displaying

**Rationale:**  
Unsanitized content can lead to security vulnerabilities such as cross-site scripting (XSS). Sanitizing post contents ensures user safety and data integrity, especially when displaying user-generated content.

### Implement logging across all layers

**Rationale:**  
Logging is essential for monitoring application behavior, diagnosing issues, and auditing actions. Implementing structured logging across all layers will improve maintainability, facilitate debugging, and help with compliance and security reviews.

### Document endpoints for better API docs

**Rationale:**  
Providing summaries and descriptions for API endpoints improves the generated OpenAPI documentation, making it easier for developers and consumers to understand the API's capabilities and usage.

### Implement key integration tests

**Rationale:**  
Integration tests verify that different components of the application work together as expected. Implementing key integration tests will help catch issues that unit tests may miss, improve reliability, and ensure that critical user flows function correctly.

### Refactor test function names to include expected behaviour

**Rationale:**  
Using descriptive test function names that follow the pattern `test_<action>_should_<expected_result>` improves clarity and maintainability. It makes the expected behavior of each test explicit and aligns with common best practices in the testing community.

### Separate DTOs from domain models

**Rationale:**  
Separating DTOs (Data Transfer Objects) from domain models improves code organization, clarity, and maintainability. It helps prevent accidental coupling between layers and makes it easier to manage changes as the codebase grows. Move DTOs such as `CreatePostData` and `UpdatePostData` from `models.py` to a dedicated file (e.g., `dtos.py`).

---

## Ideas

### Add user reputation system

**Rationale:**  
A user reputation system could help identify trustworthy users and improve the quality of content. It could be based on factors such as the number of upvotes, downvotes, and the quality of content.

### Add content moderation tools

**Rationale:**  
Content moderation tools could help prevent the spread of harmful or inappropriate content. It could be based on factors such as the presence of hate speech, nudity, or violence.

### Add real-time collaboration features

**Rationale:**  
Real-time collaboration features could help users work together more effectively. It could be based on factors such as the ability to edit and comment on content in real-time.

### Refactor monolith into microservices architecture

**Rationale:**  
Migrating to a microservices architecture could improve scalability, fault isolation, and team autonomy. It would allow independent deployment and scaling of features, but also introduces complexity in service communication, deployment, and monitoring.

This idea should be evaluated based on future growth and operational needs.

### Implement a feature flag mechanism

**Rationale:**  
A feature flag system allows enabling or disabling features at runtime without redeploying the application. This improves flexibility for testing, gradual rollouts, and quick rollback of problematic features, enhancing both development agility and operational control.

---