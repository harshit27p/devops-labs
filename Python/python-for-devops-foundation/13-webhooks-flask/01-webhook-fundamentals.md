# Webhook Fundamentals

Polling repeatedly asks whether data changed; a webhook lets the provider send an HTTP request when an event occurs.

A delivery commonly includes a POST request, event and delivery headers, and a JSON body. The receiver validates authenticity and payload, then responds with an appropriate 2xx status when accepted.

Assume events may be duplicated, arrive out of order, or be retried after temporary failures. Separate receipt from slow processing and use persistent event tracking.

Exercises: diagram GitHub → receiver → ticket API, identify what is trusted only after signature verification and explain why handlers should respond quickly.
