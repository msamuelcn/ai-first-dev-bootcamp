# RESTROSPECTIVE

## Friday Defense Questions

1. Walk me through the spec you wrote for Sprint 1 before touching a keyboard. What did you get wrong?
 - I initially underestimated the importance of project structure and modularity. I started with a single file (`main.py`) for everything, which led to circular import issues when the AI generated code that referenced models before they were defined. I had to refactor to create a separate `models.py` and add `__init__.py` files to properly structure the app and tests as packages. This was a key learning about how to set up a maintainable FastAPI project from the start.

2. Show me a function the AI generated that you changed. Why did you change it?
 - The AI generated a `create_workout` endpoint that directly used the `WorkoutBase` model for both input and output. I changed it to use `WorkoutCreate` for input (which inherits from `WorkoutBase` but is meant for creation) and `Workout` for output (which includes an `id` field). This change was necessary to align with common API design practices and to ensure that the response included all relevant information about the created workout, including its unique identifier.
3. What would happen to your API if I sent malformed JSON to every endpoint simultaneously?
 - In my current implementation, if malformed JSON were sent to the endpoints, FastAPI would return a 400 Bad Request error for each request. This is because FastAPI uses Pydantic for data validation, and when it fails to parse the input data according to the defined models, it raises a validation error. The API would remain stable and responsive, but the client would receive error responses indicating that the input was not valid.
 - If malformed JSON were sent to the endpoints, FastAPI should  return a 422 Unprocessable Entity error for each request. This is because FastAPI uses Pydantic for data validation, and when it fails to parse the input data according to the defined models, it raises a validation error. The API would remain stable and responsive, but the client would receive error responses indicating that the input was not valid.
4. What does the MCP protocol actually do under the hood? Explain it without acronyms.
 - The MCP protocol allows the CLI to communicate with an external server process that provides access to the filesystem. When a command like `summarize` is run, the CLI sends a request to this server asking it to perform certain operations, such as reading a file or listing a directory. The server processes the request and sends back a structured response. This means that instead of the CLI directly accessing files on its own, it relies on this separate process to handle all filesystem interactions, which can be useful for security and modularity.
5. If you had to rebuild Sprint 1 tomorrow without AI, which parts would take the longest and why?
 - The initial setup of the FastAPI project structure and the design of the Pydantic models would likely take the longest. This is because it requires careful planning to avoid issues like circular imports and to ensure that the API endpoints are well-designed and maintainable. Additionally, writing comprehensive tests for each endpoint would also be time-consuming, as it involves thinking through various edge cases and ensuring that all scenarios are covered effectively.





