# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.0.4] - 06.09.2021

- Fixed PyPi filename reuse issue that prevents deployment by jumping over
  `v1.0.2` and `v1.0.3`
- Use [binalyzer-core] v1.0.3:
  - Invalidate DOM cache on `count_property` or `count` assignment:
    - Ensure template copy is referenced by Binalyzer object
    - Rename `_invalidate_dom` to `invalidate` and make it publicly available
  - Added auto-sizing for the text attribute:
    - If `sizing` is set to `auto` and the `size` property is not set explicitly,
      the `text` property's length determines the template's size.
  - Added data extension:
    - If a template's size is greater than the data, the backed data will be
      extended up to the template's size using a default byte value of `0x00`.
- Use [binalyzer-template-provider] v1.0.2:
  - Added tests for auto-sizing using the text attribute

## [v1.0.1] - 22.07.2021

- Use fixed versions of dependencies:
  - Use [binalyzer-core] v1.0.1:
    - Added the `text` property:
      - The `text` property has been added to provide a way of storing static
        binary data with a template.
  - Use [binalyzer-cli] v1.0.0
  - Use [binalyzer-data-provider] v1.0.0
  - Use [binalyzer-template-provider] v1.0.1:
    - Added the `text` attribute
  - Use [binalyzer-rest] v1.0.0
  - Use [binalyzer-wasm] v1.0.0

## [v1.0.0] - 28.04.2021

- Initial release

[Unreleased]: https://github.com/denisvasilik/binalyzer
[v1.0.0]: https://github.com/denisvasilik/binalyzer/tags/v1.0.0
[v1.0.1]: https://github.com/denisvasilik/binalyzer/tags/v1.0.1
[v1.0.2]: https://github.com/denisvasilik/binalyzer/tags/v1.0.2
[v1.0.4]: https://github.com/denisvasilik/binalyzer/tags/v1.0.4

[binalyzer-core]: https://github.com/denisvasilik/binalyzer-core
[binalyzer-cli]: https://github.com/denisvasilik/binalyzer-cli
[binalyzer-template-provider]: https://github.com/denisvasilik/binalyzer-template-provider
[binalyzer-data-provider]: https://github.com/denisvasilik/binalyzer-data-provider
[binalyzer-rest]: https://github.com/denisvasilik/binalyzer-rest
[binalyzer-wasm]: https://github.com/denisvasilik/binalyzer-wasm