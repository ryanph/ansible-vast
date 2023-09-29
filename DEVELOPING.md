# Developer Notes

Modules are built with a combination of:

- The OpenAPI specification (spec.yaml) in the [vastsdk](github.com/ryanph/vastsdk) repository
- Configuration from `settings.yaml` to indicate which schemas should become modules, what fields are included, and what SDK functions should be used to perform actions etc
- Jinja2 templates (templates/)

This generative approach is possible because of the robust PATCH method in the VMS API which makes applying changes to resources simple.