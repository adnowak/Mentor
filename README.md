
## Core Services

### API Gateway
- Route management
- Rate limiting
- Request validation
- Load balancing

### Mentoring Engine
- Learning path generation
- Progress analytics
- Custom learning paths
- Chat with the mentoring engine

### Domain Services
- Specialized knowledge handlers
    - Access to different knowledge sources
- Domains can be interdependent
- Test generation
- Interactive exercises

### AI Orchestrator
- LLM integration
- Context management
- Response optimization

### The process of mentoring
- The user can specify their reason for learning and the goal
- The mentoring engine selects the domains based on the user's goal
- The mentoring engine evaluates the user's knowledge in each domain
- The mentoring engine generates a learning path for the user based on the selected domains and the user's knowledge
- The user goes through the learning path
    - The user has access to a chat with the mentoring engine
    - The mentoring engine provides feedback
    - The user can see the progress
    - The learning path never ends, it is a continous path
    - The learing path is adjusted to the user's knowledge evaluated by the mentoring engine

### Domain model
- A domain is a domain of knowledge
- A domain has a name
- A domain has a set of domain dependencies which are the domains in which the gaps could impact the learning of the current domain
- first example:
```yaml
domain:
    name: keycloak
    dependencies:
        - encryption
        - authentication
        - authorization
```
- second example:
```yaml
domain:
    name: encryption
    dependencies:
        - logic
        - algebra
```
- third example:
```yaml
domain:
    name: programming
    dependencies:
        - basic math
        - basic logic
        - english
```

### Mentee model
- A mentee is a user who is learning
- A set of keywords describing the user's knowledge and gaps for each domain
- Used by the mentoring engine as a context for the learning path generation prompt
- Features are optional and can be used to personalize the learning path
- The mentor can save the mentee's atypical preferences based on the questions asked by the mentee during the mentoring session
- yaml example:
```yaml
mentee:
    name: John Doe
    goals:
        short_term:
            - "Implement secure authentication in my app"
        long_term:
            - "Become a security specialist"
    features:
        - New developer
        - Located in Poland
        - Likes to learn by doing
        - Is allergic to Microsoft products
    knowledge:
        keycloak:
            skills:
                - jwt
                - oauth2
            gaps
                - iss claim
                - sub claim
                - slower learning pace
        spring-boot:
            skills:
                - spring boot
                - spring security
            gaps:
                - token validation
                - token refresh
    atypical-preferences:
        - "I want to learn about keycloak 11 integration in spring boot with svelte"
```

### Test result model
- It contains the domain of the test
- It contains the skills that the user has demonstrated
- It contains the gaps identified by the test
- It contains the atypical findings of the mentoring engine found during the test
- yaml example:
```yaml
test_result:
    domain: keycloak
    skills:
        - jwt
        - oauth2
    gaps:
        - iss claim
    atypical_findings:
        - The user is not able to understand how the iss claim is used for the token validation
```

### Exercise result model
- It contains the domain of the exercise
- It contains the skills that the user has demonstrated
- It contains the gaps identified by the exercise
- It contains the atypical findings of the mentoring engine found during the exercise
- yaml example:
```yaml
exercise_result:
    domain: keycloak
    skills:
        - jwt
        - oauth2
    gaps:
        - integration with spring boot
```

### Learning path summary model
- A learning path summary is a summary of history of the learning path
- It contains the goal of the user
- It contains the domains that the user has learned
- It contains the summary of results of tests and exercises that the user has completed
- It contains the atypical findings of the mentoring engine found during the mentoring session
- The mentoring engine will generate a learning path summary after each mentoring session
- The learning path summary will be used to generate the next learning path
- The learning path summary will be used to generate the human readable report for the mentee
- yaml example:
```yaml
learning_path_summary:
    goal:
        - "Implement secure authentication in my app"
    domains:
        - keycloak
        - spring boot
    results:
        - test_result:
            domain: keycloak
            skills:
                - jwt
                - oauth2
            gaps:
                - iss claim
                - sub claim
            atypical_findings:
                - iss claim
                - sub claim
```

## Technology Stack

- **API Gateway**: NGINX
- **Services**: Spring Boot
- **Auth Service**: Keycloak
- **Frontend**: Discord bot
- **Database**: PostgreSQL
- **Cache**: Redis
- **Message Queue**: Kafka
- **Container Orchestration**: Kubernetes
- **AI Integration**: XAI, Gemini, OpenAI, Anthropic, Local LLM

## Getting Started

[To be implemented]

## Development

[To be implemented]

## Deployment

[To be implemented]

## License

This project is licensed under a proprietary source-available license. The source code is publicly viewable, but any use, modification, distribution, or deployment requires a commercial license. 

Contact [contact@thementor.com] for licensing inquiries and pricing information.

© [Year] TheMentor sp. z o.o. All rights reserved.