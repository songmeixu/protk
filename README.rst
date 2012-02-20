=====
ProTK
=====

:Version: 0.3.0-DEV
:Last Update: 15 Feb 2012

Overview
========

ProTK is a toolkit for integrating workflows using automated speech recognition
software, such as HTK or Shphinx, with Praat auditory feature extraction and
WEKA machine learning models.

Authors
-------
University of Minnesota - Twin Cities

* Thomas Christie - Cognitive Science
* Serguei Pakhomov - College of Pharmacy
* Jacob Okamoto - Computer Science

License
=======
    
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Features
========
Features that are currently implemented are listed first; unimplemented
or incomplete features still under development are in *italics*.

* Database storage of prosodic and analysis data
* TextGrid word and phoneme tier parsing
* Praat script generation on-the-fly for each input file
* Praat script execution using as many CPUs as are available on the
  system
* *Praat analysis data extraction*
* *Per-analysis type functions (e.g., calculation of formant rations*

Usage
=====
The scripts for ProTK are in the ``protk`` directory in the root of the
distribution (this will be changed once the rewrite is complete).

``ingest.py``: Data ingest
--------------------------
``ingest.py`` is used to ingest all relevant data for a fileset (textgrids
and audio files). It will parse the textgrids and then generate and run
Praat analysis scripts for the audio files.

Options:
    
* ``--audio``: **required** -- directory containing audio files
* ``--truth``: directory containing truth textgrids
* ``--train``: directory containing training textgrids
* ``--script``: directory to which to output Praat scripts
* ``--praatoutput``: directory to which to output Praat analysis data files

