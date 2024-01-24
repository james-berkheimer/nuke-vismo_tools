# Nuke Pipeline Tools

These tools were written for a Nuke pipeline. The code is out of date but kept here for posterity.

## Scripts Summary

* **archiveTest.py**: Handles the archiving of Nuke scripts and shot frames. Includes utility functions like `uniqifyList` to remove duplicates from a list.

* **archiveTools.py**: Similar to `archiveTest.py`, also handles archiving tasks. Includes utility functions for getting the size of a directory and converting the size from bytes to a more readable format.

* **nukeAlphaToBeta.py**: Defines a class `Alpha_to_Beta` with methods for getting immediate subdirectories and updating file paths.

* **nukeImports.py**: Imports several other scripts and modules, likely to be used elsewhere in the pipeline.

* **nukeTools.py**: Defines a class `NukeTools` with various utility methods for Nuke. Sets up an instance of the `BackDrop` class from the `autoBackdrop` module.

* **VISMO_DeadlineNukeClient.py**: A client for Deadline, a render management software, within Nuke. Imports the `NukeTools` class and defines functions for getting the repository root and a `main` function.

