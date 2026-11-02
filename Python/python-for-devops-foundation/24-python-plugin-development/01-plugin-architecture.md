# Plugin Architecture and Contracts

A plugin should have a narrow, documented contract. The host owns orchestration, configuration validation, logging and error handling.

## Design decisions
- What capability does a plugin provide?
- What inputs and outputs are allowed?
- How are versions handled?
- Can a plugin fail without stopping the host?
- What permissions does it need?
- How is the plugin approved and updated?

Prefer explicit registration for small internal tools. Dynamic discovery is useful when the plugin ecosystem is larger, but increases complexity and risk.
