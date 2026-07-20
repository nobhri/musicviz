# Project Scope and Technical Boundaries

## Version 0 priorities

Prefer the choice that:

1. produces a playable video sooner;
2. uses existing FFmpeg capabilities;
3. introduces fewer dependencies and configuration options;
4. is easier to understand, change, or delete; and
5. supports publishing a real song.

## Excluded work

Do not add excluded Version 0 features unless the user explicitly changes the
scope. In particular, do not introduce a GUI, web application, alternative
implementation language, Python media-rendering library, custom audio analysis,
plugin architecture, database, render queue, cloud rendering, packaging system,
or social-media integration.

Use FFmpeg for media work. Python may later provide only a thin layer for input
validation, configuration, command construction, and process execution.
