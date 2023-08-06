# Changelog

All notable changes to this project will be documented in this file

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2021-09-11

### Breaking Changes

- `tealprint.TealPrint.level` now moved to `tealprint.TealConfig.level`
- `TealPrint` indentation now is a bool instead of an int. See [#4](https://github.com/Senth/tealprint/issues/4)

### Changed

- "Please report this [...]" message in `TealPrint.error()` is now optional, and is not shown by default [#6](https://github.com/Senth/tealprint/issues/6)

### Added

- Buffer messages and print them all at the same time [#3](https://github.com/Senth/tealprint/issues/3)
- Change indent spaces and indent character [#5](https://github.com/Senth/tealprint/issues/5)
- Can now push/pop indentation so that you don't have to keep track of indentation throughout classes [[#4](https://github.com/Senth/tealprint/issues/4)]
- Examples of indentation and colors in [README.md](README.md)

## [0.1.0] - 2021-07-04

### Added

- First version
- Print levels (none, error, warning, info, verbose, debug)
- Ability to color using colored package
