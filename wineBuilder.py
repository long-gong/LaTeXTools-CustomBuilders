# ST2/ST3 compat
from __future__ import print_function
import sublime
from latextools_utils.external_command import (
	external_command, get_texpath, update_env
)

if sublime.version() < "3000":
    # we are on ST2 and Python 2.X
    _ST3 = False
else:
    _ST3 = True

import os
import os.path
import re
import subprocess
# This will work because makePDF.py puts the appropriate
# builders directory in sys.path
from pdfBuilder import PdfBuilder

DEBUG = True

# ----------------------------------------------------------------
# WineBuilder class
#
# Mimic WinEdit's PdfTexify with Method (dvi->ps->pdf)
#
#


class WineBuilder(PdfBuilder):
    def __init__(self, *args):
        # Sets the file name parts, plus internal stuff
        super(WineBuilder, self).__init__(*args)

        # Now do our own initialization: set our name, see if we want to display output
        self.name = "Custom Builder"
        self.display_log = self.builder_settings.get("display_log", False)
        self.env = self.builder_settings.get(sublime.platform(), {}).get("env", None)
		# Loaded here so it is calculated on the main thread
        self.texpath = get_texpath() or os.environ['PATH']

    def commands(self):
        # Print greeting
        self.display("\n\nWineBuilder: ")

		# create an environment to be used for all subprocesses
		# adds any settings from the `env` dict to the current
		# environment
        env = dict(os.environ)
        env['PATH'] = self.texpath
        if self.env is not None and isinstance(self.env, dict):
            update_env(env, self.env)

        latex = ["latex", "-src", "-interaction=nonstopmode", "-synctex=1"]
        bibtex = ["bibtex"]
        dvi2ps = ["dvips"]
		# Get the platform 
        plat = sublime.platform()		
		# ps2pdf command, with reasonable executable (NOTE: we assume you installed 64-bit Ghostscrit)
        gs = "gswin64c" if plat == "windows" else "gs-952-linux-x86_64"
        ps2pdf = [
            gs,
            "-dNOPAUSE",
            "-dBATCH",
            "-sDEVICE=pdfwrite",
            "-dPDFSETTINGS=/prepress",
            "-dCompatibilityLevel=1.4",
            "-dSubsetFonts=true",
            "-dEmbedAllFonts=true",
            '-sOutputFile="' + self.base_name + '.pdf"',
            "-c",
            "save",
            "pop",
            "-f",
        ]

        # Regex to look for missing citations
        # This works for plain latex; apparently natbib requires special handling
        # TODO: does it work with biblatex?
        citations_rx = re.compile(r"Warning: Citation `.+' on page \d+ undefined")

        # We have commands in our PATH, and are in the same dir as the master file

        # This is for debugging purposes
        def display_results(n):
            if self.display_log:
                self.display("Command results, run %d:\n" % (n,))
                self.display(self.out)
                self.display("\n")

        run = 1
        brun = 0
        yield (latex + [self.base_name], "latex run %d; " % (run,))
        display_results(run)

        # Check for citations
        # Use search, not match: match looks at the beginning of the string
        # We need to run latex twice after bibtex
        if citations_rx.search(self.out):
            brun = brun + 1
            yield (bibtex + [self.base_name], "bibtex run %d; " % (brun,))
            display_results(1)
            run = run + 1
            yield (latex + [self.base_name], "latex run %d; " % (run,))
            display_results(run)
            run = run + 1
            yield (latex + [self.base_name], "latex run %d; " % (run,))
            display_results(run)

        # Apparently natbib needs separate processing
        if "Package natbib Warning: There were undefined citations." in self.out:
            brun = brun + 1
            yield (bibtex + [self.base_name], "bibtex run %d; " % (brun,))
            display_results(2)
            run = run + 1
            yield (latex + [self.base_name], "latex run %d; " % (run,))
            display_results(run)
            run = run + 1
            yield (latex + [self.base_name], "latex run %d; " % (run,))
            display_results(run)

        # Check for changed labels
        # Do this at the end, so if there are also citations to resolve,
        # we may save one pdflatex run
        if "Rerun to get cross-references right." in self.out:
            run = run + 1
            yield (latex + [self.base_name], "latex run %d; " % (run,))
            display_results(run)
        yield (dvi2ps + [self.base_name], "dvips run %d; " % (run,))
        display_results(run)

        # NOTE: here, ps2pdf is considered as an external command, because we use customized 
        # executable instead of the built-in on
        cmd = external_command(
					ps2pdf + [self.base_name + ".ps"], env=env, cwd=self.tex_dir, use_texpath=False,
					shell=True, stdout=subprocess.PIPE,
					stderr=subprocess.STDOUT
				)
        yield (cmd, "ps2pdf run %d; " % (run,))
        display_results(run)

        self.display("done.\n")
