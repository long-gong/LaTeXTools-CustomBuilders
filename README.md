# Custom Builders for [LaTeXTools](https://github.com/SublimeText/LaTeXTools)

This repo provides a simple custom latex builder for [LaTeXTools](https://github.com/SublimeText/LaTeXTools). 


## Overview

This builder aims to natively solve the notorious "Not All Fonts Are Eebedded" issue. If you do not encounter such an issue, or we prefer more easier but less elegant solution (_e.g._, [How to embed all the fonts in a PDF file](http://as.exeter.ac.uk/media/level1/academicserviceswebsite/tqa/assessmentprogressionandawardingtaughtprogrammes/embedfonts.pdf)), then you do not spend any time to play with this builder. 

If you windows, then you are recommended to use [WinEdit](https://www.winedt.com/) to "emjoy all benefits of this builder" with much less and easier configurations: [tutorial](https://lgong30.github.io/skill/2015/08/05/Not-All-Font-Embedded.html).


Currently, this builder ONLY supports Windows and Linux, and ONLY tested under Windows 10 and Ubuntu 18.04. 

## Requirements

Since this is a builder for LaTeXTools, a popular plugin for Sublime Text, therefore, you have to first install them: [tutorial](https://github.com/SublimeText/LaTeXTools/blob/master/README.markdown). 

In this builder, we use [Ghostscript](https://www.ghostscript.com/) to embed all fonts that are needed, so we also need download [the proper version of Ghostscript](https://www.ghostscript.com/download/gsdnld.html). Note that "GNU Affero General Public License" should be good enough. Please do not forget to add it to the PATH environment (you can either add it to the OS PATH environment or only add it to LaTeXTools via the "texpath" key for the platform you are using in its perference setting file, __i.e.,__ LaTeXTools.sublime-settings).

## Configuration

1. Copy wineBuilder.py to the builders folder of LaTeXTools, usually it is located at <Packages Folder>\LaTeXTools\builders. <Packages Folder> can be found by selecting *Preferences|Browse Packages...* or running the *Preferences: Browse Packages* command in Sublime Text. 
2. Add the following lines in the sublime latex builder configuration file (__i.e.,__ *LaTeX.sublime-build*) as the last builder under the key "variants":
    ```json
    	{
			"name": "Custom Builder - Method (dvi->ps->pdf)",
			"builder": "wine"
		}
    ```
    After adding the configuration file should be as follows.
        ```json
    // Compilation settings
    // ====================
    //
    // DO NOT TOUCH THIS FILE!
    // All configuration now occurs in LaTeXTools Preferences.sublime-settings
    // Put a copy of *that* file in your User directory and customize at will
    //
    // Again: there is NOTHING user-customizable here anymore.

    {

        "target": "make_pdf",
        "selector": "text.tex.latex",

        "osx":
            {
                "file_regex": "^(...*?):([0-9]+): ([0-9]*)([^\\.]+)"
            },

        "windows":
            {
                "file_regex": "^((?:.:)?[^:\n\r]*):([0-9]+):?([0-9]+)?:? (.*)$"
            },

        "linux":
            {
                "file_regex": "^(...*?):([0-9]+): ([0-9]*)([^\\.]+)"
            },

        "variants":
        [
            {
                "name": "Traditional",
                "builder": "traditional"
            },
            {
                "name": "PdfLaTeX",
                "builder": "traditional",
                "program": "pdflatex"
            },
            {
                "name": "XeLaTeX",
                "builder": "traditional",
                "program": "xelatex"
            },
            {
                "name": "LuaLaTeX",
                "builder": "traditional",
                "program": "lualatex"
            },
            {
                "name": "Basic Builder",
                "builder": "basic"
            },
            {
                "name": "Basic Builder - PdfLaTeX",
                "builder": "basic",
                "program": "pdflatex"
            },
            {
                "name": "Basic Builder - XeLaTeX",
                "builder": "basic",
                "program": "xelatex"
            },
            {
                "name": "Basic Builder - LuaLaTeX",
                "builder": "basic",
                "program": "lualatex"
            },
            {
                "name": "Script Builder",
                "builder": "script"
            },
            {
                "name": "Custom Builder - Method (dvi->ps->pdf)",
                "builder": "wine"
            }
        ]
    } 
    ```

You might notice the *"DO NOT TOUCH THIS FILE!"* in the configuration file. At the very beginning, I did not plan to touch this file, and I believed a better solution could be to reply on [the less-hacking way provided officially by LaTeXTools](https://github.com/SublimeText/LaTeXTools/wiki/Custom-Builders). However, I failed to make it work. After trying for several times, I just gave up and changed to this more hacking way. 




